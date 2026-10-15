"""Single explicitly authorized LLDB window; never schedules or retries attach."""
import json
import os
import signal
import time
from pathlib import Path

import lldb


def _save_private(path, payload):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(payload, stream)


def _interrupt(_signum, _frame):
    raise KeyboardInterrupt


def capture(debugger, pid, output, duration=20.0):
    """One attach, bounded stop count, detach before writing private material."""
    if not 0 < duration <= 20:
        raise ValueError('Invalid capture duration')
    folder = Path(output)
    if folder.stat().st_mode & 0o077:
        raise ValueError('Private output directory required')
    start = time.monotonic()
    deadline = start + duration
    result = {'outcome': 'error', 'hits': 0, 'matching': 0, 'detached': False}
    values = set()
    target = None
    process = None
    previous_handlers = {s: signal.signal(s, _interrupt) for s in (signal.SIGTERM, signal.SIGINT)}
    try:
        debugger.SetAsync(True)
        target = debugger.CreateTarget('/Applications/WeChat.app/Contents/MacOS/WeChat')
        listener = lldb.SBListener('single-media-window')
        error = lldb.SBError()
        process = target.AttachToProcessWithID(listener, pid, error)
        if not error.Success() or not process.IsValid():
            result['outcome'] = 'attach_failed'
            return result
        breakpoints = [target.BreakpointCreateByName(name) for name in ('CCCrypt', 'CCCryptorCreate')]
        if not all(bp.GetNumLocations() for bp in breakpoints):
            result['outcome'] = 'symbols_missing'
            return result
        ids = {bp.GetID() for bp in breakpoints}
        previous_stop = process.GetStopID()
        if not process.Continue().Success():
            result['outcome'] = 'continue_failed'
            return result
        print('MEDIA_WINDOW_READY', flush=True)
        result['outcome'] = 'timeout'
        hot_start = None
        while time.monotonic() < deadline:
            state = process.GetState()
            if state == lldb.eStateStopped and process.GetStopID() != previous_stop:
                previous_stop = process.GetStopID()
                owned_stop = False
                for thread in process:
                    if thread.GetStopReason() != lldb.eStopReasonBreakpoint:
                        continue
                    if thread.GetStopReasonDataAtIndex(0) not in ids:
                        continue
                    owned_stop = True
                    result['hits'] += 1
                    now = time.monotonic()
                    if hot_start is None:
                        hot_start = now
                    frame = thread.GetFrameAtIndex(0)
                    regs = [frame.FindRegister('x' + str(i)) for i in range(5)]
                    if not all(reg.IsValid() for reg in regs):
                        raise ValueError('Register unavailable')
                    op, alg, options, pointer, size = [reg.GetValueAsUnsigned() for reg in regs]
                    if op == 1 and alg == 0 and options & 2 and size == 16 and pointer:
                        result['matching'] += 1
                        memory_error = lldb.SBError()
                        value = process.ReadMemory(pointer, 16, memory_error)
                        if not memory_error.Success() or len(value) != 16:
                            raise ValueError('Memory unavailable')
                        values.add(bytes(value).hex())
                if not owned_stop:
                    result['outcome'] = 'unexpected_stop'
                    break
                if result['hits'] >= 16 or (result['hits'] >= 5 and time.monotonic() - hot_start < 1):
                    result['outcome'] = 'hit_limit'
                    break
                if len(values) >= 8:
                    result['outcome'] = 'value_limit'
                    break
                if not process.Continue().Success():
                    result['outcome'] = 'continue_failed'
                    break
            elif state in (lldb.eStateExited, lldb.eStateCrashed, lldb.eStateDetached, lldb.eStateInvalid):
                result['outcome'] = 'unexpected_target_state'
                break
            event = lldb.SBEvent()
            listener.WaitForEvent(1, event)
    except KeyboardInterrupt:
        result['outcome'] = 'cancelled'
    except Exception as exc:
        result['outcome'] = 'error'
        result['error_type'] = type(exc).__name__
    finally:
        # Repeated cancellation must not interrupt the release sequence.
        for signum in previous_handlers:
            signal.signal(signum, signal.SIG_IGN)
        try:
            if process is not None and process.IsValid():
                if process.GetState() not in (lldb.eStateDetached, lldb.eStateExited):
                    if process.GetState() != lldb.eStateStopped:
                        process.SendAsyncInterrupt()
                        cleanup_deadline = time.monotonic() + 2
                        while process.GetState() != lldb.eStateStopped and time.monotonic() < cleanup_deadline:
                            listener.WaitForEvent(1, lldb.SBEvent())
                    try:
                        target.DisableAllBreakpoints()
                    finally:
                        release = process.Detach(False)
                        result['detached'] = release.Success()
                else:
                    result['detached'] = process.GetState() == lldb.eStateDetached
        except Exception as exc:
            result['cleanup_error_type'] = type(exc).__name__
        finally:
            for signum, handler in previous_handlers.items():
                # Embedded LLDB may return None for a native C handler.
                # This one-shot interpreter exits immediately after capture.
                signal.signal(signum, signal.SIG_DFL if handler is None else handler)
        result['elapsed_seconds'] = round(time.monotonic() - start, 3)
        result['unique_values'] = len(values)
        if result['detached'] and values:
            _save_private(folder / 'parameters.json', sorted(values))
        _save_private(folder / 'result.json', result)
    return result

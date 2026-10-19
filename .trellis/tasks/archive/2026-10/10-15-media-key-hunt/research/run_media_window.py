"""Foreground supervisor for the user's ONE 2026-10-15 WeChat authorization.

This file is not a standing grant. Never schedule it or reuse an ended window.
"""
import json
import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path

TARGET = '/Applications/WeChat.app/Contents/MacOS/WeChat'
CONSUMED = Path('/tmp/myia-wechat-media-window-20261015.consumed')
DRIVER = Path(__file__).with_name('media_window.py').resolve()


def processes():
    raw = subprocess.check_output(
        ['/bin/ps', '-axo', 'pid=,ppid=,flags=,stat=,comm='], text=True, timeout=1)
    result = {}
    for line in raw.splitlines():
        row = line.split(None, 4)
        if len(row) == 5:
            result[int(row[0])] = {'ppid': int(row[1]), 'flags': int(row[2], 16),
                                  'state': row[3], 'exe': row[4]}
    return result


def preflight():
    rows = processes()
    targets = [pid for pid, row in rows.items() if row['exe'] == TARGET]
    if len(targets) != 1:
        raise RuntimeError('Expected exactly one WeChat process')
    pid = targets[0]
    if rows[pid]['flags'] & 0x800 or rows[pid]['state'].startswith(('T', 'Z')):
        raise RuntimeError('WeChat already traced or stopped')
    if any(Path(row['exe']).name in ('lldb', 'debugserver') for row in rows.values()):
        raise RuntimeError('Existing debugger; refusing to compete')
    return pid


def supervise(command, target_pid, folder, budget=24.0):
    started = time.monotonic()
    child = None
    owned = {}
    output = b''
    cancelled = False
    result = {'timed_out': False, 'cancelled': False}

    def cancel(_signum, _frame):
        nonlocal cancelled
        cancelled = True

    handlers = {s: signal.signal(s, cancel) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        # Same foreground session, never start_new_session or shell/background.
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while child.poll() is None:
            rows = processes()
            for pid, row in rows.items():
                if row['ppid'] == child.pid and Path(row['exe']).name == 'debugserver':
                    owned[pid] = row['exe']
            if cancelled or time.monotonic() - started >= budget:
                result['cancelled'] = cancelled
                result['timed_out'] = not cancelled
                break
            try:
                output, _ = child.communicate(timeout=min(0.2, max(0.01, budget - (time.monotonic() - started))))
            except subprocess.TimeoutExpired:
                continue
    finally:
        for signum in handlers:
            signal.signal(signum, signal.SIG_IGN)
        try:
            if child is not None:
                if child.poll() is None:
                    child.terminate()  # Driver handles TERM by detaching first.
                    try:
                        output, _ = child.communicate(timeout=2)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        output, _ = child.communicate(timeout=0.5)
                else:
                    output, _ = child.communicate(timeout=0.5)
                result['debugger_returncode'] = child.returncode
            # Only helper PIDs observed as direct children of this LLDB are ours.
            rows = processes()
            for pid, executable in owned.items():
                if pid in rows and rows[pid]['exe'] == executable:
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
            verification_deadline = min(started + 29, time.monotonic() + 1.5)
            while True:
                rows = processes()
                live = rows.get(target_pid)
                residual = [pid for pid, exe in owned.items()
                            if pid in rows and rows[pid]['exe'] == exe]
                result['wechat_running'] = bool(live and live['exe'] == TARGET and not live['state'].startswith(('T', 'Z')))
                result['wechat_traced'] = bool(live and live['flags'] & 0x800)
                result['owned_helpers_remaining'] = len(residual)
                if not residual and not result['wechat_traced']:
                    break
                if time.monotonic() >= verification_deadline:
                    break
                # Bounded ps verification; no retry or attach here.
                time.sleep(0.05)
            result['cleanup_ok'] = (result['wechat_running'] and not result['wechat_traced']
                                    and not result['owned_helpers_remaining'])
        finally:
            for signum, handler in handlers.items():
                signal.signal(signum, signal.SIG_DFL if handler is None else handler)
            result['elapsed_seconds'] = round(time.monotonic() - started, 3)
            # Raw LLDB output can contain private data: never print or commit it.
            fd = os.open(str(folder / 'lldb-private.log'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(output)
    return result


def main():
    pid = preflight()
    folder = Path(tempfile.mkdtemp(prefix='myia-media-window-'))
    # Fixed consumption marker prevents running this already authorized window twice.
    fd = os.open(str(CONSUMED), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump({'pid': pid, 'private_output': str(folder), 'authorization': '2026-10-15 single <=30s'}, stream)
    command = ['/usr/bin/xcrun', 'lldb', '--no-lldbinit', '--batch',
               '-o', 'settings set plugin.process.gdb-remote.packet-timeout 1',
               '-o', 'command script import ' + str(DRIVER),
               '-o', 'script media_window.capture(lldb.debugger, ' + str(pid) + ', ' + repr(str(folder)) + ', 20.0)',
               '-o', 'quit']
    result = supervise(command, pid, folder)
    result['private_output'] = str(folder)
    result['capture_recorded'] = (folder / 'result.json').is_file()
    result['capture_ok'] = False
    if result['capture_recorded']:
        capture_result = json.loads((folder / 'result.json').read_text())
        result['capture_ok'] = (capture_result.get('detached') is True
                                and capture_result.get('outcome') in ('timeout', 'hit_limit', 'value_limit')
                                and not result['timed_out'] and not result['cancelled'])
    print(json.dumps(result), flush=True)
    fd = os.open(str(folder / 'supervisor.json'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(result, stream)
    return 0 if result['cleanup_ok'] and result['capture_ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())

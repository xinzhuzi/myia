"""Offline lifecycle tests. None of these tests attaches to any application."""
import importlib.util
import json
import signal
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
CONSTANTS = dict(eStateStopped=1, eStateExited=2, eStateCrashed=3,
                 eStateDetached=4, eStateInvalid=5, eStateRunning=6,
                 eStopReasonBreakpoint=10)


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Error:
    def __init__(self, ok=True):
        self.ok = ok

    def Success(self):
        return self.ok


class Clock:
    def __init__(self):
        self.value = 0

    def monotonic(self):
        return self.value


class Register:
    def __init__(self, value, valid=True):
        self.value, self.valid = value, valid

    def IsValid(self):
        return self.valid

    def GetValueAsUnsigned(self):
        return self.value


class FakeThread:
    def __init__(self, process):
        self.process = process

    def GetStopReason(self):
        return 0 if self.process.mode == 'unexpected' else 10

    def GetStopReasonDataAtIndex(self, index):
        return 1

    def GetFrameAtIndex(self, index):
        return self

    def FindRegister(self, name):
        return Register([1, 0, 2, 100, 16][int(name[1:])], self.process.mode != 'register')


class Process:
    def __init__(self, mode):
        self.mode = mode
        self.state = 1
        self.stop_id = 0
        self.continues = 0
        self.detach_calls = []
        self.interrupts = 0

    def IsValid(self):
        return self.mode != 'attach'

    def GetState(self):
        return self.state

    def GetStopID(self):
        return self.stop_id

    def Continue(self):
        self.continues += 1
        self.state = 6
        return Error(self.mode != 'continue')

    def SendAsyncInterrupt(self):
        self.interrupts += 1
        self.state = 1

    def Detach(self, keep_stopped):
        self.detach_calls.append(keep_stopped)
        if self.mode != 'detach':
            self.state = 4
        return Error(self.mode != 'detach')

    def ReadMemory(self, address, length, error):
        error.ok = self.mode != 'memory'
        return bytes(range(16))

    def __iter__(self):
        return iter([FakeThread(self)])


class Target:
    def __init__(self, process):
        self.process = process
        self.attach_count = 0
        self.disabled = False

    def AttachToProcessWithID(self, listener, pid, error):
        self.attach_count += 1
        error.ok = self.process.mode != 'attach'
        return self.process

    def BreakpointCreateByName(self, name):
        return types.SimpleNamespace(GetNumLocations=lambda: int(self.process.mode != 'symbol'), GetID=lambda: 1)

    def DisableAllBreakpoints(self):
        self.disabled = True


@pytest.fixture
def environment(monkeypatch, tmp_path):
    def make(mode):
        process = Process(mode)
        target = Target(process)
        timer = Clock()

        class Listener:
            def __init__(self, name):
                pass

            def WaitForEvent(self, seconds, event):
                timer.value += 0.05
                if mode == 'cancel':
                    raise KeyboardInterrupt
                if mode not in ('timeout', 'symbol', 'attach'):
                    process.state = 1
                    process.stop_id += 1
                return True

        fake = types.SimpleNamespace(**CONSTANTS, SBError=Error, SBListener=Listener, SBEvent=object)
        monkeypatch.setitem(sys.modules, 'lldb', fake)
        module = load('media_window')
        module.time = timer
        debugger = types.SimpleNamespace(SetAsync=lambda value: None, CreateTarget=lambda name: target)
        tmp_path.chmod(0o700)
        return module, debugger, process, target
    return make


@pytest.mark.parametrize('mode,outcome', [
    ('normal', 'hit_limit'), ('timeout', 'timeout'), ('cancel', 'cancelled'),
    ('register', 'error'), ('memory', 'error'), ('unexpected', 'unexpected_stop'),
    ('symbol', 'symbols_missing'), ('attach', 'attach_failed'),
    ('continue', 'continue_failed'), ('detach', 'hit_limit')])
def test_release_all_paths(environment, tmp_path, mode, outcome):
    module, debugger, process, target = environment(mode)
    handlers = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    result = module.capture(debugger, 123, tmp_path, 1.0)
    assert result['outcome'] == outcome
    assert target.attach_count == 1
    assert {s: signal.getsignal(s) for s in handlers} == handlers
    if mode != 'attach':
        assert process.detach_calls == [False]
        assert target.disabled
    assert result['detached'] == (mode not in ('attach', 'detach'))
    assert (tmp_path / 'parameters.json').exists() == (mode == 'normal')
    for path in tmp_path.iterdir():
        assert path.stat().st_mode & 0o077 == 0
    assert json.loads((tmp_path / 'result.json').read_text()) == result


def test_rejects_unsafe_duration_before_attach(environment, tmp_path):
    module, debugger, process, target = environment('normal')
    with pytest.raises(ValueError):
        module.capture(debugger, 123, tmp_path, 21)
    assert target.attach_count == 0


def test_supervisor_timeout(tmp_path, monkeypatch):
    module = load('run_media_window')
    monkeypatch.setattr(module, 'processes', lambda: {123: {'exe': module.TARGET, 'flags': 0x4044, 'state': 'S', 'ppid': 1}})
    # This child merely waits; it has no LLDB import or attach operation.
    result = module.supervise([sys.executable, '-c', 'import time; time.sleep(10)'], 123, tmp_path, budget=0.15)
    assert result['timed_out']
    assert result['cleanup_ok']
    assert result['elapsed_seconds'] < 3


def test_supervisor_detects_traced_target(tmp_path, monkeypatch):
    module = load('run_media_window')
    monkeypatch.setattr(module, 'processes', lambda: {123: {'exe': module.TARGET, 'flags': 0x4844, 'state': 'S', 'ppid': 1}})
    result = module.supervise([sys.executable, '-c', 'pass'], 123, tmp_path)
    assert not result['cleanup_ok']
    assert result['wechat_traced']


def test_once_marker_prevents_second_start(tmp_path, monkeypatch):
    module = load('run_media_window')
    marker = tmp_path / 'consumed'
    marker.write_text('already used')
    monkeypatch.setattr(module, 'CONSUMED', marker)
    monkeypatch.setattr(module, 'preflight', lambda: 123)
    monkeypatch.setattr(module.tempfile, 'mkdtemp', lambda **kwargs: str(tmp_path))
    monkeypatch.setattr(module, 'supervise', lambda *args: pytest.fail('second execution prohibited'))
    with pytest.raises(FileExistsError):
        module.main()


def test_foreground_cancellation(tmp_path, monkeypatch):
    module = load('run_media_window')
    monkeypatch.setattr(module, 'processes', lambda: {123: {'exe': module.TARGET, 'flags': 0x4044, 'state': 'S', 'ppid': 1}})
    original_popen = module.subprocess.Popen

    def launch(*args, **kwargs):
        child = original_popen(*args, **kwargs)
        # Deliver cancellation locally; child never imports a debugger.
        signal.raise_signal(signal.SIGINT)
        return child

    monkeypatch.setattr(module.subprocess, 'Popen', launch)
    result = module.supervise([sys.executable, '-c', 'import time; time.sleep(10)'], 123, tmp_path)
    assert result['cancelled']
    assert result['cleanup_ok']
    assert result['elapsed_seconds'] < 3


def test_missing_capture_metadata_is_failure(tmp_path, monkeypatch, capsys):
    module = load('run_media_window')
    monkeypatch.setattr(module, 'CONSUMED', tmp_path / 'consumed')
    monkeypatch.setattr(module, 'preflight', lambda: 123)
    monkeypatch.setattr(module.tempfile, 'mkdtemp', lambda **kwargs: str(tmp_path))
    monkeypatch.setattr(module, 'supervise', lambda *args: {'cleanup_ok': True, 'timed_out': False, 'cancelled': False})
    assert module.main() == 2
    result = json.loads(capsys.readouterr().out)
    assert not result['capture_ok'] and not result['capture_recorded']

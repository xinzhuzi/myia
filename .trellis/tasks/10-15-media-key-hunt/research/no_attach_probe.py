"""Exercise real LLDB embedded signal handling with fake target/process only."""
import importlib.util
import tempfile
import types
from pathlib import Path

import lldb


def run():
    path = Path(__file__).with_name('media_window.py')
    spec = importlib.util.spec_from_file_location('probe_capture', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    state = {'detached': False, 'disabled': False, 'attach_calls': 0}
    ok = types.SimpleNamespace(Success=lambda: True)
    failed = types.SimpleNamespace(Success=lambda: False)

    def detach(keep_stopped):
        assert keep_stopped is False
        state['detached'] = True
        return ok

    # No real SBTarget/SBProcess is created; there is no OS attach operation.
    process = types.SimpleNamespace(IsValid=lambda: True, GetState=lambda: lldb.eStateStopped,
                                    GetStopID=lambda: 0, Continue=lambda: failed, Detach=detach)

    def fake_attach(listener, pid, error):
        state['attach_calls'] += 1
        return process

    def disable():
        state['disabled'] = True

    target = types.SimpleNamespace(AttachToProcessWithID=fake_attach, DisableAllBreakpoints=disable,
                                   BreakpointCreateByName=lambda name: types.SimpleNamespace(
                                       GetNumLocations=lambda: 1, GetID=lambda: 1))
    debugger = types.SimpleNamespace(SetAsync=lambda value: None, CreateTarget=lambda name: target)
    folder = Path(tempfile.mkdtemp(prefix='myia-no-attach-probe-'))
    result = module.capture(debugger, 0, folder, 1)
    assert state == {'detached': True, 'disabled': True, 'attach_calls': 1}
    assert result['outcome'] == 'continue_failed' and result['detached']
    assert (folder / 'result.json').is_file()
    print('NO_ATTACH_EMBEDDED_CLEANUP_AND_PERSISTENCE_OK', flush=True)

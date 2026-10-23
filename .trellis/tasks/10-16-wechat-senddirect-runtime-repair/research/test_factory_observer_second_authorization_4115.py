"""Live preflight gate under fake process/disk responses; no subprocess started."""
from __future__ import annotations

import io
import json
import plistlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import run_factory_observer_second_4115 as supervisor


def authorization():
    # A test value only: this is never written into the real task or used live.
    return {'consumed': False, 'max_seconds': 30, 'target': 'WeChat 4.1.15 (270135)',
            'purpose': 'one factory hit: manual filehelper test digests and thread stack',
            'recipient': 'filehelper', 'content': '今天真是个好日子',
            'single_foreground_window': True, 'no_native_calls': True, 'no_automatic_send': True}


def setup_gate(monkeypatch, tmp_path, auth):
    root = tmp_path / 'research'
    root.mkdir()
    (root / 'factory-second-cleanup-qualification.json').write_text(json.dumps({'passed': True, 'hashes': {}}))
    (root.parent / 'task-tiers.json').write_text(json.dumps({'tiers': [{}, {}, {
        'factory_observation_second_authorization': auth}]}))
    monkeypatch.setattr(supervisor, 'ROOT', root)
    monkeypatch.setattr(supervisor, 'source_hashes', lambda: {})
    monkeypatch.setattr(supervisor.subprocess, 'run', lambda *_args, **_kwargs: SimpleNamespace(returncode=1))
    monkeypatch.setattr(supervisor.subprocess, 'check_output', lambda *_args, **_kwargs: '777\n')
    before = {'pid': 777, 'flags': 0, 'state': 2, 'start_sec': 1,
              'start_usec': 2, 'executable': supervisor.WECHAT}
    monkeypatch.setattr(supervisor, 'status', lambda _pid: before)
    original_open = Path.open

    def read_plist(path, *args, **kwargs):
        if str(path) == '/Applications/WeChat.app/Contents/Info.plist':
            return io.BytesIO(plistlib.dumps({'CFBundleShortVersionString': '4.1.15',
                                             'CFBundleVersion': '270135'}))
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', read_plist)
    senddirect = SimpleNamespace(load_anchor_table=lambda _path: {},
                                 _validate_disk_anchor=lambda _table: {'anchored': 'ok'})
    monkeypatch.setitem(sys.modules, 'wechat_bridge', SimpleNamespace(senddirect=senddirect))

    def reject_process(*_args, **_kwargs):
        pytest.fail('authorization preflight started a process')

    monkeypatch.setattr(supervisor.subprocess, 'Popen', reject_process)
    return root, before


def test_missing_authorization_rejects_without_process_or_window(monkeypatch, tmp_path):
    root, _ = setup_gate(monkeypatch, tmp_path, None)
    with pytest.raises(RuntimeError, match='authorization is missing'):
        supervisor.supervise('live', 'observe')
    assert sorted(path.name for path in root.iterdir()) == ['factory-second-cleanup-qualification.json']


@pytest.mark.parametrize('key,value', [
    ('consumed', True), ('max_seconds', 31), ('target', 'another process'),
    ('purpose', 'send'), ('recipient', 'someone else'), ('content', 'different text'),
    ('single_foreground_window', False), ('no_native_calls', False), ('no_automatic_send', False),
])
def test_changed_scope_and_reuse_rejected(monkeypatch, tmp_path, key, value):
    auth = authorization()
    auth[key] = value
    root, _ = setup_gate(monkeypatch, tmp_path, auth)
    with pytest.raises(RuntimeError):
        supervisor.supervise('live', 'observe')
    assert sorted(path.name for path in root.iterdir()) == ['factory-second-cleanup-qualification.json']


def test_matching_scope_only_returns_metadata(monkeypatch, tmp_path):
    root, before = setup_gate(monkeypatch, tmp_path, authorization())
    assert supervisor.preflight_live() == before
    assert not (root / 'factory-window-second-consumed.json').exists()


def test_changed_qualified_sources_rejected(monkeypatch, tmp_path):
    setup_gate(monkeypatch, tmp_path, authorization())
    monkeypatch.setattr(supervisor, 'source_hashes', lambda: {'changed': 'hash'})
    with pytest.raises(RuntimeError, match='source changed'):
        supervisor.preflight_live()


def test_old_window_authorization_does_not_authorize_second(monkeypatch, tmp_path):
    root, _ = setup_gate(monkeypatch, tmp_path, None)
    task = root.parent / 'task-tiers.json'
    data = json.loads(task.read_text())
    data['tiers'][2]['factory_observation_authorization'] = authorization()
    task.write_text(json.dumps(data))
    with pytest.raises(RuntimeError, match='authorization is missing'):
        supervisor.supervise('live', 'observe')
    assert sorted(path.name for path in root.iterdir()) == ['factory-second-cleanup-qualification.json']


def test_consumption_marker_rejects_before_creating_window(monkeypatch, tmp_path):
    root, _ = setup_gate(monkeypatch, tmp_path, authorization())
    marker = root / 'factory-window-second-consumed.json'
    marker.write_text('{}')
    before = sorted(path.name for path in root.iterdir())
    with pytest.raises(RuntimeError, match='already consumed'):
        supervisor.supervise('live', 'observe')
    assert sorted(path.name for path in root.iterdir()) == before

"""Exercise disabled launchers with fake external commands, never a debugger."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / '.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath'
SCRIPTS = sorted(TARGET.glob('drive_wf*.sh'))
assert len(SCRIPTS) == 5, 'Review new or missing launchers before proceeding'
# Refuse to run any script unless its entire executable prefix is this known gate.
for script in SCRIPTS:
    prefix = script.read_text().split('exit 78\n', 1)[0] + 'exit 78\n'
    lines = [line for line in prefix.splitlines() if line.strip() and not line.startswith('#')]
    assert len(lines) == 2 and lines[0].startswith("printf '%s\\n' 'Disabled:") and lines[0].endswith("' >&2") and lines[1] == 'exit 78', script

def snapshot():
    return {str(p.relative_to(TARGET)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in TARGET.iterdir() if p.is_file()}

before = snapshot()
results = []
with tempfile.TemporaryDirectory(prefix='senddirect-guard-') as temp:
    probe = Path(temp)
    marker = probe / 'unexpected-command'
    for name in ('lldb', 'pgrep', 'kill', 'sleep', 'sed', 'rm', 'tee', 'date', 'head', 'grep', 'bash', 'osascript', 'open', 'wechat-bridge'):
        stub = probe / name
        stub.write_text('#!/bin/bash\nprintf "%s\\n" "$0" >> "$PROBE_MARKER"\nexit 91\n')
        stub.chmod(0o700)
    env = {'PATH': str(probe), 'PROBE_MARKER': str(marker)}
    for script in SCRIPTS:
        syntax = subprocess.run(['/bin/bash', '-n', str(script)], env=env, capture_output=True, timeout=5)
        assert syntax.returncode == 0, syntax.stderr
        result = subprocess.run(['/bin/bash', str(script)], env=env, capture_output=True, timeout=5)
        assert result.returncode == 78 and not result.stdout and b'Disabled:' in result.stderr, script
        assert not marker.exists(), f'External command attempted by {script}'
        results.append({'script': script.name, 'syntax_exit': syntax.returncode, 'exit': result.returncode})
assert before == snapshot(), 'Historical experiment files changed during verification'
print(json.dumps({'passed': True, 'results': results, 'historical_files_unchanged': len(before),
                  'external_commands_invoked': 0, 'scope': 'five legacy launchers only; not a global enforcement mechanism'}, indent=2))

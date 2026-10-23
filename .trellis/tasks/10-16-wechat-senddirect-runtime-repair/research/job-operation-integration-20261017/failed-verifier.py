"""Build one owned job/request integration fixture; never access WeChat."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
root = repo / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
assert platform.system() == 'Darwin' and platform.machine() == 'arm64'
output = root / 'job-operation-integration-20261017'
output.mkdir()
sys.path.insert(0, str(root))
from newsendmsg_wire_4115 import MessageItem, build_request  # noqa: E402

wire = build_request((MessageItem(
    field_1=b'fixture-only', field_2='离线组合测试'.encode(),
    field_3=1, field_4=0, field_5=0),))
wire_path = output / 'owned-input.bin'
with wire_path.open('xb') as handle:
    handle.write(wire)
source = root / 'test_newsendmsg_job_operation_4115.cpp'
binary = output / 'fixture'
command = ['clang++', '-std=c++17', '-Wall', '-Wextra', '-Werror',
           str(source), '-o', str(binary)]
version = subprocess.run(['clang++', '--version'], capture_output=True, text=True,
                         check=True, timeout=5).stdout
build = subprocess.run(command, capture_output=True, text=True, timeout=20)
with (output / 'build.json').open('x') as handle:
    json.dump({'args': command, 'returncode': build.returncode,
               'stdout': build.stdout, 'stderr': build.stderr}, handle, indent=2)
assert build.returncode == 0, build.stderr
run = subprocess.run([str(binary), str(wire_path)], capture_output=True, text=True, timeout=10)
with (output / 'run.json').open('x') as handle:
    json.dump({'returncode': run.returncode, 'stdout': run.stdout,
               'stderr': run.stderr}, handle, indent=2)
assert run.returncode == 0, (run.returncode, run.stderr)
result = json.loads(run.stdout)
assert result == {
    'cases': 10, 'job_completion_is_not_request_drain': True,
    'job_cancel_is_not_request_cancel': True,
    'late_callback_preserves_terminal_state': True,
    'owned_wire_matches_factory_copy': True, 'balanced_lifetime': True,
    'wechat_loaded': False, 'sent': False,
}
paths = [source, Path(__file__).resolve(), *(root / name for name in (
    'test_newsendmsg_operation_4115.cpp', 'newsendmsg_operation_4115.hpp',
    'newsendmsg_job_abi_4115.hpp', 'newsendmsg_native_body_4115.hpp',
    'newsendmsg_native_response_4115.hpp', 'newsendmsg_completion_4115.hpp',
    'newsendmsg_wire_4115.py', 'account-safety-stop-20261016.md'))]
report = {
    'passed': True, 'scope': 'Owned host fixture integration, not the native scheduler',
    'compiler': version, 'build': command, 'result': result,
    'source_sha256': {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in paths},
    'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
    'wire_sha256': hashlib.sha256(wire).hexdigest(),
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False,
    'limitations': [
        'Job/Group/Config and all service functions are owned fixtures with executable lifetime.',
        'No recovered native group/config layouts, scheduler semantics or thread-affinity proof.',
        'Body fixture copies bytes; it does not run the native protobuf parser.',
        'Self-owned serialized control is not a native queue drain or module-unload barrier.',
        'No real response correlation or independent delivery evidence.',
    ],
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({'passed': True, 'result': result, 'callable_for_send': False}))

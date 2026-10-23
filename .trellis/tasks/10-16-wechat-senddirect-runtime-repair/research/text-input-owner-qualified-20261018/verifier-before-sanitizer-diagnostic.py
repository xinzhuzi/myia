"""Qualify an owned text-input component using frozen bytes and host fixtures only."""
from __future__ import annotations

import hashlib
import json
import platform
import struct
import subprocess
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
root = repo / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
reader = repo / 'Library/ai/verify_wechat_input_type_20261016.py'
stop = root / 'account-safety-stop-20261016.md'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')


assert digest(reader) == '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'
assert digest(stop) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
assert platform.system() == 'Darwin' and platform.machine() == 'arm64'
assert len(sys.argv) <= 2
name = sys.argv[1] if len(sys.argv) == 2 else 'text-input-owner-qualified-20261018'
assert Path(name).name == name and name.startswith('text-input-owner-')
output = root / name
output.mkdir(exist_ok=False)
namespace = {'__file__': str(reader)}
prefix, separator, _ = reader.read_text().partition('rows, instructions = [], {}')
assert separator and "open('x')" not in prefix
exec(compile(prefix, str(reader), 'exec'), namespace)
read_va = namespace['read_va']
paths = {Path(__file__).resolve(), reader, stop}
for filename, expected in {
    'newsendmsg-text-input-path-contract.json':
        'ffa7abe710f241e7a70d655db85c0bc0e52e632c0b2482cbac5a9b1831ff1941',
    'newsendmsg-text-input-path-verification.json':
        'a30aec51184c813c2fbe1afca75c7569d557e095566c2977e5fb2853cd7b0b78',
}.items():
    path = root / filename
    assert digest(path) == expected
    paths.add(path)
contract = json.loads((root / 'newsendmsg-text-input-path-contract.json').read_text())
assert contract['binary_sha256'] == namespace['digest']
assert contract['numeric_one_input_identity_and_service_path_proven']
assert not contract['callable_for_send'] and not contract['runtime_observed']
instructions, exports = {}, []
for number, entry in ((164, '77bdd0'), (165, '77be90'), (167, '69a714'),
                      (171, '2920b74')):
    folder = root / f'text-contract-pass{number}'
    path = folder / f'native-fn-{entry}.asm'
    run_path = folder / 'run.json'
    run = json.loads(run_path.read_text())
    assert run['returncode'] == 0 and not run['target_attached']
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    for flag in ('-log', '-scriptlog'):
        log = Path(run['args'][run['args'].index(flag) + 1])
        assert 'REPORT SCRIPT ERROR' not in log.read_text()
        paths.add(log)
    lines = path.read_text().splitlines()
    for line in lines:
        address, raw, assembly = line.split('\t', 2)
        address, raw = int(address, 16), bytes.fromhex(raw)
        assert len(raw) == 4 and read_va(address, 4) == raw
        instructions[address] = assembly
    exports.append({'file': str(path.relative_to(root)), 'instructions': len(lines)})
    paths.update((path, path.with_suffix('.c'), run_path))
checks = {
    0x77bddc: 'mov x20,x8', 0x77bde0: 'mov w0,#0x610',
    0x77bde4: 'bl 0x07140030', 0x77bdec: 'bl 0x0077be90',
    0x77bdf0: 'adds x8,x19,#0x18', 0x77bdf4: 'stp x8,x19,[x20]',
    0x77beb0: 'str x8,[x0], #0x18', 0x77beb4: 'mov w1,#0x5f8',
    0x77beb8: 'bl 0x07140390', 0x77bec4: 'add x0,x19,#0x18',
    0x77becc: 'bl 0x0069a714', 0x77bee8: 'adrp x8,0x9eb2000',
    0x77beec: 'add x8,x8,#0x690', 0x77bef0: 'add x8,x8,#0x10',
    0x77bef4: 'str x8,[x19, #0x18]', 0x77befc: 'str q0,[x19, #0x5e0]',
    0x77bf00: 'str q0,[x19, #0x5f0]', 0x77bf04: 'str q0,[x19, #0x600]',
    0x69a764: 'stp q0,q0,[x0, #0x90]', 0x69a77c: 'str xzr,[x0, #0xe0]',
    0x69a780: 'str wzr,[x0, #0xe8]', 0x2920b68: 'bl 0x0077bdd0',
    0x2920b70: 'mov w9,#0x1', 0x2920b74: 'str w9,[x8, #0xe4]',
    0x2920b78: 'add x0,x8,#0x5c8', 0x2920b7c: 'add x1,sp,#0xf8',
    0x2920b80: 'bl 0x0713f8e0', 0x2920b88: 'add x0,x8,#0x90',
    0x2920b8c: 'mov x1,x21', 0x2920b90: 'bl 0x0713f8e0',
}
for site, expected in checks.items():
    assert instructions[site] == expected, (hex(site), instructions.get(site), expected)
branches = []
for site, target in ((0x77bde4, 0x7140030), (0x77bdec, 0x77be90),
                     (0x77beb8, 0x7140390), (0x77becc, 0x69a714),
                     (0x2920b68, 0x77bdd0), (0x2920b80, 0x713f8e0),
                     (0x2920b90, 0x713f8e0)):
    word = struct.unpack('<I', read_va(site, 4))[0]
    assert word >> 26 == 0b100101
    immediate = word & 0x3ffffff
    immediate -= (1 << 26) if immediate & (1 << 25) else 0
    assert site + immediate * 4 == target
    branches.append({'site': hex(site), 'target': hex(target)})

# Decode the ARM64 import stub, then walk its dyld chain to its exact import.
stub_address = 0x713f8e0
stub = struct.unpack('<3I', read_va(stub_address, 12))
assert stub[0] & 0x9f00001f == 0x90000010
assert stub[1] & 0xffc003ff == 0xf9400210 and stub[2] == 0xd61f0200
immediate = (((stub[0] >> 5) & 0x7ffff) << 2) | ((stub[0] >> 29) & 3)
immediate -= (1 << 21) if immediate & (1 << 20) else 0
slot = (stub_address & ~0xfff) + (immediate << 12) + ((stub[1] >> 10) & 0xfff) * 8
assert slot == 0x9b36500
segments, data, fixups = namespace['segments'], namespace['data'], namespace['fixups']
header = struct.unpack_from('<7I', data, fixups)
assert header[0] == 0 and header[5:] == (1, 0)
indices = [i for i, s in enumerate(segments) if s[0] <= slot < s[0] + s[3]]
assert len(indices) == 1
index = indices[0]
starts = fixups + header[1]
segment = starts + struct.unpack_from('<I', data, starts + 4 + index * 4)[0]
_, page_size, fmt, base, _, pages = struct.unpack_from('<IHHQIH', data, segment)
assert fmt == 6 and base == segments[index][0]
page = (slot - base) // page_size
assert page < pages
first = struct.unpack_from('<H', data, segment + 22 + page * 2)[0]
assert first != 0xffff and not first & 0x8000
chain = base + page * page_size + first
for steps in range(page_size // 4):
    word = struct.unpack('<Q', read_va(chain, 8))[0]
    if chain == slot:
        break
    stride = ((word >> 51) & 0xfff) * 4
    assert stride and chain + stride <= slot
    chain += stride
assert chain == slot and word >> 63 == 1 and ((word >> 24) & 0xff) == 0
ordinal = word & 0xffffff
assert ordinal < header[4]
imported = struct.unpack_from('<I', data, fixups + header[2] + ordinal * 4)[0]
offset = fixups + header[3] + (imported >> 9)
symbol = data[offset:data.index(0, offset)].decode('ascii')
assert symbol == '__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_'
assignment_import = {'stub': hex(stub_address), 'slot': hex(slot), 'ordinal': ordinal,
                     'symbol': symbol, 'chain_steps': steps + 1}

sources = [root / 'newsendmsg_text_input_4115.hpp',
           root / 'test_newsendmsg_text_input_4115.cpp', root / 'text_input_abi_fixture_4115.S']
paths.update(sources)
expected_result = {'cases': 21, 'hidden_x8': True, 'byte_preservation': True,
                   'ownership_checked': True, 'exception_cleanup': True,
                   'guard_regions_intact': True}
fixtures = []
for label, flags in (('strict', []), ('sanitized', ['-fsanitize=address,undefined',
                                                  '-fno-sanitize-recover=all',
                                                  '-fno-omit-frame-pointer'])):
    binary = output / f'fixture-{label}'
    command = ['clang++', '-std=c++17', '-Wall', '-Wextra', '-Werror', '-UNDEBUG',
               *flags, str(sources[1]), str(sources[2]), '-o', str(binary)]
    build = subprocess.run(command, capture_output=True, text=True, timeout=30)
    save(output / f'{label}-compile.json', {'args': command, 'returncode': build.returncode,
                                          'stdout': build.stdout, 'stderr': build.stderr})
    assert build.returncode == 0, build.stderr
    try:
        run = subprocess.run([str(binary)], capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired as error:
        save(output / f'{label}-timeout.json', {'timeout': 15, 'child_killed_by_subprocess': True,
                                              'stdout': str(error.stdout), 'stderr': str(error.stderr)})
        raise
    save(output / f'{label}-run.json', {'args': run.args, 'returncode': run.returncode,
                                      'stdout': run.stdout, 'stderr': run.stderr})
    assert run.returncode == 0 and not run.stderr, (label, run.returncode, run.stderr)
    result = json.loads(run.stdout)
    assert result == expected_result
    fixtures.append({'mode': label, 'result': result, 'binary_sha256': digest(binary)})
version = subprocess.run(['clang++', '--version'], capture_output=True, text=True, timeout=5)
assert version.returncode == 0
save(output / 'compiler.json', {'args': version.args, 'stdout': version.stdout})
report = {
    'passed': True, 'host': platform.machine(), 'binary_sha256': namespace['digest'],
    'exports': exports, 'native_instructions_matched': sum(x['instructions'] for x in exports),
    'instruction_positions_checked': len(checks), 'branch_decodes': branches,
    'assignment_import': assignment_import, 'fixtures': fixtures,
    'source_sha256': {str(p.relative_to(repo)): digest(p) for p in sorted(paths)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'send_verified': False, 'deployed': False, 'callable_for_send': False,
    'limitations': [
        'Owned host input construction only; no WeChat loading or function addresses bound.',
        'Object/allocator/control-block compatibility in the target remains unexecuted.',
        'No category parsing in this component does not prove final arbitrary-content preservation.',
        'Service prerequisites, coroutine context, cancellation, final drain and independent receipt remain open.',
        'Numeric type is written after assignments as an owned-construction policy; native builder writes it first.',
    ],
}
save(output / 'verification.json', report)
print(json.dumps({k: report[k] for k in ('passed', 'native_instructions_matched',
                                       'instruction_positions_checked', 'target_executed',
                                       'callable_for_send')} | {'fixture_cases_per_build': 21,
                                                              'sanitizers': ['address', 'undefined']}))

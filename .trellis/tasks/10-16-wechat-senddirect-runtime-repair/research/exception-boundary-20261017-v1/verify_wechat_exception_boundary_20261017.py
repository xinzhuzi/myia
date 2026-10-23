"""Verify frozen exception metadata, missing landing pads and owned final callback safety."""
from __future__ import annotations

import hashlib
import json
import platform
import re
import struct
import subprocess
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
root = repo / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
name = sys.argv[1]
assert Path(name).name == name and name.startswith('exception-boundary-20261017')
output = root / name
output.mkdir()
(output / 'verification_source.py').write_bytes(Path(__file__).read_bytes())
reader = repo / 'Library/ai/verify_wechat_input_type_20261016.py'
assert hashlib.sha256(reader.read_bytes()).hexdigest() == (
    '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17')
namespace = {'__file__': str(reader)}
exec(compile(reader.read_text().split('rows, instructions = [], {}', 1)[0],
             str(reader), 'exec'), namespace)
stop = root / 'account-safety-stop-20261016.md'
assert hashlib.sha256(stop.read_bytes()).hexdigest() == (
    'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d')
args = json.loads((root / 'native-contract-run.json').read_text())['args']
binary = Path(args[1]).parent / 'wechat_arm64.dylib'
assert platform.system() == 'Darwin' and platform.machine() == 'arm64'
probe = repo / 'Library/ai/probe_wechat_lsda_20261017.py'
command = [sys.executable, str(probe), '0x667f534', '0x667fc38', '0x6678aa0',
           '0x66741ac', '0x66798bc']
result = subprocess.run(command, capture_output=True, text=True, timeout=10)
assert result.returncode == 0, result.stderr
metadata = json.loads(result.stdout)
with (output / 'unwind-lsda.json').open('x') as handle:
    json.dump(metadata, handle, indent=2)
    handle.write('\n')
records = {int(row['start'], 16): row for row in metadata['records']}
assert [row['end_exclusive'] for row in metadata['records']] == [
    '0x667fa1c', '0x667fd04', '0x6679088', '0x6674c80', '0x6679c10']
# Ranges come from __unwind_info, not decompiler function bodies.
ranges = [(start, int(row['end_exclusive'], 16)) for start, row in records.items()]
instructions, dumps = {}, []
for start, end in ranges:
    command = ['xcrun', 'llvm-objdump', '--disassemble',
               f'--start-address={hex(start)}', f'--stop-address={hex(end)}', str(binary)]
    run = subprocess.run(command, capture_output=True, text=True, timeout=20)
    assert run.returncode == 0, run.stderr
    raw = output / f'full-unwind-{start:x}.txt'
    with raw.open('x') as handle:
        handle.write(run.stdout)
    normalized, positions = [], []
    for line in run.stdout.splitlines():
        match = re.fullmatch(r'\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+(.+)', line)
        if not match:
            continue
        location = int(match[1], 16)
        word = int(match[2], 16).to_bytes(4, 'little')
        assert start <= location < end
        assert namespace['read_va'](location, 4) == word
        assembly = ' '.join(match[3].split(' <', 1)[0].split(';', 1)[0].split())
        instructions[location] = assembly
        positions.append(location)
        normalized.append(f'{hex(location)}\t{word.hex()}\t{assembly}')
    assert positions == list(range(start, end, 4))
    clean = output / f'full-unwind-{start:x}.asm'
    with clean.open('x') as handle:
        handle.write('\n'.join(normalized) + '\n')
    dumps.append({'file': str(clean.relative_to(root)), 'instructions': len(positions),
                  'sha256': hashlib.sha256(clean.read_bytes()).hexdigest()})
# Confirm exception coverage at actual call instructions, including absent cleanup.
coverage = []
for function, site, landing, action in (
    (0x667f534, 0x667f584, '0x667f61c', 7),
    (0x667fc38, 0x667fc94, '0x667fce4', 0),
    (0x667fc38, 0x667fcb4, None, 0),
    (0x667fc38, 0x667fcd0, None, 0),
    (0x6678aa0, 0x6678cd4, None, 0),
    (0x6678aa0, 0x6678d68, '0x6679074', 0),
    (0x66741ac, 0x6674bfc, '0x6674c40', 0),
    (0x66798bc, 0x6679950, None, 0),
):
    matches = [row for row in records[function]['call_sites']
               if int(row['start'], 16) <= site < int(row['end_exclusive'], 16)]
    assert len(matches) == 1 and matches[0]['landing_pad'] == landing
    assert matches[0]['action'] == action
    coverage.append({'function': hex(function), 'site': hex(site),
                     'landing_pad': landing, 'action': action})
checks = {
    0x667f620: 'cmp w1, #0x2', 0x667f624: 'b.ne 0x667f70c',
    0x667f62c: 'bl 0x714009c', 0x667f70c: 'cmp w1, #0x1',
    0x667f710: 'b.ne 0x667fa10', 0x667f718: 'bl 0x714009c',
    0x667f8ac: 'bl 0x668272c', 0x667f968: 'bl 0x668272c',
    0x667f96c: 'bl 0x71400b4', 0x667f988: 'bl 0x66823c4',
    0x667f994: 'b 0x667f594', 0x667fa14: 'bl 0x713f1d8',
    0x667fa18: 'bl 0x17050', 0x667fcd0: 'blr x8',
    0x667fd00: 'bl 0x713f1d8', 0x6679084: 'bl 0x713f1d8',
    0x6674c5c: 'bl 0x713f1d8',
    0x66741fc: 'cbnz w8, 0x6674404', 0x6674204: 'str w8, [x19, #0x288]',
    0x6674208: 'b 0x667468c', 0x6674404: 'tbnz x1, #0x3f, 0x66746b8',
}
for site, expected in checks.items():
    assert instructions[site] == expected, (hex(site), instructions.get(site), expected)
# Exact caught RTTIs are inferred from the 0x9b PC-relative indirect type table.
assert records[0x667f534]['type_table_address'] == '0x75dcd98'
assert [row['filter'] for row in records[0x667f534]['call_sites'][1]['action_chain']] == [2, 1, 0, 0]
slots, types = [], []
for number, pointer_slot, type_info, name_address, expected in (
    (1, 0x9b36a08, 0x9fb24e8, 0x9684d00, '_257f487b'),
    (2, 0x9b36a00, 0x9fb1c88, 0x9683a74, '_d0dea98e'),
):
    entry = 0x75dcd98 - 4 * number
    displacement, = struct.unpack('<i', namespace['read_va'](entry, 4))
    assert entry + displacement == pointer_slot
    row = namespace['decode_slot'](pointer_slot)
    assert row['decoded'] == hex(type_info)
    slots.append(row)
    row = namespace['decode_slot'](type_info + 8)
    # Apple arm64 libc++ typeinfo reserves the name pointer's high bit.
    assert int(row['decoded'], 16) == name_address | (1 << 63)
    slots.append(row)
    actual = namespace['read_va'](name_address, len(expected) + 1)
    assert actual == expected.encode() + b'\0'
    types.append({'filter': number, 'type_info': hex(type_info), 'name': expected})
assert namespace['read_va'](0x75dcd8c, 4) == bytes(4)
# Cross-reference imported calls using Mach-O indirect symbols, not nearby labels.
data = namespace['data']
cursor, symbol_sections = 32, []
for _ in range(struct.unpack_from('<I', data, 16)[0]):
    command, length = struct.unpack_from('<II', data, cursor)
    if command == 2:
        symbol_offset, _, strings_offset, _ = struct.unpack_from('<4I', data, cursor + 8)
    if command == 11:
        indirect_offset, _ = struct.unpack_from('<II', data, cursor + 56)
    if command == 0x19:
        for i in range(struct.unpack_from('<I', data, cursor + 64)[0]):
            start = cursor + 72 + i * 80
            address, size = struct.unpack_from('<QQ', data, start + 32)
            flags, first, stub_size = struct.unpack_from('<III', data, start + 64)
            kind = flags & 255
            if kind in (6, 7, 8):
                symbol_sections.append((address, size, first, stub_size if kind == 8 else 8))
    cursor += length
imports = []
for location, expected in (
    (0x714009c, '___cxa_begin_catch'), (0x71400b4, '___cxa_end_catch'),
    (0x713f1d8, '__Unwind_Resume'), (0x9b36c48, '___gxx_personality_v0'),
):
    address, size, first, stride = next(row for row in symbol_sections
                                      if row[0] <= location < row[0] + row[1])
    assert (location - address) % stride == 0
    symbol, = struct.unpack_from('<I', data, indirect_offset + 4 * (first + (location - address) // stride))
    string_index, = struct.unpack_from('<I', data, symbol_offset + 16 * symbol)
    start = strings_offset + string_index
    actual = data[start:data.index(b'\0', start)].decode()
    assert actual == expected, (hex(location), actual)
    imports.append({'address': hex(location), 'symbol': actual})
exports = []
for entry in ('17050', '668272c'):
    path = root / f'text-contract-pass260/native-fn-{entry}.asm'
    for line in path.read_text().splitlines():
        location, raw, assembly = line.split('\t', 2)
        assert namespace['read_va'](int(location, 16), len(bytes.fromhex(raw))) == bytes.fromhex(raw)
    exports.append({'file': str(path.relative_to(root)),
                    'instructions': len(path.read_text().splitlines()),
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
run260 = json.loads((root / 'text-contract-pass260/run.json').read_text())
assert run260['returncode'] == 0 and not run260['target_attached']
assert '-readOnly' in run260['args'] and '-noanalysis' in run260['args']
source = root / 'test_newsendmsg_job_finished_4115.cpp'
assembly = root / 'job_erasure_fixture_4115.S'
fixture = output / 'fixture'
command = ['clang++', '-std=c++17', '-Wall', '-Wextra', '-Werror', '-UNDEBUG', '-pthread',
           str(source), str(assembly), '-o', str(fixture)]
build = subprocess.run(command, capture_output=True, text=True, timeout=20)
with (output / 'build.json').open('x') as handle:
    json.dump({'args': command, 'returncode': build.returncode,
               'stdout': build.stdout, 'stderr': build.stderr}, handle, indent=2)
assert build.returncode == 0, build.stderr
run = subprocess.run([str(fixture)], capture_output=True, text=True, timeout=10)
with (output / 'run.json').open('x') as handle:
    json.dump({'returncode': run.returncode, 'stdout': run.stdout,
               'stderr': run.stderr}, handle, indent=2)
assert run.returncode == 0, (run.returncode, run.stderr)
expected = {'cases': 8, 'erased_bool_invoke': True, 'std_and_nonstd_caught': True,
            'first_failure_preserved': True, 'clone_lifetime_balanced': True,
            'concurrent_faults': 32, 'cleanup_after_final_fault': True,
            'native_scheduler_executed': False, 'sent': False}
assert json.loads(run.stdout) == expected
contract = {
    'binary_sha256': namespace['digest'], 'scope': 'Exception boundaries and owned final notification',
    'body_exception': {'call': '0x667f584', 'landing': '0x667f61c', 'caught_types': types,
                       'other_exception': 'resume unwinding at 0x667fa10',
                       'known_type_sequence': ['begin catch', 'conditional diagnostics',
                                               'group cancellation at 0x668272c', 'end catch',
                                               'group worker exit and return to normal disposal']},
    'final_exception': {'call': '0x667fcd0', 'local_landing_pad': None,
                        'core_entry_call': '0x6678cd4', 'core_entry_landing_pad': None,
                        'consequence': 'No local parameter cleanup on this propagation route; '
                                       'do not extrapolate normal return teardown to thrown callbacks.'},
    'cancel_state_zero': {'state_store': '0x6674204', 'return_branch': '0x6674208',
                           'cleanup_in_branch': False,
                           'constraint': 'Completion/state 3 is not proof of argument cleanup; '
                                         'actual executor ordering and later cleanup remain unproved.'},
    'owned_final_guard': {'header': 'newsendmsg_job_finished_4115.hpp',
                          'behavior': 'Preserve first exception without escape; keep shared error state.',
                          'scope': 'Owned final notification only; no native calls or throwing destructors.',
                          'not_for_job_body': 'Native typed coroutine-control exceptions must retain their route.'},
    'runtime_observed': False, 'callable_for_send': False,
    'remaining': ['Native executor identity/order and cancellation-before-entry cleanup',
                   'Full exception/cancellation paths and complete request/queue drain',
                   'Business-field closure, integrated native adapter and independent receipt'],
}
with (output / 'contract.json').open('x') as handle:
    json.dump(contract, handle, indent=2)
    handle.write('\n')
paths = [Path(__file__).resolve(), reader, probe,
         repo / 'Library/ai/inspect_wechat_unwind_20261017.py', source, assembly, stop,
         root / 'newsendmsg_job_finished_4115.hpp', root / 'newsendmsg_job_abi_4115.hpp',
         Path('/Library/Developer/CommandLineTools/SDKs/MacOSX26.4.sdk/usr/include/mach-o/compact_unwind_encoding.h'),
         Path('/Library/Developer/CommandLineTools/SDKs/MacOSX26.4.sdk/usr/include/mach-o/loader.h'),
         Path('/Library/Developer/CommandLineTools/SDKs/MacOSX26.4.sdk/usr/include/c++/v1/typeinfo')]
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'full_unwind_dumps': dumps,
    'instructions_matched': len(instructions), 'instruction_positions_checked': len(checks),
    'call_sites_checked': coverage, 'types': types, 'slots': slots, 'imports': imports,
    'extra_exports': exports, 'fixture': expected,
    'source_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    'artifact_sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in output.iterdir() if path.is_file()},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False,
    'limitations': 'Frozen exception metadata and owned host ABI fixture; no actual executor/drain/receipt.',
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: report[key] for key in (
    'passed', 'instructions_matched', 'instruction_positions_checked', 'types', 'fixture',
    'target_executed', 'callable_for_send', 'limitations')}))

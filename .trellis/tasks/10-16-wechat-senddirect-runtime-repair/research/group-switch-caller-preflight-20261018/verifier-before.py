"""Verify a concrete native group-switch producer; no target code is executed."""
from __future__ import annotations

import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
READER = REPO / 'Library/ai/verify_wechat_input_type_20261016.py'
UNWIND = REPO / 'Library/ai/inspect_wechat_unwind_20261017.py'
STOP = ROOT / 'account-safety-stop-20261016.md'


def digest(path: Path) -> str:
    """Hash one retained evidence file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert digest(READER) == '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'
assert digest(UNWIND) == '82cb22932b58299ac22e688d493402ebaffc4877a2b2af2d6d7de5e68db6fb4b'
assert digest(STOP) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
namespace = {'__file__': str(READER)}
exec(compile(READER.read_text().partition('rows, instructions = [], {}')[0],
             str(READER), 'exec'), namespace)
read_va = namespace['read_va']
sources = {READER, UNWIND, STOP, Path(__file__).resolve()}
groups = {418: ('2fc5d68',), 401: ('2fec684',), 400: ('46735dc',),
          398: ('4551eac',), 395: ('453df64',), 261: ('466ad74',),
          72: ('4669774',), 86: ('6684b8c',), 88: ('66846b8',), 390: ('2660d9c',)}
instructions, exports = {}, []
for number, entries in groups.items():
    folder = ROOT / f'text-contract-pass{number}'
    run = json.loads((folder / 'run.json').read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    sources.add(folder / 'run.json')
    for name in ('ghidra.log', 'script.log', 'headless-output.log'):
        path = folder / name
        assert 'REPORT SCRIPT ERROR' not in path.read_text()
        sources.add(path)
    for entry in entries:
        path = folder / f'native-fn-{entry}.asm'
        positions = []
        for line in path.read_text().splitlines():
            address, raw, assembly = line.split('\t', 2)
            site = int(address, 16)
            assert read_va(site, 4) == bytes.fromhex(raw), address
            instructions[site] = assembly
            positions.append(site)
        assert positions == list(range(int(entry, 16), positions[-1] + 4, 4)), entry
        exports.append({'file': str(path.relative_to(ROOT)), 'rows': len(positions)})
        sources.update((path, path.with_suffix('.c'), path.with_suffix('.refs.tsv')))
checks = {
    0x4669774: 'adrp x8,0xa45d000', 0x4669778: 'ldr x0,[x8, #0xf38]',
    0x466ad74: 'ldr x10,[x0, #0x290]', 0x466ad78: 'ldr x9,[x0, #0x298]',
    0x466ad7c: 'stp x10,x9,[x8]',
    0x2fc5dd8: 'bl 0x04669774', 0x2fc5ddc: 'add x8,sp,#0x118',
    0x2fc5de0: 'bl 0x0466ad74', 0x2fc5ea4: 'ldr x21,[sp, #0x118]',
    0x2fc5f50: 'ldr x20,[x21, #0x8]', 0x2fc5f60: 'add x21,sp,#0x148',
    0x2fc5f8c: 'fmov d0,xzr', 0x2fc5f90: 'str xzr,[sp, #0x188]',
    0x2fc5f94: 'mov v0.D[0x1],v0.D[0x0]', 0x2fc5f98: 'stur q0,[x21, #0x30]',
    0x2fc5fa8: 'add x8,sp,#0x160', 0x2fc5fac: 'str x8,[sp, #0x198]',
    0x2fc5fc0: 'str x20,[sp, #0x298]', 0x2fc6004: 'ldr x20,[sp, #0x298]',
    0x2fc6008: 'ldr x21,[sp, #0x198]', 0x2fc6034: 'mov w0,#0x110',
    0x2fc6040: 'adrp x8,0x9de0000', 0x2fc6044: 'add x8,x8,#0xc80',
    0x2fc6048: 'str x8,[x0], #0x8', 0x2fc6050: 'bl 0x02fec2dc',
    0x2fc605c: 'stp x9,x8,[x22, #0x100]',
    0x2fc6078: 'sub x8,x29,#0x98', 0x2fc607c: 'sub x2,x29,#0x88',
    0x2fc6080: 'mov x0,x20', 0x2fc6084: 'mov x1,x21',
    0x2fc6088: 'bl 0x06684b8c',
    0x6684c10: 'str xzr,[sp, #0x20]', 0x6684c1c: 'add x3,sp,#0x8',
    0x6684c20: 'bl 0x066846b8', 0x6684714: 'ldr x8,[x23, #0x18]',
    0x6684718: 'cbnz x8,0x06684720', 0x668471c: 'ldr x8,[x20, #0x120]',
    0x6684720: 'str x8,[sp, #0xe8]',
    0x2fec6b0: 'ldr x0,[x19, #0x10]', 0x2fec6c8: 'ldr x8,[x19, #0x8]',
    0x2fec6d4: 'bl 0x04669774', 0x2fec6d8: 'add x1,x19,#0x18',
    0x2fec6dc: 'bl 0x046735dc',
    0x4674abc: 'ldr x0,[sp, #0x78]', 0x4674ac0: 'sub x8,x29,#0xe0',
    0x4674ac4: 'mov x1,x19', 0x4674ac8: 'bl 0x04551eac',
    0x4551f7c: 'bl 0x04669774', 0x4551f80: 'sub x8,x29,#0x58',
    0x4551f84: 'bl 0x0466ad74', 0x4551f88: 'ldur x0,[x29, #-0x58]',
    0x4551f8c: 'sturb wzr,[x29, #-0x31]', 0x4551f90: 'sturb wzr,[x29, #-0x48]',
    0x4551f94: 'sub x1,x29,#0x48', 0x4551f98: 'bl 0x0453df64',
    0x453e198: 'bl 0x0668272c', 0x453e1a8: 'bl 0x066823c4',
    0x2660df0: 'bl 0x04669774', 0x2660df4: 'add x8,sp,#0x20',
    0x2660df8: 'bl 0x0466ad74', 0x2660e8c: 'ldr x21,[sp, #0x20]',
    0x2660ef8: 'mov x0,x21', 0x2660f00: 'bl 0x0453cce8',
}
for site, expected in checks.items():
    assert instructions[site].replace(' ', '') == expected.replace(' ', ''), (
        hex(site), instructions.get(site), expected)
branches = []
for site, expected in checks.items():
    kind = expected.split()[0]
    if kind not in ('bl', 'cbnz'):
        continue
    word, = struct.unpack('<I', read_va(site, 4))
    if kind == 'bl':
        assert word >> 26 == 0b100101
        width, immediate = 26, word & 0x3ffffff
    else:
        assert word & 0x7f000000 == 0x35000000
        width, immediate = 19, (word >> 5) & 0x7ffff
    delta = immediate - (1 << width) if immediate & (1 << (width - 1)) else immediate
    target = site + 4 * delta
    assert target == int(expected.split(',')[-1].split()[-1], 16)
    branches.append({'site': hex(site), 'target': hex(target)})
slot = namespace['decode_slot'](0x9de0c80 + 0x30)
assert slot['decoded'] == '0x2fec684'
# Recheck the immutable source chain backing the earlier configuration proof.
dependency = ROOT / 'scheduler-config-20261018/verification.json'
config = json.loads(dependency.read_text())
assert config['passed'] and config['binary_sha256'] == namespace['digest']
for name, expected in config['source_sha256'].items():
    path = REPO / name
    assert digest(path) == expected, name
sources.add(dependency)
seed_folder = ROOT / 'text-contract-pass417'
seed_run = json.loads((seed_folder / 'run.json').read_text())
assert seed_run['returncode'] == 0 and seed_run['target_attached'] is False
for name in ('run.json', 'ghidra.log', 'script.log', 'headless-output.log', 'callback-seeds.tsv'):
    path = seed_folder / name
    assert 'REPORT SCRIPT ERROR' not in path.read_text()
    sources.add(path)
assert '09de0c80\t02fc6048\tDATA\t02fc5d68' in (seed_folder / 'callback-seeds.tsv').read_text()
output = ROOT / 'group-switch-caller-20261018'
output.mkdir()
run = subprocess.run([sys.executable, str(UNWIND), '0x2fc5d68', '0x2fec684'],
                     capture_output=True, text=True, check=True, timeout=10)
unwind = json.loads(run.stdout)
assert unwind['binary_sha256'] == namespace['digest']
with (output / 'unwind.json').open('x') as handle:
    handle.write(run.stdout)
sources.add(output / 'unwind.json')
binary = Path(json.loads((ROOT / 'native-contract-run.json').read_text())['args'][1]).parent / 'wechat_arm64.dylib'
llvm_exports, all_positions = [], set(instructions)
for record in unwind['records']:
    start, end = int(record['start'], 16), int(record['end_exclusive'], 16)
    command = ['xcrun', 'llvm-objdump', '--disassemble', f'--start-address={hex(start)}',
               f'--stop-address={hex(end)}', str(binary)]
    run = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
    positions = []
    for line in run.stdout.splitlines():
        match = re.fullmatch(r'\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+(.+)', line)
        if match:
            site = int(match[1], 16)
            assert read_va(site, 4) == int(match[2], 16).to_bytes(4, 'little')
            positions.append(site)
    assert positions == list(range(start, end, 4))
    additional = len(set(positions) - all_positions)
    all_positions.update(positions)
    path = output / f'function-{start:x}.llvm.txt'
    with path.open('x') as handle:
        handle.write(run.stdout)
    sources.add(path)
    llvm_exports.append({'start': hex(start), 'end_exclusive': hex(end),
                         'rows': len(positions), 'additional_positions': additional,
                         'args': command})
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'ghidra_rows': sum(r['rows'] for r in exports), 'llvm_exports': llvm_exports,
    'unique_instruction_positions': len(all_positions), 'checked_sites': len(checks),
    'branches': branches, 'slots': [slot], 'dependency_source_hashes_verified': len(config['source_sha256']),
    'finding': 'A concrete activity-group cancellation caller is itself launched through the global service interface default group, with null executor configuration inherited from that group.',
    'scope': '0x2fc5d68 -> default-group job body 0x2fec684 -> 0x46735dc -> 0x4551eac -> 0x453df64',
    'limits': ['The global service/interface must remain the same instance and retain its configuration across selected accesses.',
               'Same configured executor is static provenance, not an observed runtime thread or coroutine identity.',
               'Caller binding does not alone prove the complete submission span cannot yield, pump, reenter or throw.',
               'No proof for every group-switch entry, full shutdown, external cancellation, final argument release or drain.',
               'Full business mapping, complete native adapter, real sending, independent receipt and deployment remain incomplete.'],
    'source_sha256': {str(path.relative_to(REPO)): digest(path) for path in sorted(sources)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False, 'deployed': False,
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: report[key] for key in ('passed', 'ghidra_rows', 'unique_instruction_positions',
                                             'checked_sites', 'dependency_source_hashes_verified')}))

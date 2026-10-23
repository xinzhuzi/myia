"""Verify selected text-job configuration provenance without target execution."""
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
    """Return the SHA-256 of a retained file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert digest(READER) == '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'
assert digest(UNWIND) == '82cb22932b58299ac22e688d493402ebaffc4877a2b2af2d6d7de5e68db6fb4b'
assert digest(STOP) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
namespace = {'__file__': str(READER)}
exec(compile(READER.read_text().partition('rows, instructions = [], {}')[0],
             str(READER), 'exec'), namespace)
read_va = namespace['read_va']
sources = {Path(__file__).resolve(), READER, UNWIND, STOP}
instructions, exports = {}, []
groups = {
    86: ('6684b8c',), 88: ('66846b8',), 89: ('667ddf8',), 97: ('2e0a888',),
    142: ('6681744',), 143: ('6681860',), 144: ('667e0e4',),
    146: ('667e734',), 147: ('667378c',), 148: ('667a110',),
    251: ('667a274',), 255: ('6677e1c',), 262: ('453c20c',),
    266: ('453b674',), 267: ('66845d0',), 278: ('453e264',),
    279: ('668467c',), 411: ('66734b4',), 412: ('66703f8',),
    413: ('6670560',), 415: ('d7cf04', '2d23bc0'),
}
for number, entries in groups.items():
    folder = ROOT / f'text-contract-pass{number}'
    path = folder / 'run.json'
    run = json.loads(path.read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    sources.add(path)
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
            assert read_va(site, 4) == bytes.fromhex(raw)
            assert site not in instructions or instructions[site] == assembly
            instructions[site] = assembly
            positions.append(site)
        expected_start = 0x453df64 if entry == '453e264' else int(entry, 16)
        assert positions[0] == expected_start
        assert positions == list(range(positions[0], positions[-1] + 4, 4))
        exports.append({'file': str(path.relative_to(ROOT)), 'rows': len(positions)})
        sources.update((path, path.with_suffix('.c'), path.with_suffix('.refs.tsv')))

output = ROOT / (sys.argv[1] if len(sys.argv) == 2 else 'scheduler-config-20261018')
assert output.parent == ROOT and output.name.startswith('scheduler-config-20261018')
output.mkdir()
selected = (0x453c20c, 0x66846b8, 0x667e0e4, 0x667378c,
            0x667a110, 0x667a274, 0x6677e1c, 0x453b674, 0x453df64)
run = subprocess.run([sys.executable, str(UNWIND), *map(hex, selected)],
                     capture_output=True, text=True, check=True, timeout=10)
unwind = json.loads(run.stdout)
assert unwind['binary_sha256'] == namespace['digest']
with (output / 'unwind.json').open('x') as handle:
    handle.write(run.stdout)
sources.add(output / 'unwind.json')
args = json.loads((ROOT / 'native-contract-run.json').read_text())['args']
binary = Path(args[1]).parent / 'wechat_arm64.dylib'
llvm_exports, all_positions = [], set(instructions)
for record in unwind['records']:
    start, end = int(record['start'], 16), int(record['end_exclusive'], 16)
    command = ['xcrun', 'llvm-objdump', '--disassemble', f'--start-address={hex(start)}',
               f'--stop-address={hex(end)}', str(binary)]
    run = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
    positions, rows = [], []
    for line in run.stdout.splitlines():
        match = re.fullmatch(r'\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+(.+)', line)
        if not match:
            continue
        site = int(match[1], 16)
        raw = int(match[2], 16).to_bytes(4, 'little')
        assert start <= site < end and read_va(site, 4) == raw
        positions.append(site)
        rows.append(f'{hex(site)}\t{raw.hex()}\t{match[3]}')
    assert positions == list(range(start, end, 4))
    added = set(positions) - all_positions
    all_positions.update(positions)
    for suffix, content in (('asm', '\n'.join(rows) + '\n'), ('llvm.txt', run.stdout)):
        path = output / f'function-{start:x}.{suffix}'
        with path.open('x') as handle:
            handle.write(content)
        sources.add(path)
    llvm_exports.append({'start': hex(start), 'end_exclusive': hex(end),
                         'args': command, 'rows': len(positions),
                         'additional_positions': len(added)})

checks = {
    0x453c2ec: 'fmov d0,xzr', 0x453c2f0: 'mov v0.D[0x1],v0.D[0x0]',
    0x453c2f4: 'str xzr,[sp, #0x48]', 0x453c2f8: 'stur q0,[sp, #0x38]',
    0x453c354: 'add x1,sp,#0x20', 0x453c358: 'add x2,sp,#0x60',
    0x453c360: 'mov x0,x20', 0x453c364: 'bl 0x06684b8c',
    0x6684c0c: 'mov x1,x19', 0x6684c20: 'bl 0x066846b8',
    0x66846d8: 'mov x23,x1', 0x66846dc: 'mov x20,x0',
    0x6684724: 'ldr x8,[x23, #0x20]', 0x6684728: 'cbnz x8,0x06684730',
    0x668472c: 'ldr x8,[x20, #0x128]', 0x6684730: 'str x8,[sp, #0xf0]',
    0x66847fc: 'add x0,sp,#0xd0', 0x668480c: 'bl 0x0667ddf8',
    0x667de0c: 'mov x2,x1', 0x667de10: 'mov x1,x0',
    0x667de20: 'bl 0x06681744', 0x6681768: 'mov x24,x1',
    0x66817a8: 'mov x2,x24', 0x66817b4: 'bl 0x06681860',
    0x6681878: 'mov x20,x1', 0x6681928: 'mov x0,x20',
    0x668192c: 'mov x1,x19', 0x6681930: 'bl 0x0667e0e4',
    0x667e10c: 'mov x26,x1', 0x667e110: 'mov x19,x0',
    0x667e2d4: 'add x8,x19,#0xf8', 0x667e2d8: 'ldur q0,[x26, #0x18]',
    0x667e2dc: 'ldur q1,[x26, #0x28]', 0x667e2e0: 'str q1,[x8, #0x10]',
    0x667e2e4: 'stur q0,[x19, #0xf8]',
    0x667e794: 'add x3,x19,#0xe0', 0x667e79c: 'bl 0x0667378c',
    0x667379c: 'mov x4,x3', 0x66737c0: 'bl 0x0667a110',
    0x667a128: 'mov x21,x4', 0x667a16c: 'mov x4,x21',
    0x667a170: 'bl 0x0667a274', 0x667a28c: 'mov x20,x4',
    0x667a290: 'mov x19,x0', 0x667a2a8: 'add x22,x0,#0x268',
    0x667a3d0: 'ldur q0,[x20, #0x18]', 0x667a3d4: 'str q0,[x22]',
    0x6677ff8: 'ldr x0,[x19, #0x270]', 0x6677ffc: 'cbz x0,0x066784e4',
    0x66784e4: 'bl 0x066734b4', 0x66784e8: 'str x0,[x19, #0x270]',
    0x66845f4: 'movi v0.2D,#0x0', 0x66845f8: 'stp q0,q0,[x19, #0x100]',
    0x66845fc: 'str q0,[x19, #0x120]', 0x6684600: 'str xzr,[x19, #0x130]',
    0x2e0a888: 'add x0,x0,#0x108', 0x2e0a88c: 'ret',
    0x453b940: 'bl 0x02e0a888', 0x453b944: 'str x20,[x0, #0x18]',
    0x453e260: 'bl 0x066845d0', 0x453e264: 'str x21,[x19, #0x10]',
    0x453e270: 'bl 0x0668467c', 0x453e27c: 'bl 0x02e0a888',
    0x453e280: 'str x20,[x0, #0x18]',
    0x668467c: 'str x1,[x0, #0x100]', 0x6684680: 'ret',
    0x6673538: 'mov w0,#0x80000', 0x667353c: 'mov x1,#0x0',
    0x6673540: 'bl 0x066703f8', 0x6670420: 'cmp x19,#0x0',
    0x6670424: 'csinv x8,x19,xzr,ne', 0x6670428: 'str x8,[x0, #0x10]',
    0x6670560: 'ldr x0,[x0, #0x10]', 0x6670564: 'ret',
    0xd7d148: 'bl 0x02e0a888', 0xd7d168: 'bl 0x02e0a888',
    0xd7d16c: 'ldrb w8,[x0, #0x17]', 0xd7d174: 'ldp x10,x11,[x0]',
    0x2d24140: 'add x0,x26,#0xe88', 0x2d24144: 'bl 0x02e0a888',
    0x2d2414c: 'ldr x19,[x22], #0x8', 0x2d24150: 'cmp x19,x22',
}
for site, expected in checks.items():
    assert instructions[site].replace(' ', '') == expected.replace(' ', ''), (
        hex(site), instructions.get(site), expected)
branches = []
for site, expected in checks.items():
    mnemonic = expected.split()[0]
    if mnemonic not in ('bl', 'cbz', 'cbnz'):
        continue
    word, = struct.unpack('<I', read_va(site, 4))
    if mnemonic == 'bl':
        assert word >> 26 == 0b100101
        width, immediate = 26, word & 0x3ffffff
    else:
        assert word & 0x7f000000 == (0x34000000 if mnemonic == 'cbz' else 0x35000000)
        width, immediate = 19, (word >> 5) & 0x7ffff
    delta = immediate - (1 << width) if immediate & (1 << (width - 1)) else immediate
    target = site + delta * 4
    assert target == int(expected.split(',')[-1].split()[-1], 16)
    branches.append({'site': hex(site), 'kind': mnemonic, 'target': hex(target)})
slot = namespace['decode_slot'](0x9fb2290 + 0x38)
assert slot['decoded'] == '0x6670560'
refs = ROOT / 'text-contract-pass97/native-fn-2e0a888.refs.tsv'
lines = refs.read_text().splitlines()
assert lines[0] == 'total\t7\toutput_limit\t64' and len(lines) == 8
sources.add(refs)
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'ghidra_rows_matched': sum(r['rows'] for r in exports), 'llvm_exports': llvm_exports,
    'unique_instruction_positions': len(all_positions), 'checked_sites': len(checks),
    'branch_decodes': branches, 'slots': [slot],
    'findings': [
        'Selected normal text launch explicitly zeroes request configuration word+0x20.',
        'Zero word+0x20 inherits directly from the selected group+0x128.',
        'Both default and new activity group constructors initialize group+0x128 to zero.',
        'Known interface setup writes the executor at config+0x18; parent storage at group+0x100 is separate.',
        'Config+0x20 copies through Job+0x100 to Core+0x270 with no default-provider selection there.',
        'Null Core+0x270 selects the per-thread default provider at resume/admission.',
        'The shown first-creation default provider stores and returns UINT64_MAX as its admission limit.',
        'Thus the unmodified constructed configuration does not supply a finite capacity limit.',
        'The two-instruction +0x108 accessor also appears with string and tree uses in other callers.',
    ],
    'limits': [
        'Constructor values do not prove the current mutable group, TLS object or executor identity.',
        'Accessor cross-references are bounded direct references, not an exhaustive alias/write analysis.',
        'Do not label every accessor caller a JobGroup config user solely from an identical offset.',
        'No live finite-limit occupancy, startup/cancel ordering, final argument release or leak observation.',
        'No complete business mapping, complete native adapter, send receipt or deployment proof.',
    ],
    'source_sha256': {str(path.relative_to(REPO)): digest(path) for path in sorted(sources)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False, 'deployed': False,
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: report[key] for key in (
    'passed', 'ghidra_rows_matched', 'unique_instruction_positions', 'checked_sites',
    'target_executed', 'target_attached', 'send_verified')}))

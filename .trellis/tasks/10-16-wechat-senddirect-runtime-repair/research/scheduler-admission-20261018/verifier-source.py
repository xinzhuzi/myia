"""Verify frozen coroutine admission and cancellation boundaries without target execution."""
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
    253: ('6677b20',), 254: ('66761cc', '66767e8'), 255: ('667637c',),
    256: ('66798bc',), 411: ('66734b4', '6676714'), 412: ('66703f8',),
    413: ('6670560', '667dcac'), 414: ('667da80', '667dad0', '667db24', '5037c'),
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
        assert positions == list(range(int(entry, 16), positions[-1] + 4, 4))
        exports.append({'file': str(path.relative_to(ROOT)), 'rows': len(positions)})
        sources.update((path, path.with_suffix('.c'), path.with_suffix('.refs.tsv')))

output = ROOT / (sys.argv[1] if len(sys.argv) == 2 else 'scheduler-admission-20261018')
assert output.parent == ROOT and output.name.startswith('scheduler-admission-20261018')
output.mkdir()
selected = (0x66734b4, 0x66703f8, 0x6670560, 0x6676714, 0x667dcac,
            0x667637c, 0x66761cc, 0x66767e8, 0x667db24, 0x5037c)
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
    0x6677b88: 'ldr x8,[x19, #0x20]!', 0x6677b94: 'ldr x1,[x8, #0x270]',
    0x6677b9c: 'bl 0x066767e8', 0x6677bb0: 'bl 0x066761cc',
    0x66761e4: 'ldr w8,[x19, #0x288]', 0x66761e8: 'cbz w8,0x0667627c',
    0x66761ec: 'cmp w8,#0x3', 0x66761f0: 'b.eq 0x06676334',
    0x6676254: 'bl 0x06677e1c', 0x6676280: 'stp x19,x8,[sp, #0x8]',
    0x6676290: 'ldadd x10,x9,[x9]', 0x667629c: 'ldp x9,x10,[x0, #0x28]',
    0x66762ac: 'stp x19,x8,[x9]', 0x66762dc: 'str x1,[x0, #0x28]',
    0x66762e4: 'ldr x0,[x0, #0x20]', 0x66762f4: 'bl 0x0667d508',
    0x6676328: 'mov x0,x19', 0x667632c: 'mov w1,#0x0',
    0x6676330: 'bl 0x0667637c', 0x6676344: 'ret',
    0x66763a4: 'ldr x8,[x0, #0x18]', 0x66763a8: 'ldr x9,[x0]',
    0x66763ac: 'cmp x8,x9', 0x66763b0: 'b.cs 0x06676658',
    0x66763bc: 'ldp x8,x1,[x0, #0x20]', 0x66763c4: 'b.eq 0x06676658',
    0x6676404: 'bl 0x0667d6b0', 0x6676440: 'str x8,[x20, #0x28]',
    0x66764b0: 'str x22,[x1, #0x20]', 0x66764dc: 'ldr x8,[x20, #0x18]',
    0x66764e0: 'add x8,x8,#0x1', 0x66764e4: 'str x8,[x20, #0x18]',
    0x66764ec: 'ldr w8,[x20, #0x288]', 0x66764f0: 'cmp w8,#0x3',
    0x66764f4: 'tbz w19,#0x0,0x06676574', 0x66764f8: 'b.eq 0x066765f8',
    0x66764fc: 'ldr x19,[x20, #0x268]', 0x6676530: 'stp x8,x20,[x0]',
    0x6676538: 'stp x22,x21,[x0, #0x10]', 0x6676544: 'ldr x8,[x8, #0x10]',
    0x6676554: 'blr x8', 0x6676574: 'b.eq 0x066765f8',
    0x66765d4: 'bl 0x06677e1c', 0x6676608: 'ldaddal x9,x8,[x8]',
    0x6676638: 'ldaddal x9,x8,[x8]', 0x6676684: 'ret',
    0x6676804: 'mov x21,x1', 0x6676808: 'mov x19,x0',
    0x667680c: 'mov x20,x8', 0x6676814: 'bl 0x066734b4',
    0x667685c: 'ldr x8,[x8, #0x38]', 0x6676860: 'mov x0,x21',
    0x6676864: 'blr x8', 0x6676868: 'mov x23,x0',
    0x6676894: 'str x23,[x25, #0x18]!',
    0x6676898: 'stp xzr,xzr,[x0, #0x30]',
    0x66768a4: 'str x9,[x0, #0x20]', 0x66768a8: 'stp xzr,xzr,[x0, #0x40]',
    0x66768ac: 'stp x25,x0,[x20]', 0x6676914: 'stp x21,x25,[x1, #0x20]',
    0x66734e8: 'add x0,x0,#0xe68', 0x6673538: 'mov w0,#0x80000',
    0x667353c: 'mov x1,#0x0', 0x6673540: 'bl 0x066703f8',
    0x6673564: 'stp x21,x0,[x20]', 0x6670404: 'mov x19,x1',
    0x6670418: 'add x8,x8,#0x290', 0x667041c: 'stp x8,x20,[x0]',
    0x6670420: 'cmp x19,#0x0', 0x6670424: 'csinv x8,x19,xzr,ne',
    0x6670428: 'str x8,[x0, #0x10]', 0x6670560: 'ldr x0,[x0, #0x10]',
    0x6670564: 'ret', 0x66767ac: 'ldr x9,[x0, #0x18]',
    0x66767b0: 'sub x9,x9,#0x1', 0x66767b4: 'str x9,[x0, #0x18]',
    0x66767d8: 'mov w1,#0x1', 0x66767e4: 'b 0x0667637c',
    0x6679944: 'ldr x8,[x19, #0x258]', 0x667994c: 'ldr x0,[x19, #0x260]',
    0x6679950: 'blr x8', 0x6679954: 'str xzr,[x19, #0x258]',
    0x66799a4: 'bl 0x066767e8', 0x66799b0: 'bl 0x06676714',
    0x667db34: 'ldr x19,[x0, #0x8]', 0x667db38: 'ldr w8,[x19, #0x288]',
    0x667db3c: 'cmp w8,#0x3', 0x667db40: 'b.eq 0x0667dbc8',
    0x667dba4: 'bl 0x06677e1c', 0x667dbd4: 'ret',
    0x667da8c: 'ldr x19,[x0, #0x10]', 0x667da9c: 'ldaddal x9,x8,[x8]',
    0x667dadc: 'ldr x19,[x0, #0x10]', 0x667daec: 'ldaddal x9,x8,[x8]',
    0x667db14: 'mov w1,#0x20', 0x667db20: 'b 0x0714000c',
    0x667dcc4: 'ldr x21,[x0, #0x38]', 0x667dccc: 'ldr x22,[x19, #0x40]',
    0x667dce4: 'sub x22,x22,#0x20', 0x667dcf0: 'ldur x20,[x22, #-0x18]',
    0x667dcfc: 'ldaddal x23,x8,[x8]', 0x667dd34: 'ldr x1,[x19, #0x28]',
    0x667dd38: 'add x0,x19,#0x20', 0x667dd4c: 'b 0x0005037c',
    0x5039c: 'bl 0x0005037c', 0x503a8: 'bl 0x0005037c',
    0x503b0: 'mov w1,#0x28', 0x503bc: 'b 0x0714000c',
}
for site, expected in checks.items():
    assert instructions[site].replace(' ', '') == expected.replace(' ', ''), (
        hex(site), instructions.get(site), expected)

branches = []
for site, expected in checks.items():
    mnemonic = expected.split()[0]
    if mnemonic not in ('b', 'bl', 'b.eq', 'b.cs', 'cbz', 'tbz'):
        continue
    word, = struct.unpack('<I', read_va(site, 4))
    if mnemonic in ('b', 'bl'):
        assert word >> 26 == (0b100101 if mnemonic == 'bl' else 0b000101)
        width, immediate = 26, word & 0x3ffffff
    elif mnemonic.startswith('b.'):
        assert word & 0xff000010 == 0x54000000
        assert word & 15 == {'b.eq': 0, 'b.cs': 2}[mnemonic]
        width, immediate = 19, (word >> 5) & 0x7ffff
    elif mnemonic == 'cbz':
        assert word & 0x7f000000 == 0x34000000
        width, immediate = 19, (word >> 5) & 0x7ffff
    else:
        assert word & 0x7f000000 == 0x36000000
        assert ((word >> 19) & 31) == 0 and word >> 31 == 0
        width, immediate = 14, (word >> 5) & 0x3fff
    delta = immediate - (1 << width) if immediate & (1 << (width - 1)) else immediate
    target = site + delta * 4
    assert target == int(expected.split(',')[-1].split()[-1], 16)
    branches.append({'site': hex(site), 'kind': mnemonic, 'target': hex(target)})
slots = []
for slot, target in ((0x9fb2290 + 0x38, 0x6670560), (0x9fb2b80 + 0x10, 0x667dcac),
                     (0x9fb2b00 + 0x20, 0x667da80), (0x9fb2b00 + 0x28, 0x667dad0),
                     (0x9fb2b00 + 0x30, 0x667db24)):
    row = namespace['decode_slot'](slot)
    assert row['decoded'] == hex(target)
    slots.append(row)

report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'ghidra_rows_matched': sum(row['rows'] for row in exports),
    'llvm_exports': llvm_exports, 'unique_instruction_positions': len(all_positions),
    'checked_sites': len(checks), 'branch_decodes': branches, 'slots': slots,
    'findings': [
        'Core+0x270, not executor+0x268, keys the per-thread scheduler map.',
        'Scheduler+0 is the key object slot+0x38 result; +0x18 counts admitted tree nodes.',
        'State-zero resumes retain a core pair in the pending heap before admission.',
        'Admission returns unchanged when unsigned admitted count is at least the stored limit.',
        'The null-key default object stores UINT64_MAX when its second constructor argument is zero.',
        'Thus the default limit is not evidence that ordinary sends encounter finite throttling.',
        'Admission inserts a raw core key before testing state 3; that state skips core resume.',
        'Readmission mode 1 submits an owned closure; its invoke also skips state 3.',
        'Native cleanup calls the argument cleaner before erasing the admitted tree key.',
        'Successful erasure decrements the count and requests one readmission in mode 1.',
        'Scheduler owner destruction releases pending core pairs and frees raw-key tree nodes.',
    ],
    'limits': [
        'No proof that the selected live send uses the default object or a finite custom limit.',
        'No actual gate occupancy, cancellation interleaving, resource leak or delivery observed.',
        'Dropping core references does not by itself prove release of the Job-owning core argument.',
        'Local state-3 skips do not exhaust all external listeners or indirect destructor effects.',
        'No ordering lease, state-zero final cleanup, complete adapter, send receipt or deployment proof.',
        'Unwind byte ranges can include adjacent leaf functions or exception tails; semantics remain bounded.',
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

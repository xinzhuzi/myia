"""Verify conditional text-auxiliary provenance against frozen ARM64 bytes."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
READER = REPO / 'Library/ai/verify_wechat_input_type_20261016.py'
STOP = ROOT / 'account-safety-stop-20261016.md'


def digest(path: Path) -> str:
    """Return the digest of one retained input."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert digest(READER) == '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'
assert digest(STOP) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
namespace = {'__file__': str(READER)}
prefix, separator, _ = READER.read_text().partition('rows, instructions = [], {}')
assert separator and "open('x')" not in prefix
exec(compile(prefix, str(READER), 'exec'), namespace)
read_va, decode_slot = namespace['read_va'], namespace['decode_slot']
output = ROOT / 'text-auxiliary-20261018'
output.mkdir(exist_ok=False)
sources = {READER, STOP, Path(__file__).resolve()}
groups = {
    126: ('ac6038',), 132: ('4cbbd20',), 157: ('30efce4',), 159: ('4cbcfd4',),
    222: ('f57630', '2a0cf30'), 230: ('4cbf820',), 231: ('4cbebac',),
    232: ('4a28ae8', '4a28ea8', '4a28ecc', '4a28f24', '4a290c4',
          '4a292d4', '4a29d84', '4a2bd4c'),
    233: ('4a292c4', '4a292e4', '4a2964c', '4a2965c', '4cbf3c0'),
    234: ('4cbf170',), 235: ('4cd949c',), 236: ('4ce9cd8',), 427: ('2652cc',),
}
instructions, exports = {}, []
for number, entries in groups.items():
    folder = ROOT / f'text-contract-pass{number}'
    run_path = folder / 'run.json'
    run = json.loads(run_path.read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    sources.add(run_path)
    for filename in ('ghidra.log', 'script.log', 'headless-output.log'):
        path = folder / filename
        assert 'REPORT SCRIPT ERROR' not in path.read_text()
        sources.add(path)
    for entry in entries:
        path = folder / f'native-fn-{entry}.asm'
        positions = []
        for line in path.read_text().splitlines():
            address, raw, assembly = line.split('\t', 2)
            address, raw = int(address, 16), bytes.fromhex(raw)
            assert len(raw) == 4 and read_va(address, 4) == raw
            assert address not in instructions or instructions[address] == assembly
            instructions[address] = assembly
            positions.append(address)
        assert positions[0] == int(entry, 16) and positions == sorted(set(positions))
        exports.append({'file': str(path.relative_to(ROOT)), 'instructions': len(positions),
                        'internal_gaps_half_open': [[hex(a + 4), hex(b)]
                                                   for a, b in zip(positions, positions[1:]) if b != a + 4]})
        sources.update((path, path.with_suffix('.c')))

checks = {
    0xac605c: 'movi v0.2D,#0x0', 0xac610c: 'stp q0,q0,[x19, #0x220]',
    0x30f0f14: 'ldr x0,[x20, #0x8]', 0x30f0f1c: 'ldr x8,[x8, #0x10]',
    0x30f0f20: 'blr x8', 0x30f0f24: 'mov x1,x0',
    0x30f0f28: 'mov x0,x21', 0x30f0f2c: 'bl 0x04cbbd20',
    0x30f0f4c: 'bl 0x04cbcfd4',
    0x4cbbd34: 'mov x20,x1', 0x4cbbd38: 'mov x19,x0',
    0x4cbbd58: 'str w20,[x19, #0xc]', 0x4cbbd5c: 'ldur x8,[x19, #0xc]',
    0x4cbbd60: 'str x8,[x19, #0x108]', 0x4cbbd64: 'mov x0,x19',
    0x4cbbd68: 'bl 0x04cbebac',
    0x4cbebc0: 'ldr x8,[x0, #0x220]', 0x4cbebc4: 'cbz x8,0x04cbebdc',
    0x4cbebd8: 'ret', 0x4cbebe0: 'bl 0x04a290c4',
    0x4cbec24: 'bl 0x04a29d84', 0x4cbecac: 'bl 0x04a28ecc',
    0x4cbecc8: 'bl 0x04a28ae8', 0x4cbecd4: 'bl 0x04a2bd4c',
    0x4cbed5c: 'bl 0x04a28f24', 0x4cbed8c: 'bl 0x04a28ea8',
    0x4cbedb8: 'bl 0x04a292d4', 0x4cbede8: 'bl 0x04a292c4',
    0x4cbee14: 'bl 0x04a2965c', 0x4cbee40: 'bl 0x04a292e4',
    0x4cbee44: 'cbz w0,0x04cbee68', 0x4cbee4c: 'bl 0x04cbf170',
    0x4cbee50: 'add x0,x19,#0x220', 0x4cbee58: 'bl 0x002652cc',
    0x4cbee6c: 'bl 0x04a2964c', 0x4cbee74: 'cbz w0,0x04cbee94',
    0x4cbee94: 'bl 0x04cbf3c0', 0x4cbee98: 'add x0,x19,#0x220',
    0x4cbeea0: 'bl 0x002652cc',
    0x2652d8: 'ldr q0,[x1]', 0x2652dc: 'stp xzr,xzr,[x1]',
    0x2652e0: 'ldr x19,[x0, #0x8]', 0x2652e4: 'str q0,[x0]',
    0x2652e8: 'cbz x19,0x0026531c', 0x265324: 'ret',
    0x4cbf248: 'adrp x8,0x9eb1000', 0x4cbf24c: 'add x8,x8,#0x640',
    0x4cbf250: 'add x8,x8,#0x10', 0x4cbf254: 'str x8,[x19, #0x18]',
    0x4cbf428: 'adrp x8,0x9eb0000', 0x4cbf42c: 'add x8,x8,#0xfd8',
    0x4cbf430: 'add x8,x8,#0x10', 0x4cbf438: 'str x8,[x21, #0x18]!',
    0xf578a8: 'ldr x8,[x20, #0x220]', 0xf578ac: 'str x8,[x19, #0x220]',
    0xf578b0: 'ldr x8,[x20, #0x228]', 0xf578b4: 'str x8,[x19, #0x228]',
    0xf578c4: 'ldadd x9,x8,[x8]',
    0x2a0d144: 'movi v0.2D,#0x0', 0x2a0d154: 'ldr q1,[x20, #0x220]',
    0x2a0d158: 'str q1,[x19, #0x220]', 0x2a0d15c: 'str q0,[x20, #0x220]',
    0x4cbcfd4: 'str w1,[x0, #0x10]', 0x4cbcffc: 'bl 0x04a29d84',
    0x4cbd000: 'cbz w0,0x04cbd00c',
    0x4cbf844: 'bl 0x04cbebac', 0x4cbf848: 'ldr x0,[x19, #0x220]',
    0x4cbf854: 'ldr x8,[x8, #0x10]', 0x4cbf85c: 'blr x8',
    0x4cd949c: 'ret', 0x4ce9cd8: 'ret',
}
for address, expected in checks.items():
    assert instructions.get(address) == expected, (hex(address), instructions.get(address), expected)

predicate_checks = {
    0x4a28aec: 'mov w9,#0x2710', 0x4a28af0: 'cmp w8,w9',
    0x4a28eac: 'cmp w8,#0x2f',
    0x4a28ed0: 'sub w9,w8,#0x2b', 0x4a28ed4: 'cmp w8,#0x3e',
    0x4a28ed8: 'ccmp w9,#0x2,#0x0,ne', 0x4a28edc: 'cset w0,cc',
    0x4a28f28: 'cmp w8,#0x22', 0x4a290c8: 'cmp w8,#0x3',
    0x4a290cc: 'ccmp w8,#0xd,#0x4,ne', 0x4a290d0: 'mov w9,#0x27',
    0x4a290d4: 'ccmp w8,w9,#0x4,ne', 0x4a290d8: 'cset w0,eq',
    0x4a292d8: 'cmp w8,#0x32', 0x4a29d88: 'cmp w8,#0x31',
    0x4a2bd50: 'mov w9,#0x2712', 0x4a2bd54: 'cmp w8,w9',
    0x4a292c8: 'cmp w8,#0x30', 0x4a29650: 'cmp w8,#0x23',
    0x4a29668: 'sub w10,w9,#0x2a', 0x4a2966c: 'cmp w10,#0x19',
    0x4a29670: 'lsl w10,w0,w10', 0x4a29674: 'and w10,w10,#0x3ffffff',
    0x4a29678: 'and w10,w10,#0xff000001',
    0x4a2967c: 'ccmp w10,#0x0,#0x4,ls', 0x4a29680: 'b.eq 0x04a29688',
    0x4a2968c: 'cmp w9,#0x31', 0x4a29690: 'mov w9,#0x32',
    0x4a29694: 'ccmp w8,w9,#0x0,eq', 0x4a29698: 'cset w0,eq',
}
for address, expected in predicate_checks.items():
    assert instructions.get(address) == expected, (hex(address), instructions.get(address), expected)

branches = []
for address, assembly in {**checks, **predicate_checks}.items():
    operation = assembly.split()[0]
    if operation not in ('bl', 'b', 'cbz', 'cbnz') and not operation.startswith('b.'):
        continue
    word = struct.unpack('<I', read_va(address, 4))[0]
    if operation in ('bl', 'b'):
        assert word & 0x7c000000 == 0x14000000
        bits, value = 26, word & 0x3ffffff
    else:
        assert word & 0x7e000000 == 0x34000000 or word & 0xff000010 == 0x54000000
        bits, value = 19, (word >> 5) & 0x7ffff
    value -= (1 << bits) if value & (1 << (bits - 1)) else 0
    target = address + value * 4
    assert target == int(assembly.split()[-1].split(',')[-1], 16)
    branches.append({'site': hex(address), 'target': hex(target), 'operation': operation})

slots = []
for slot, target in ((0x9eb0ff8, 0x4cd949c), (0x9eb1660, 0x4ce9cd8)):
    row = decode_slot(slot)
    assert int(row['decoded'], 16) == target
    assert read_va(target, 4) == bytes.fromhex('c0035fd6')
    slots.append(row)
for name in ('newsendmsg-record-database-contract.json', 'newsendmsg-record-input-contract.json',
             'newsendmsg-text-input-owner-contract.json'):
    path = ROOT / name
    assert json.loads(path.read_text())['binary_sha256'] == namespace['digest']
    sources.add(path)

report = {
    'binary_sha256': namespace['digest'], 'exports': exports,
    'distinct_instruction_positions_matched': len(instructions),
    'selected_instruction_checks': len(checks) + len(predicate_checks),
    'independently_decoded_control_transfers': branches, 'virtual_slots': slots,
    'reviewed_conditional_conclusion': {
        'record_low_type': 1,
        'initial_auxiliary_pair_empty': True,
        'setter_calls_prepare_after_type_write': True,
        'empty_prepare_result_payload_vtables': ['0x9eb1650', '0x9eb0fe8'],
        'nonempty_prepare_returns_without_replacement': True,
        'record_copy_retains_auxiliary_pair': True,
        'record_move_transfers_auxiliary_pair_and_clears_source': True,
        'selected_two_vtable_slot_0x10_methods_are_ret': True,
        'requires_no_unproved_intervening_replacement_or_vtable_mutation': True,
    },
    'limitations': [
        'This joins constructor/setter/prepare and copy/move contracts, not all intervening callees.',
        'Arbitrary pre-existing auxiliary objects have no established identity.',
        'No proof of whole-path recipient/body preservation, native coroutine/drain or adapter qualification.',
        'Byte coverage does not imply complete semantics; retained internal export gaps are listed.',
        'No target execution, native call, send, independent receipt or deployment.',
    ],
    'source_sha256': {str(path.relative_to(REPO)): digest(path) for path in sorted(sources)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'whole_path_content_preservation_proven': False, 'complete_adapter': False,
    'send_verified': False, 'deployed': False, 'full_objective_complete': False,
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'exports': len(exports), 'instruction_positions': len(instructions),
                  'selected_checks': report['selected_instruction_checks'],
                  'control_transfers': len(branches), 'slots': len(slots),
                  'source_hashes': len(sources), 'target_executed': False}))

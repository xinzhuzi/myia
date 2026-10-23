"""Verify frozen signal ownership and disposal; never execute the target."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
READER = REPO / 'Library/ai/verify_wechat_input_type_20261016.py'
STOP = ROOT / 'account-safety-stop-20261016.md'
assert hashlib.sha256(READER.read_bytes()).hexdigest() == (
    '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17')
assert hashlib.sha256(STOP.read_bytes()).hexdigest() == (
    'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d')
namespace = {'__file__': str(READER)}
exec(compile(READER.read_text().partition('rows, instructions = [], {}')[0],
             str(READER), 'exec'), namespace)
read_va = namespace['read_va']

SOURCES = {
    89: ('6682d18',), 144: ('667e0e4',), 150: ('667fd04',),
    251: ('668614c',), 252: ('668032c', '668037c', '66803d0'),
    258: ('6683134',), 402: ('668688c', '6686644', '6686680', '6686420'),
    404: ('66860b0', '6685fd0'),
}
exports, instructions = [], {}
source_paths = {Path(__file__).resolve(), READER, STOP}
for number, names in SOURCES.items():
    folder = ROOT / f'text-contract-pass{number}'
    run_path = folder / 'run.json'
    run = json.loads(run_path.read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    for flag in ('-log', '-scriptlog'):
        log = Path(run['args'][run['args'].index(flag) + 1])
        assert 'REPORT SCRIPT ERROR' not in log.read_text()
        source_paths.add(log)
    source_paths.add(run_path)
    for name in names:
        path = folder / f'native-fn-{name}.asm'
        rows = path.read_text().splitlines()
        for index, row in enumerate(rows):
            location, raw, assembly = row.split('\t', 2)
            address, expected = int(location, 16), bytes.fromhex(raw)
            assert len(expected) == 4 and address == int(name, 16) + index * 4
            assert read_va(address, 4) == expected
            assert address not in instructions or instructions[address] == assembly
            instructions[address] = assembly
        pseudo = path.with_suffix('.c')
        header = pseudo.read_text().splitlines()[1]
        assert header == f'// entry={int(name, 16):08x} end={int(name, 16) + len(rows) * 4 - 1:08x}'
        exports.append({'file': str(path.relative_to(ROOT)), 'instructions': len(rows)})
        source_paths.update((path, pseudo))

CHECKS = {
    0x66860cc: 'mov w0,#0xa0', 0x66860e4: 'str q0,[x0, #0x90]',
    0x6686118: 'strh wzr,[x19, #0x98]', 0x668611c: 'str x19,[x20, #0x8]',
    0x6686650: 'mov x19,x0', 0x6686654: 'bl 0x07141590',
    0x6686658: 'ldr x8,[x19, #0x90]', 0x668665c: 'cmp x8,x0',
    0x6686660: 'b.eq 0x06686668', 0x6686664: 'str x0,[x19, #0x90]',
    0x668666c: 'cset w0,ne',
    0x667fd24: 'mov x19,x1', 0x667fd28: 'mov x20,x0',
    0x667fd58: 'bl 0x0713fb14', 0x667fd60: 'bl 0x06686644',
    0x667fd64: 'tbz w0,#0x0,0x0667febc', 0x667fd94: 'bl 0x0668688c',
    0x667fdb8: 'str x19,[sp, #0x8]', 0x667fdbc: 'ldp x0,x9,[x8, #0x8]',
    0x667fdc0: 'add x1,x8,#0x18', 0x667fdc4: 'add x2,sp,#0x8',
    0x667fdc8: 'blr x9', 0x667fdd8: 'ldr x21,[x8, #0x40]',
    0x667fddc: 'cbz x21,0x0667fdb8', 0x667fdf8: 'ldp x27,x20,[x8, #0x48]',
    0x667fe08: 'ldadd x25,x9,[x9]', 0x667fe10: 'stp x28,x19,[sp, #0x60]',
    0x667fe18: 'mov w0,#0x68', 0x667fe3c: 'stp x27,x20,[x0, #0x48]',
    0x667fe48: 'ldadd x25,x8,[x8]', 0x667fe4c: 'stp x28,x19,[x0, #0x58]',
    0x667fe58: 'ldr x8,[x8, #0x10]', 0x667fe64: 'blr x8',
    0x668008c: 'bl 0x06686680', 0x66800a0: 'bl 0x0713fb20',
    0x66868dc: 'ldr w8,[x24, #0x38]', 0x66868e0: 'tbnz w8,#0x1,0x06686940',
    0x66868e4: 'mov w0,#0x60', 0x668690c: 'ldp x9,x8,[x24, #0x48]',
    0x6686910: 'stp x9,x8,[x0, #0x48]', 0x668691c: 'ldadd x22,x8,[x8]',
    0x6686940: 'and w9,w8,#0x3', 0x6686944: 'cmp w9,#0x1',
    0x6686950: 'str w8,[x24, #0x38]', 0x6686960: 'bl 0x06685fd0',
    0x66861dc: 'bl 0x0713fb14', 0x66861e4: 'ldr x9,[x8, #0x90]',
    0x66861e8: 'cbz x9,0x06686200', 0x66861f0: 'strb w9,[x8, #0x98]',
    0x66861f8: 'bl 0x0713fb20', 0x6686204: 'bl 0x0713fb20',
    0x6686698: 'ldrb w8,[x1, #0x98]', 0x66866a0: 'b.ne 0x06686724',
    0x66866b8: 'bl 0x0713fb20', 0x66866bc: 'strb wzr,[x20, #0x8]',
    0x66867bc: 'strb wzr,[x19, #0x99]', 0x66867c8: 'str xzr,[x19, #0x90]',
    0x66867e8: 'bl 0x0713fb38', 0x66867f4: 'mov w1,#0xa0',
    0x6686808: 'b 0x0714000c',
    0x6680338: 'ldr x19,[x0, #0x50]', 0x6680348: 'ldaddal x9,x8,[x8]',
    0x6680388: 'ldr x19,[x0, #0x50]', 0x6680398: 'ldaddal x9,x8,[x8]',
    0x66803c0: 'mov w1,#0x68', 0x66803d0: 'ldp x8,x3,[x0, #0x8]',
    0x66803d4: 'add x1,x0,#0x18', 0x66803d8: 'add x2,x0,#0x60',
    0x66803dc: 'mov x0,x8', 0x66803e0: 'br x3',
    0x668644c: 'stp x8,x4,[sp, #0x30]',
    0x668649c: 'stur q1,[x0, #0x38]', 0x66864a0: 'stp x22,x19,[x0, #0x48]',
}
for address, expected in CHECKS.items():
    assert instructions[address] == expected, (hex(address), instructions.get(address), expected)

branches = []
for address, assembly in CHECKS.items():
    mnemonic = assembly.split(' ', 1)[0]
    if mnemonic not in ('b', 'bl', 'b.eq', 'b.ne', 'cbz', 'tbnz', 'tbz'):
        continue
    word = int.from_bytes(read_va(address, 4), 'little')
    if mnemonic in ('b', 'bl'):
        assert word >> 26 == (0b100101 if mnemonic == 'bl' else 0b000101)
        bits, immediate = 26, word & 0x3ffffff
    elif mnemonic in ('tbnz', 'tbz'):
        assert word & 0x7f000000 == (0x37000000 if mnemonic == 'tbnz' else 0x36000000)
        bits, immediate = 14, (word >> 5) & 0x3fff
    else:
        if mnemonic.startswith('b.'):
            assert word & 0xff00001f == (0x54000000 if mnemonic == 'b.eq' else 0x54000001)
        else:
            assert word & 0x7f000000 == 0x34000000
        bits, immediate = 19, (word >> 5) & 0x7ffff
    immediate -= (1 << bits) if immediate & (1 << (bits - 1)) else 0
    target = address + immediate * 4
    assert target == int(assembly.rsplit('0x', 1)[1], 16)
    branches.append({'site': hex(address), 'target': hex(target)})


def resolve_stub_import(stub: int) -> dict:
    """Decode a three-instruction stub and its source-bound chained import."""
    first, load, branch = struct.unpack('<3I', read_va(stub, 12))
    assert first & 0x9f00001f == 0x90000010
    assert load & 0xffc003ff == 0xf9400210 and branch == 0xd61f0200
    delta = (((first >> 5) & 0x7ffff) << 2) | ((first >> 29) & 3)
    delta -= (1 << 21) if delta & (1 << 20) else 0
    slot = (stub & ~0xfff) + (delta << 12) + ((load >> 10) & 0xfff) * 8
    data, fixups, segments = namespace['data'], namespace['fixups'], namespace['segments']
    header = struct.unpack_from('<7I', data, fixups)
    assert header[0] == 0 and header[5:] == (1, 0)
    indices = [i for i, segment in enumerate(segments) if segment[0] <= slot < segment[0] + segment[3]]
    assert len(indices) == 1
    index = indices[0]
    starts = fixups + header[1]
    segment = starts + struct.unpack_from('<I', data, starts + 4 + index * 4)[0]
    _, page_size, fmt, base, _, pages = struct.unpack_from('<IHHQIH', data, segment)
    assert fmt == 6 and base == segments[index][0]
    page = (slot - base) // page_size
    assert page < pages
    first = struct.unpack_from('<H', data, segment + 22 + page * 2)[0]
    assert first != 0xffff and first & 0x8000 == 0
    chain = base + page * page_size + first
    for steps in range(page_size // 4):
        word = struct.unpack('<Q', read_va(chain, 8))[0]
        if chain == slot:
            break
        stride = ((word >> 51) & 0xfff) * 4
        assert stride and chain + stride <= slot
        chain += stride
    assert chain == slot and word >> 63 == 1 and (word >> 24) & 0xff == 0
    ordinal = word & 0xffffff
    assert ordinal < header[4]
    imported = struct.unpack_from('<I', data, fixups + header[2] + ordinal * 4)[0]
    start = fixups + header[3] + (imported >> 9)
    symbol = data[start:data.index(0, start)].decode('ascii')
    return {'stub': hex(stub), 'slot': hex(slot), 'symbol': symbol, 'chain_steps': steps + 1}


imports = [resolve_stub_import(stub) for stub in (0x7141590, 0x713fb14, 0x713fb20)]
assert [item['symbol'] for item in imports] == [
    '_pthread_self', '__ZNSt3__115recursive_mutex4lockEv', '__ZNSt3__115recursive_mutex6unlockEv']
slots = []
for offset, target in ((0x20, 0x668032c), (0x28, 0x668037c), (0x30, 0x66803d0)):
    row = namespace['decode_slot'](0x9fb2df8 + offset)
    assert row['decoded'] == hex(target)
    slots.append(row)

# The selected deferred invocation is exactly five instructions, with no flag recheck.
assert [instructions[address] for address in range(0x66803d0, 0x66803e4, 4)] == [
    'ldp x8,x3,[x0, #0x8]', 'add x1,x0,#0x18', 'add x2,x0,#0x60', 'mov x0,x8', 'br x3']
legacy = ROOT / 'core-teardown-20261017/contract.json'
legacy_contract = json.loads(legacy.read_text())
assert any('active dispatch count' in line for line in legacy_contract['base_cleanup'])
source_paths.add(legacy)
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'instructions_matched': sum(item['instructions'] for item in exports),
    'instruction_positions_checked': len(CHECKS), 'branch_decodes': branches,
    'imports': imports, 'closure_slots': slots,
    'correction': {'supersedes': str(legacy.relative_to(ROOT)) + ':base_cleanup[1]',
                   'signal_state_0x90': 'pthread_self value of the active emitting thread; not a count',
                   'signal_state_0x98': 'signal-state disposal requested during emission',
                   'signal_state_0x99': 'disabled registered nodes need sweeping'},
    'conclusions': [
        'The recursive mutex serializes the selected synchronous emit path.',
        'Same-thread recursive emission skips the listener snapshot and outer finish path.',
        'Destructor may defer the signal-state allocation disposal; this is not core argument cleanup.',
        'Snapshot copies retain receiver pairs independently of the registered nodes.',
        'The selected deferred closure owns a receiver pair but takes the Job as a raw pointer.',
        'Disconnection of a registered node cannot by itself revoke an already copied invocation.',
    ],
    'limits': [
        'Frozen normal paths, not exception, concurrency, runtime reachability or full drain proof.',
        'Listener member functions and receiver destructors can have other unproven effects.',
        'Global reference queries are truncated and do not enumerate the selected Job listener set.',
        'State-zero argument release, actual shutdown/start ordering and full adapter remain open.',
    ],
    'source_sha256': {str(path.relative_to(REPO)): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in sorted(source_paths)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False,
}
output = ROOT / 'signal-dispatch-20261018-verification.json'
with output.open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: value for key, value in report.items()
                  if key not in ('exports', 'source_sha256', 'conclusions', 'limits')}))

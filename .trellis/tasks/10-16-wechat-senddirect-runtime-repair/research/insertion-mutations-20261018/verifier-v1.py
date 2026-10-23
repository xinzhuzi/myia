"""Verify bounded insertion writes and copy domains against frozen ARM64 bytes."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TASK = REPO / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair'
ROOT = TASK / 'research'
READER = REPO / 'Library/ai/verify_wechat_input_type_20261016.py'
STOP = ROOT / 'account-safety-stop-20261016.md'


def digest(path: Path) -> str:
    """Hash an exact retained source."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signed(value: int, bits: int) -> int:
    """Sign extend an ARM64 branch displacement."""
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


assert digest(READER) == '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'
assert digest(STOP) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
namespace = {'__file__': str(READER)}
prefix, separator, _ = READER.read_text().partition('rows, instructions = [], {}')
assert separator
exec(compile(prefix, str(READER), 'exec'), namespace)
sources = {READER, STOP, Path(__file__).resolve()}
rows, exports, transfers = {}, [], []
for folder, function in (
    ('text-contract-pass229', '32961a4'), ('text-contract-pass228', '3269bec'),
    ('text-contract-pass230', '4cbf820'), ('text-contract-pass230', '4cbfb58'),
    ('text-contract-pass287', '4eafe18'), ('text-contract-pass429', '196dc'),
    ('text-contract-pass429', '4cbd748'), ('text-contract-pass429', '4d310bc'),
    ('text-contract-pass430', '4eae868'), ('text-contract-pass304', '4eae1b8'),
    ('text-contract-pass222', 'f57630'), ('text-contract-pass224', '4cbd624'),
):
    directory = ROOT / folder
    run = json.loads((directory / 'run.json').read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    sources.add(directory / 'run.json')
    for name in ('ghidra.log', 'script.log', 'headless-output.log'):
        path = directory / name
        assert 'REPORT SCRIPT ERROR' not in path.read_text()
        sources.add(path)
    source = directory / f'native-fn-{function}.asm'
    sources.update((source, source.with_suffix('.c')))
    positions = []
    for line in source.read_text().splitlines():
        address, raw, assembly = line.split('\t', 2)
        address, raw = int(address, 16), bytes.fromhex(raw)
        assert len(raw) == 4 and namespace['read_va'](address, 4) == raw
        word = struct.unpack('<I', raw)[0]
        assert address not in rows or rows[address] == (word, assembly)
        rows[address] = (word, assembly)
        positions.append(address)
        target = None
        if word & 0x7c000000 == 0x14000000:
            target = address + 4 * signed(word & 0x3ffffff, 26)
        elif word & 0xff000010 == 0x54000000 or word & 0x7e000000 == 0x34000000:
            target = address + 4 * signed((word >> 5) & 0x7ffff, 19)
        elif word & 0x7e000000 == 0x36000000:
            target = address + 4 * signed((word >> 5) & 0x3fff, 14)
        if target is not None:
            assert target == int(assembly.split()[-1].split(',')[-1], 16)
            transfers.append({'site': hex(address), 'target': hex(target)})
    assert positions[0] == int(function, 16)
    assert positions == list(range(positions[0], positions[-1] + 4, 4))
    exports.append({'file': str(source.relative_to(ROOT)), 'instructions': len(positions)})

checks = {
    0x32961c0: 'mov x20,x0', 0x32961d8: 'ldp x22,x0,[x0, #0x8]',
    0x3296210: 'ldp x22,x0,[x20, #0x8]', 0x3296240: 'ldp x22,x0,[x20, #0x8]',
    0x329626c: 'ldr x0,[x20, #0x8]', 0x3296274: 'bl 0x04cbf820',
    0x3296278: 'ldr x0,[x20, #0x8]', 0x329627c: 'bl 0x04cbfb58',
    0x329629c: 'ldr x1,[x20, #0x8]', 0x32962ac: 'bl 0x02e86b60',
    0x329631c: 'bl 0x03296b1c', 0x3296384: 'tbz w19,#0x0,0x032963ac',
    0x3296390: 'ldr x1,[x20, #0x8]', 0x3296398: 'b.ne 0x032963b0',
    0x329639c: 'ldr x8,[x1, #0x208]', 0x32963a0: 'ldr x8,[x8]',
    0x32963ac: 'ldr x1,[x20, #0x8]', 0x32963b8: 'bl 0x00f57630',
    0x32963f4: 'bl 0x00f57630', 0x3296408: 'bl 0x03263cd4',
    0x3269c08: 'mov x19,x1', 0x326a008: 'mov x0,x19',
    0x326a00c: 'bl 0x04cbd5f0', 0x4cbfb64: 'mov x19,x0',
    0x4cbfb68: 'add x0,x0,#0x190', 0x4cbfb6c: 'bl 0x04eafe18',
    0x4cbfb84: 'add x0,x19,#0x178', 0x4cbfb8c: 'bl 0x000196dc',
    0x4cbfbac: 'add x0,x19,#0x190', 0x4cbfbb8: 'b 0x05ab3f98',
    0x4eafe2c: 'mov x19,x0', 0x196f4: 'mov x19,x0',
    0x19760: 'bl 0x07140390', 0x19784: 'bl 0x07140390',
    0x1980c: 'stp x20,x24,[x19]', 0x19834: 'b 0x0714000c',
    0x4cbd77c: 'mov x19,x0', 0x4cbd788: 'ldr x8,[x8, #0x28]',
    0x4cbd78c: 'blr x8', 0x4cbd7c0: 'add x8,x19,#0x18',
    0x4cbd814: 'bl 0x07140e7c', 0x4cbd6d0: 'bl 0x04cbd748',
    0x4d310bc: 'stp x22,x21,[sp, #-0x30]!',
    0xf57874: 'add x0,x19,#0x190', 0xf57878: 'add x1,x20,#0x190',
    0xf5787c: 'bl 0x04eae868', 0x4eae874: 'mov x19,x0',
    0x4eae880: 'str x8,[x0]', 0x4eae8a4: 'bl 0x04eae1b8',
    0x4eae1c8: 'mov x19,x1', 0x4eae1cc: 'mov x20,x0',
    0xf5789c: 'ldadd x9,x8,[x8]', 0xf578c4: 'ldadd x9,x8,[x8]',
    0xf578e4: 'ldadd x9,x8,[x8]',
}
# The formatter's prologue is checked from its retained source below, not inferred ABI.
checks.pop(0x4d310bc)
for address, expected in checks.items():
    assert rows[address][1] == expected, (hex(address), rows[address][1], expected)

# Decode integer unsigned-immediate STR, rather than trusting printed offsets.
store_specs = [
    (0x3296208, 22, 0x204, 4, 'record presence'),
    (0x329620c, 22, 0x198, 4, 'record name number 1'),
    (0x3296238, 22, 0x204, 4, 'record presence'),
    (0x329623c, 22, 0x19c, 4, 'record name number 2'),
    (0x3296260, 22, 0x110, 4, 'record name number 3'),
    (0x3296270, 0, 0x218, 1, 'record insertion flag'),
    (0x32963a4, 1, 0xf4, 4, 'record local id conditional'),
    (0x326a0b8, 19, 0x100, 8, 'record time correction conditional'),
    (0x4cbf824, 0, 0x108, 8, 'record type mirror'),
    (0x4cbfba0, 19, 0x180, 8, 'record byte vector end'),
    (0x4eb0328, 19, 0x70, 4, 'metadata top cache equals record+0x200'),
    (0x4eaff98, 22, 0x14, 4, 'metadata+0x20 child cache'),
    (0x4eb001c, 22, 0x14, 4, 'metadata+0x20 child cache'),
    (0x4eb0158, 22, 0x10, 4, 'metadata+0x40 child cache'),
    (0x4eb01c4, 22, 0x10, 4, 'metadata+0x40 child cache'),
    (0x4eb023c, 22, 0xc, 4, 'metadata+0x48 child cache'),
    (0x4eb034c, 22, 0xc, 4, 'metadata+0x48 child cache'),
    (0x4eb02e4, 8, 0xc, 4, 'metadata+0x60 child cache'),
    (0x4eb031c, 8, 0xc, 4, 'metadata+0x68 child cache'),
    (0x19768, 19, 8, 8, 'vector end within capacity'),
    (0x19814, 19, 0x10, 8, 'vector capacity after allocation'),
    (0xf57884, 19, 0x208, 8, 'copied shared integer pointer'),
    (0xf5788c, 19, 0x210, 8, 'copied shared integer controller'),
    (0xf578ac, 19, 0x220, 8, 'copied aux pointer'),
    (0xf578b4, 19, 0x228, 8, 'copied aux controller'),
    (0xf578cc, 19, 0x230, 8, 'copied source aux pointer'),
    (0xf578d4, 19, 0x238, 8, 'copied source aux controller'),
]
stores = []
for address, base, offset, width, meaning in store_specs:
    word = rows[address][0]
    assert word & 0x3fc00000 == 0x39000000, hex(address)
    actual_width = 1 << (word >> 30)
    assert (word >> 5) & 31 == base
    assert actual_width == width and ((word >> 10) & 0xfff) * width == offset
    stores.append({'site': hex(address), 'base_register': f'x{base}',
                   'offset': hex(offset), 'width': width, 'domain': meaning})

# Compare only the selected original-record direct stores; no whole-callee inference.
protected = [(0xc, 0x14), (0x18, 0x60), (0x130, 0x148)]
for _, _, offset, width, _ in store_specs[:10]:
    assert all(offset + width <= begin or end <= offset for begin, end in protected)
# The comparison helper has no non-stack store instructions in its complete export.
comparison = ROOT / 'text-contract-pass429/native-fn-4cbd748.asm'
non_stack_stores = [line for line in comparison.read_text().splitlines()
                    if line.split('\t', 2)[2].startswith(('str', 'stur', 'stp'))
                    and '[sp' not in line and '[x29' not in line]
assert non_stack_stores == []
thunk_address = 0x4cbd5f0
thunk_word = struct.unpack('<I', namespace['read_va'](thunk_address, 4))[0]
assert thunk_word & 0xfc000000 == 0x14000000
assert thunk_address + 4 * signed(thunk_word & 0x3ffffff, 26) == 0x4cbd748

allocations = []
for offset, allocation, store, merge, target in (
    (0x10, 0x4eae588, 0x4eae5b0, 0x4eae3a4, 0x4ea6d78),
    (0x18, 0x4eae5d0, 0x4eae5fc, 0x4eae3cc, 0x4ea766c),
    (0x20, 0x4eae61c, 0x4eae63c, 0x4eae3f4, 0x4ea95e4),
    (0x28, 0x4eae65c, 0x4eae684, 0x4eae41c, 0x4ea9d08),
    (0x30, 0x4eae6a4, 0x4eae6cc, 0x4eae444, 0x4ea8b08),
    (0x38, 0x4eae6ec, 0x4eae714, 0x4eae46c, 0x4eaa904),
    (0x40, 0x4eae734, 0x4eae750, 0x4eae4b4, 0x4eab788),
    (0x48, 0x4eae770, 0x4eae784, 0x4eae4dc, 0x4eabd84),
    (0x58, 0x4eae7a4, 0x4eae7c4, 0x4eae520, 0x4eacbdc),
    (0x60, 0x4eae7e4, 0x4eae7fc, 0x4eae548, 0x4ead798),
    (0x68, 0x4eae81c, 0x4eae834, 0x4eae570, 0x4eadd14),
):
    assert rows[allocation][1] == 'bl 0x07140030'
    word = rows[store][0]
    assert word & 0xffc003ff == 0xf9000280  # STR x0,[x20,#imm12*8]
    assert ((word >> 10) & 0xfff) * 8 == offset
    assert rows[merge][1] == f'bl 0x{target:08x}'
    allocations.append({'offset': hex(offset), 'allocate': hex(allocation),
                        'install': hex(store), 'merge_call': hex(merge), 'merge_target': hex(target)})

# Revalidate the earlier provenance/order sources; do not rerun exclusive producers.
for name, expected in (
    ('text-prepare-order-20261018/verification.json',
     '62cca35cbc5c22eb07ffa0148dff9b76ee539f7d334f99114564b5c991b5d561'),
    ('database-record-outlets-20261018/verification.json',
     'ae39a85a20bf133b5f6f6b3997699e0a3138c869bf56861576ff8f00ad59931f'),
):
    path = ROOT / name
    assert digest(path) == expected
    sources.add(path)
    for relative, expected_hash in json.loads(path.read_text())['source_sha256'].items():
        source = REPO / relative
        assert digest(source) == expected_hash, relative
        sources.add(source)

output = ROOT / 'insertion-mutations-20261018'
output.mkdir(exist_ok=False)
report = {
    'binary_sha256': namespace['digest'], 'exports': exports,
    'distinct_instruction_positions_matched': len(rows), 'selected_checks': len(checks),
    'independently_decoded_transfers': transfers, 'independently_decoded_stores': stores,
    'comparison_thunk': {'site': hex(thunk_address), 'raw': struct.pack('<I', thunk_word).hex(),
                         'target': '0x4cbd748', 'non_stack_direct_stores': 0},
    'metadata_top_level_allocation_sites': allocations,
    'metadata_size_is_read_only': False, 'record_copy_is_fully_independent': False,
    'selected_original_record_direct_writes_overlap_type_names_or_body': False,
    'copy_domains': {
        'body_and_names': 'owned string copy branches; body proof retained in implementation82',
        'byte_vector': 'new allocation and memcpy for nonempty input',
        'metadata': 'new in-record object, zeroed, then merge; 11 nested top-level allocation branches',
        'shared_integer': 'pointer/controller copied and reference count incremented',
        'aux_and_source_aux': 'pointer/controller copied and reference count incremented',
    },
    'remaining_boundaries': [
        'Database vector consumers 0x3296b1c/0x3263cd4 may affect shared subobjects; full effects unproved.',
        'Nested metadata merge and size callees not exhaustively proved; valid object/allocator assumptions remain.',
        'Account getters/global aliases and arbitrary aux virtual effects not proved by absence of direct stores.',
        'Parent callees and subsequent queues, exceptions, races, scheduling and final release remain open.',
    ],
    'excluded_failed_export': 'text-contract-pass428: missing 0x prefixes; Java script error despite engine exit0',
    'limitations': 'Selected write/alias contracts, not full symbolic execution, reachability, nonalias or preservation proof.',
    'source_sha256': {str(path.relative_to(REPO)): digest(path) for path in sorted(sources)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'whole_path_content_preservation_proven': False, 'complete_adapter': False,
    'send_verified': False, 'deployed': False, 'full_objective_complete': False,
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'passed': True, 'positions': len(rows), 'checks': len(checks),
                  'stores': len(stores), 'transfers': len(transfers), 'allocations': len(allocations),
                  'source_hashes': len(sources), 'output': str(output.relative_to(REPO))}))

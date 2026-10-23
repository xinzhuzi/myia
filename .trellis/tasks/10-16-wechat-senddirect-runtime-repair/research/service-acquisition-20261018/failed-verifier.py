"""Qualify the selected frozen service getter and its local cleanup boundaries."""
from __future__ import annotations

import ast
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
LSDA = REPO / 'Library/ai/probe_wechat_lsda_20261017.py'
IMPORT_READER = REPO / 'Library/ai/verify_wechat_launch_span_20261018.py'
STOP = ROOT / 'account-safety-stop-20261016.md'


def sha256(path: Path) -> str:
    """Hash one exact retained file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path, expected in (
    (READER, '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17'),
    (UNWIND, '82cb22932b58299ac22e688d493402ebaffc4877a2b2af2d6d7de5e68db6fb4b'),
    (LSDA, 'f07c5d35f27a55f5923118d3ae9dc158ddb4bca940196eb7ad1f86ceb54995be'),
    (IMPORT_READER, '4cf2214a655badc3fa8037dc6f3c7e646e5f4086d0487a6403a323304a55eec9'),
    (STOP, 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'),
):
    assert sha256(path) == expected, str(path)
namespace = {'__file__': str(READER)}
exec(compile(READER.read_text().partition('rows, instructions = [], {}')[0],
             str(READER), 'exec'), namespace)
read_va = namespace['read_va']
output = ROOT / (sys.argv[1] if len(sys.argv) == 2 else 'service-acquisition-20261018')
assert output.parent == ROOT and output.name.startswith('service-acquisition-20261018')
output.mkdir()
sources = {Path(__file__).resolve(), READER, UNWIND, LSDA, IMPORT_READER, STOP}
instructions: dict[int, str] = {}
exports = []
groups = {
    490: ('268f370',),
    491: ('454182c', '4540bd8', '21b3684', '6676adc', '6676b84'),
    492: ('26c4024', '26c4070'),
    493: ('4541f78',),
    494: ('21b3484',),
    221: ('292d868',),
    220: ('292ef9c',),
}
for number, entries in groups.items():
    folder = ROOT / f'text-contract-pass{number}'
    run_path = folder / 'run.json'
    run = json.loads(run_path.read_text())
    assert run['returncode'] == 0 and run['target_attached'] is False
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    sources.add(run_path)
    for name in ('ghidra.log', 'script.log', 'headless-output.log'):
        path = folder / name
        assert 'REPORT SCRIPT ERROR' not in path.read_text()
        sources.add(path)
    for entry in entries:
        path = folder / f'native-fn-{entry}.asm'
        positions = []
        for row in path.read_text().splitlines():
            text, raw, assembly = row.split('\t', 2)
            pc, expected = int(text, 16), bytes.fromhex(raw)
            assert len(expected) == 4 and read_va(pc, 4) == expected
            assert pc not in instructions
            positions.append(pc)
            instructions[pc] = assembly
        assert positions == list(range(int(entry, 16), positions[-1] + 4, 4))
        sources.update((path, path.with_suffix('.c')))
        exports.append({'file': str(path.relative_to(ROOT)), 'rows': len(positions)})

builder = ROOT / 'text-job-field2-20261018/function-291fb70.asm'
positions = []
for row in builder.read_text().splitlines():
    text, raw, assembly = row.split('\t', 2)
    pc = int(text, 16)
    assert read_va(pc, 4) == bytes.fromhex(raw) and pc not in instructions
    positions.append(pc)
    instructions[pc] = assembly
assert positions == list(range(0x291fb70, 0x2921e1c, 4))
sources.add(builder)

selected = (0x268f370, 0x454182c, 0x4540bd8, 0x21b3684, 0x6676adc,
            0x6676b84, 0x26c4024, 0x26c4070, 0x4541f78, 0x21b3484)
run = subprocess.run([sys.executable, str(LSDA), *map(hex, selected)],
                     capture_output=True, text=True, check=True, timeout=15)
unwind = json.loads(run.stdout)
assert unwind['binary_sha256'] == namespace['digest'] and not unwind['target_executed']
with (output / 'unwind-lsda.json').open('x') as handle:
    handle.write(run.stdout)
sources.add(output / 'unwind-lsda.json')
args = json.loads((ROOT / 'native-contract-run.json').read_text())['args']
binary = Path(args[1]).parent / 'wechat_arm64.dylib'
llvm, covered = {}, set()
for record in unwind['records']:
    start, end = int(record['start'], 16), int(record['end_exclusive'], 16)
    if (start, end) in covered:
        continue
    covered.add((start, end))
    run = subprocess.run(['xcrun', 'llvm-objdump', '--disassemble',
                          f'--start-address={hex(start)}', f'--stop-address={hex(end)}',
                          str(binary)], capture_output=True, text=True, check=True, timeout=20)
    positions, rows = [], []
    for line in run.stdout.splitlines():
        match = re.fullmatch(r'\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+(.+)', line)
        if not match:
            continue
        pc = int(match[1], 16)
        raw = int(match[2], 16).to_bytes(4, 'little')
        assert start <= pc < end and read_va(pc, 4) == raw
        assembly = ' '.join(match[3].split(' <', 1)[0].split(';', 1)[0].split())
        positions.append(pc)
        llvm[pc] = assembly
        rows.append(f'{hex(pc)}\t{raw.hex()}\t{assembly}')
    assert positions == list(range(start, end, 4))
    for suffix, content in (('asm', '\n'.join(rows) + '\n'), ('llvm.txt', run.stdout)):
        path = output / f'function-{start:x}.{suffix}'
        with path.open('x') as handle:
            handle.write(content)
        sources.add(path)

checks = {
    # Getter ABI and both acquisition routes.
    0x268f380: 'mov x20,x0', 0x268f384: 'mov x19,x8',
    0x268f388: 'adrp x8,0x9da2000', 0x268f38c: 'add x8,x8,#0x0',
    0x268f3a4: 'bl 0x0454182c', 0x268f3b0: 'add x0,sp,#0x10',
    0x268f3b4: 'bl 0x06676adc', 0x268f3b8: 'ldrb w8,[sp, #0x38]',
    0x268f3bc: 'cmp w8,#0x1', 0x268f3c0: 'b.ne 0x0268f414',
    0x268f3c8: 'bl 0x066856fc', 0x268f3d0: 'bl 0x021b3684',
    0x268f3d4: 'ldp x8,x20,[x0]', 0x268f3e4: 'ldadd x10,x11,[x9]',
    0x268f3e8: 'stp x8,x20,[x19]', 0x268f420: 'sub x1,x29,#0x18',
    0x268f424: 'mov x0,x20', 0x268f428: 'bl 0x04540bd8',
    0x268f430: 'stp x9,x8,[x19]', 0x268f440: 'ldadd x9,x8,[x8]',
    0x268f480: 'bl 0x06676b84',
    # Pending registry lookup returns an optional future, not the service pair.
    0x4541844: 'mov x20,x0', 0x4541848: 'mov x19,x8',
    0x4541850: 'ldr x8,[x8, #0x10]', 0x4541858: 'blr x8',
    0x45418c8: 'add x0,x20,#0x28', 0x45418d0: 'bl 0x02aea564',
    0x45418e0: 'ldp x9,x8,[x0, #0x28]',
    0x45418e4: 'stp x9,x8,[x19]', 0x45418f4: 'ldadd x9,x8,[x8]',
    0x45418f8: 'ldr x8,[x0, #0x38]', 0x4541930: 'strb w8,[x19, #0x18]',
    # Synchronous lookup may itself wait; no ordinary-stack fallback guarantee.
    0x4540bf4: 'mov x20,x1', 0x4540bf8: 'mov x21,x0',
    0x4540bfc: 'mov x19,x8', 0x4540c94: 'bl 0x04541d70',
    0x4540cac: 'ldp x9,x8,[x0, #0x28]',
    0x4540cc8: 'ldr x9,[x8, #0x20]', 0x4540ccc: 'mov x1,sp',
    0x4540cd0: 'mov x8,x19', 0x4540cd4: 'mov x0,x20',
    0x4540cd8: 'blr x9', 0x4540d24: 'stp x8,x21,[x0]',
    0x4540d28: 'stp x22,x20,[x0, #0x10]',
    0x4540d3c: 'bl 0x0666ab58', 0x4540d6c: 'bl 0x066856fc',
    0x4540d74: 'bl 0x021b3684',
    # Descriptor key and the actual shared-pair copy method.
    0x26c4024: 'adrp x8,0x9ded000', 0x26c4028: 'add x8,x8,#0x300',
    0x26c402c: 'ldr x8,[x8, #0x8]',
    0x26c4030: 'and x0,x8,#0x7fffffffffffffff',
    0x26c4070: 'ldp x10,x9,[x1]', 0x26c4080: 'ldadd x12,x11,[x11]',
    0x26c4084: 'stp x10,x9,[x8]',
    # Typed future access checks its own exact RTTI, then returns payload+8.
    0x21b3694: 'bl 0x0666a844', 0x21b36c4: 'adrp x9,0x87d0000',
    0x21b36c8: 'add x9,x9,#0x270', 0x21b36dc: 'bl 0x07141998',
    0x21b36e8: 'adds x0,x8,#0x8', 0x21b371c: 'bl 0x07140108',
    # Current-core guard owns a promoted pair; zero TLS is not a safe context.
    0x6676aec: 'adrp x0,0xa24d000', 0x6676af0: 'add x0,x0,#0xe80',
    0x6676afc: 'ldr x8,[x0]', 0x6676b00: 'cbz x8,0x06676b50',
    0x6676b10: 'bl 0x0713fc28', 0x6676b18: 'stp x20,x0,[x19]',
    0x6676b50: 'stp xzr,xzr,[x19]', 0x6676b54: 'ldr x8,[x19]',
    0x6676b58: 'ldr w9,[x8, #0x288]',
    0x6676b64: 'ldr w9,[x8, #0x3c8]',
    0x6676b68: 'add w9,w9,#0x1', 0x6676b6c: 'str w9,[x8, #0x3c8]',
    0x6676b84: 'ldr x8,[x0]', 0x6676b88: 'ldr w9,[x8, #0x288]',
    0x6676b98: 'sub w9,w9,#0x1', 0x6676b9c: 'str w9,[x8, #0x3c8]',
    0x6676bac: 'ldr x19,[x0, #0x8]', 0x6676bbc: 'ldaddal x9,x8,[x8]',
    # Builder keeps the result pair separately from input and call_id.
    0x2920bc0: 'add x8, sp, #0x88', 0x2920bc4: 'bl 0x268f370',
    0x2920bd8: 'ldr x8, [sp, #0x88]', 0x2920bdc: 'cbz x8, 0x29211d4',
    0x29216cc: 'ldp x9, x8, [sp, #0x88]',
    0x29216d0: 'stp x9, x8, [sp, #0x58]',
    0x29216e0: 'ldadd x9, x8, [x8]', 0x29216ec: 'bl 0x292d868',
    0x292d8f8: 'ldur q0,[x21, #0x58]', 0x292d8fc: 'str q0,[x19, #0x60]',
    0x292d900: 'stp xzr,xzr,[x21, #0x58]',
    0x292efe0: 'ldr x0,[x0, #0x60]', 0x292f008: 'bl 0x0317ded4',
    # Optional-future cleanup does not itself cancel a job or drain a queue.
    0x21b3484: 'ldrb w8,[x0, #0x18]', 0x21b3488: 'cmp w8,#0x1',
    0x21b349c: 'ldr x19,[x0, #0x8]',
    0x21b34ac: 'ldaddal x9,x8,[x8]', 0x21b34cc: 'bl 0x0713fc1c',
}
for pc, expected in checks.items():
    assert ''.join(instructions[pc].split()) == ''.join(expected.split()), (
        hex(pc), instructions[pc], expected)
# Ghidra omitted these cleanup landing pads; check recovered LLVM separately.
tail_checks = {
    0x268f4d0: 'b 0x268f4d4', 0x268f4d4: 'mov x19, x0',
    0x268f4d8: 'add x0, sp, #0x10', 0x268f4dc: 'bl 0x6676b84',
    0x268f4e0: 'b 0x268f4e8', 0x268f4e4: 'mov x19, x0',
    0x268f4e8: 'add x0, sp, #0x20', 0x268f4ec: 'bl 0x21b3484',
    0x268f4f0: 'mov x0, x19', 0x268f4f4: 'bl 0x713f1d8',
}
for pc, expected in tail_checks.items():
    assert llvm[pc] == expected, (hex(pc), llvm[pc], expected)

branches = []
for pc, assembly in {**instructions, **{p: llvm[p] for p in tail_checks}}.items():
    mnemonic = assembly.split()[0]
    if mnemonic not in ('b', 'bl', 'cbz', 'cbnz', 'tbz', 'tbnz') and not mnemonic.startswith('b.'):
        continue
    target = int(assembly.replace(',', ' ').split()[-1], 16)
    word, = struct.unpack('<I', read_va(pc, 4))
    if mnemonic in ('b', 'bl'):
        assert word & 0x7c000000 == 0x14000000
        immediate, bits = word & 0x3ffffff, 26
    elif mnemonic.startswith('b.'):
        assert word & 0xff000010 == 0x54000000
        immediate, bits = (word >> 5) & 0x7ffff, 19
    elif mnemonic in ('cbz', 'cbnz'):
        assert word & 0x7e000000 == 0x34000000
        immediate, bits = (word >> 5) & 0x7ffff, 19
    else:
        assert word & 0x7e000000 == 0x36000000
        immediate, bits = (word >> 5) & 0x3fff, 14
    if immediate & (1 << (bits - 1)):
        immediate -= 1 << bits
    assert pc + 4 * immediate == target, hex(pc)
    branches.append({'site': hex(pc), 'target': hex(target)})

slots = []
for slot, expected in ((0x9da2010, 0x26c4024), (0x9da2020, 0x26c4070),
                       (0x9ded308, 0x80000000088bc050), (0x9e870d8, 0x4541f78)):
    decoded = namespace['decode_slot'](slot)
    assert int(decoded['decoded'], 16) == expected
    slots.append(decoded)
assert read_va(0x88bc050, 10) == b'_3d834e75\0'
assert read_va(0x87d0270, 10) == b'_62250804\0'
# Reuse exactly one reviewed read-only import decoder, excluding its producer.
function, = [node for node in ast.parse(IMPORT_READER.read_text()).body
             if isinstance(node, ast.FunctionDef) and node.name == 'bound_import']
module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
import_namespace = {'namespace': namespace, 'read_va': read_va, 'struct': struct}
exec(compile(module, str(IMPORT_READER), 'exec'), import_namespace)
imports = [import_namespace['bound_import'](address, symbol) for address, symbol in (
    (0x713fc28, '__ZNSt3__119__shared_weak_count4lockEv'),
    (0x713fc1c, '__ZNSt3__119__shared_weak_count14__release_weakEv'),
    (0x7141998, '_strcmp'), (0x713f1d8, '__Unwind_Resume'),
)]
getter_record, = [row for row in unwind['records'] if row['pc'] == '0x268f370']
assert getter_record['end_exclusive'] == '0x268f4f8'
assert getter_record['lsda_address'] == '0x7364e58'
exception_calls = []
for pc, expected in ((0x268f3b4, '0x268f4e4'), (0x268f3c8, '0x268f4d4'),
                     (0x268f3d0, '0x268f4d4'), (0x268f428, '0x268f4d0')):
    entry, = [row for row in getter_record['call_sites']
              if int(row['start'], 16) <= pc < int(row['end_exclusive'], 16)]
    assert entry['landing_pad'] == expected and entry['action'] == 0
    exception_calls.append({'site': hex(pc), **entry})

findings = {
    'getter_abi': 'x0=registry, hidden x8=owned shared-pair result',
    'descriptor_key': '_3d834e75',
    'pending_result_type': '_62250804',
    'current_core_guard': 'unconditional 0x6676adc before optional pending-result branch',
    'no_current_core_path': 'zero pair at 0x6676b50, then unconditional core+0x288 load',
    'normal_local_release': '0x6676b84 releases guard; optional future released separately',
    'selected_exception_local_release': 'post-guard wait/getter/fallback pads release guard, then optional future, then resume unwind',
    'guard_constructor_failure': 'landing pad releases optional future; no completed guard to release',
    'service_capture': 'builder sp+0x88 -> capture source+0x58 -> body+0x60; shared ownership retained',
    'scope': 'valid objects, completed guard construction and normally returning cleanup; selected local call sites only',
}
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'ghidra_and_builder_positions': len(instructions),
    'complete_unwind_ranges': len(covered), 'llvm_positions': len(llvm),
    'distinct_instruction_positions_matched': len(set(instructions) | set(llvm)),
    'exact_checks': len(checks) + len(tail_checks), 'branches': branches,
    'slots': slots, 'imports': imports, 'exception_calls': exception_calls,
    'findings': findings,
    'native_thread_identity_verified': False, 'state_zero_final_cleanup_verified': False,
    'complete_native_scheduling_and_drain_verified': False,
    'whole_path_field_preservation_proven': False, 'complete_adapter_verified': False,
    'runtime_observed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False, 'full_goal_complete': False,
    'remaining': [
        'Actual admission, service lifetime across shutdown and external group cancellation',
        'State-zero final parameter release and all queue/listener/weak-owner drain',
        'Full business-field preservation and complete native adapter',
        'Real send, independent receipt and deployment; account stop remains in effect',
    ],
    'source_sha256': {str(p.relative_to(REPO)): sha256(p) for p in sorted(sources)},
}
with (output / 'verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: report[key] for key in (
    'passed', 'ghidra_and_builder_positions', 'complete_unwind_ranges', 'llvm_positions',
    'distinct_instruction_positions_matched', 'exact_checks', 'full_goal_complete')}
    | {'branches': len(branches), 'source_hashes': len(sources)}))

"""Qualify bounded group-switch/shutdown callers without executing the target."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
root = repo / '.trellis/tasks/10-16-wechat-senddirect-runtime-repair/research'
reader = repo / 'Library/ai/verify_wechat_input_type_20261016.py'
assert hashlib.sha256(reader.read_bytes()).hexdigest() == (
    '3b08942b05af737f6b331974629526caaae98acd04d09571b361a044e55f2f17')
namespace = {'__file__': str(reader)}
exec(compile(reader.read_text().partition('rows, instructions = [], {}')[0],
             str(reader), 'exec'), namespace)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


instructions, exports = {}, []
sources = {72: (('4669774', 12),), 261: (('466ad74', 32),),
           395: (('453df64', 1260),), 398: (('4551eac', 1000), ('4671338', 1212)),
           400: (('46735dc', 6500), ('2c976c', 7048)),
           401: (('2fec684', 304), ('1986c', 4))}
for number, entries in sources.items():
    folder = root / f'text-contract-pass{number}'
    run_path = folder / 'run.json'
    run = json.loads(run_path.read_text())
    assert run['returncode'] == 0 and not run['target_attached']
    assert '-readOnly' in run['args'] and '-noanalysis' in run['args']
    assert '-import' not in run['args']
    logs = []
    for flag in ('-log', '-scriptlog'):
        log = Path(run['args'][run['args'].index(flag) + 1])
        assert 'REPORT SCRIPT ERROR' not in log.read_text()
        logs.append({'file': str(log.relative_to(root)), 'sha256': digest(log)})
    for entry, size in entries:
        path = folder / f'native-fn-{entry}.asm'
        rows = path.read_text().splitlines()
        assert len(rows) * 4 == size, (entry, len(rows), size)
        for index, row in enumerate(rows):
            address, raw, assembly = row.split('\t', 2)
            site, expected = int(address, 16), bytes.fromhex(raw)
            assert site == int(entry, 16) + index * 4 and len(expected) == 4
            assert namespace['read_va'](site, 4) == expected
            instructions[site] = assembly
        exports.append({'file': str(path.relative_to(root)), 'instructions': len(rows),
                        'sha256': digest(path), 'pseudocode_sha256': digest(path.with_suffix('.c')),
                        'run_sha256': digest(run_path), 'logs': logs})
checks = {
    0x4551ec4: 'mov x20,x1', 0x4551ec8: 'mov x19,x8',
    0x4551ecc: 'str x0,[sp, #0x8]', 0x4551f7c: 'bl 0x04669774',
    0x4551f80: 'sub x8,x29,#0x58', 0x4551f84: 'bl 0x0466ad74',
    0x4551f88: 'ldur x0,[x29, #-0x58]',
    0x4551f8c: 'sturb wzr,[x29, #-0x31]', 0x4551f90: 'sturb wzr,[x29, #-0x48]',
    0x4551f94: 'sub x1,x29,#0x48', 0x4551f98: 'bl 0x0453df64',
    0x453e198: 'bl 0x0668272c', 0x453e1a4: 'bl 0x066823c4',
    0x453e1bc: 'str xzr,[x19, #0x10]',
    0x46735fc: 'mov x19,x1', 0x4674abc: 'ldr x0,[sp, #0x78]',
    0x4674ac0: 'sub x8,x29,#0xe0', 0x4674ac4: 'mov x1,x19',
    0x4674ac8: 'bl 0x04551eac', 0x4674af0: 'bl 0x066856fc',
    0x4674af8: 'bl 0x0666a844', 0x2fec6d8: 'add x1,x19,#0x18',
    0x2fec6dc: 'bl 0x046735dc', 0x2cb048: 'bl 0x04671338',
    0x46714a0: 'bl 0x046698d0', 0x1986c: 'b 0x002c976c',
}
for site, expected in checks.items():
    assert instructions[site] == expected, (hex(site), instructions.get(site), expected)
branches = []
for site, target in {0x4551f7c: 0x4669774, 0x4551f84: 0x466ad74,
                     0x4551f98: 0x453df64, 0x453e198: 0x668272c,
                     0x453e1a4: 0x66823c4, 0x4674ac8: 0x4551eac,
                     0x4674af0: 0x66856fc, 0x4674af8: 0x666a844,
                     0x2fec6dc: 0x46735dc, 0x2cb048: 0x4671338,
                     0x46714a0: 0x46698d0, 0x1986c: 0x2c976c}.items():
    word = struct.unpack('<I', namespace['read_va'](site, 4))[0]
    assert word >> 26 == (0b000101 if site == 0x1986c else 0b100101)
    delta = word & 0x3ffffff
    delta -= (1 << 26) if delta & (1 << 25) else 0
    assert site + delta * 4 == target
    branches.append({'site': hex(site), 'target': hex(target)})
stop = root / 'account-safety-stop-20261016.md'
assert digest(stop) == 'b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d'
report = {
    'passed': True, 'binary_sha256': namespace['digest'], 'exports': exports,
    'instructions_matched': sum(item['instructions'] for item in exports),
    'instruction_positions_checked': len(checks), 'branch_decodes': branches,
    'findings': [
        '0x4551eac ordinary inputs are x0 owner and x1 copied options; shared result is hidden x8.',
        '0x4551eac fetches global service/interface then calls group switch with an empty name.',
        'Selected empty-name group path cancels, waits, destroys and clears the active group.',
        '0x2fec684 -> 0x46735dc -> 0x4551eac caller chain is direct at verified call sites.',
        '_WeChatMain branch at 0x1986c targets 0x2c976c, which directly calls 0x4671338; that calls 0x46698d0.',
    ],
    'limits': [
        'Selected direct call sites and argument setup do not prove every predecessor or thread identity.',
        'The large caller pseudocode was only inspected in bounded excerpts, not treated as a full semantic proof.',
        'The _WeChatMain thunk pseudocode inlines the large callee; only its four-byte branch is used.',
        'No total order with executor startup/resume, no state-zero final cleanup, and no drain proof.',
        'No runtime reachability, actual native integration, delivery or deployment is established.',
    ],
    'source_sha256': {str(path.relative_to(repo)): digest(path)
                      for path in (Path(__file__).resolve(), reader, stop)},
    'target_executed': False, 'target_attached': False, 'native_function_called': False,
    'callable_for_send': False, 'send_verified': False,
}
with (root / 'shutdown-callers-20261018-verification.json').open('x') as handle:
    json.dump(report, handle, indent=2)
    handle.write('\n')
print(json.dumps({key: value for key, value in report.items()
                  if key not in ('exports', 'source_sha256', 'findings', 'limits', 'branch_decodes')}))

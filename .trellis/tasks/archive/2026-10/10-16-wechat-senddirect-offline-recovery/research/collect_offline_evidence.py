"""Retain offline evidence only. No process attachment, UI, messaging or shell."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import plistlib
import shutil
import sqlite3
import struct

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
HOME = Path.home()
OLD = ROOT / '.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt'
records = {'collected_at': datetime.now(timezone.utc).isoformat(), 'static_sources': [], 'crashes': []}
for name in ('hunt_r33_out.txt', 'hunt_r36_out.txt', 'hunt_r37_out.txt', 'hunt_r38_out.txt'):
    src = HOME / 'ghidra-hunt-r9' / name
    dst = OUT / name
    shutil.copyfile(src, dst)
    records['static_sources'].append({'source': str(src), 'copy': name,
                                     'sha256': hashlib.sha256(dst.read_bytes()).hexdigest()})
for src in (OLD / 'crash-234325.ips',
            HOME / 'Library/Logs/DiagnosticReports/WeChat-2026-10-16-001720.ips',
            HOME / 'Library/Logs/DiagnosticReports/WeChat-2026-10-16-012235.ips'):
    raw = src.read_text()
    _, index = json.JSONDecoder().raw_decode(raw)
    data = json.loads(raw[index:])
    thread = data['threads'][data['faultingThread']]
    state = thread['threadState']
    records['crashes'].append({'source': str(src), 'sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
        'capture_time': data['captureTime'], 'pid': data['pid'], 'exception': data['exception'],
        'thread': thread.get('name'), 'x21': state['x'][21]['value'], 'far': state.get('far'),
        'frames': [{'image': data['usedImages'][f['imageIndex']]['name'], 'rva': hex(f['imageOffset'])}
                   for f in thread['frames'][:6]]})
installed = Path('/Applications/WeChat.app/Contents/Resources/wechat.dylib')
thin = HOME / 'Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib'
# Compare actual installed arm64 slice bytes with the retained analysis carrier.
addresses = (0x5980A84, 0x5980BC4, 0x5980C44, 0x5980CA4, 0x5A6C394, 0x5A6C868, 0x5981CD4)
with installed.open('rb') as binary, thin.open('rb') as carrier:
    magic, count = struct.unpack('>II', binary.read(8))
    assert magic == 0xCAFEBABE
    arches = [struct.unpack('>IIIII', binary.read(20)) for _ in range(count)]
    [arm] = [entry for entry in arches if entry[0] == 0x100000C]
    samples = []
    for address in addresses:
        binary.seek(arm[2] + address)
        carrier.seek(address)
        current = binary.read(8)
        assert len(current) == 8 and current == carrier.read(8), hex(address)
        samples.append({'rva': hex(address), 'bytes': current.hex(), 'carrier_matches': True})
records['binary'] = {'installed': str(installed), 'carrier': str(thin), 'arm64_slice_offset': hex(arm[2]),
    'version': plistlib.loads(Path('/Applications/WeChat.app/Contents/Info.plist').read_bytes())['CFBundleShortVersionString'],
    'samples': samples, 'coverage': 'seven 8-byte anchors only; not whole binary identity'}
connection = sqlite3.connect('file:' + str(HOME / '.zcode/cli/db/db.sqlite') + '?mode=ro', uri=True)
connection.row_factory = sqlite3.Row
sid = 'sess_fb75a5f9-0ba3-4757-b89f-8739bb741c56'
run = 'dwfrun-2d95aeba-da46-4c0c-be1f-a7d86157c155'
records['session'] = dict(connection.execute('select id,title,time_updated from session where id=?', (sid,)).fetchone())
records['workflow'] = dict(connection.execute('select id,name,status,time_updated from dwf_run where id=?', (run,)).fetchone())
records['workflow_running_tool_rows'] = connection.execute("select count(*) from tool_usage where session_id in (select session_id from dwf_actor where run_id=?) and status='running'", (run,)).fetchone()[0]
connection.close()
(OUT / 'evidence.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'static_files': len(records['static_sources']), 'crash_reports': len(records['crashes']),
                  'binary_anchors_match': len(samples), 'workflow_status': records['workflow']['status']}, indent=2))

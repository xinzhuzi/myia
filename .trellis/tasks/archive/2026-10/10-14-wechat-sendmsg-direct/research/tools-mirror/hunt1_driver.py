# -*- coding: utf-8 -*-
"""hunt1_driver.py — 第 1 轮猎捕活体驱动(design Step1 run-sheet + Step2 布防)

经 lldb `command script import` 在解释器线程内跑完整时间线:
  布防(cmd 文件已设 bp1/bp2+on_hit+disable)→ cap.arm(TTL 30s)→ enable → Continue()
  → 触发线程:printf '嘻嘻' | wechat-bridge send_text filehelper --file -(本相位唯一发送,预算 1)
  → 等 hit 文件落盘(hunt/hit_*.txt)→ proc.Stop() 令 Continue() 返回
  → 红线:先禁全部断点,再 Detach。
任何异常路径同样收敛到 Stop→禁断点→Detach(uncertain-never-retry)。
"""

import glob
import os
import subprocess
import threading
import time

import lldb  # noqa: F401  (运行环境=lldb 解释器)
import cap   # noqa: F401  (cmd 文件先前 command script import 过,同一模块实例)

HUNT = '/Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/hunt'
BRIDGE = '/Users/zhengbingjin/.myia/plugins/wechat-bridge/bin/wechat-bridge'
SEND_CMD = "printf '嘻嘻' | %s send_text filehelper --file -" % BRIDGE

cap.configure(hit_dir=HUNT)  # 产物落 hunt/(本相位产物目录)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()


def log(msg):
    print('[driver %s] %s' % (time.strftime('%H:%M:%S'), msg), flush=True)


st = {'armed_at': None, 'hit': None, 'send': None, 'err': None, 'stop_rc': None}


def _bps():
    return [target.GetBreakpointAtIndex(i) for i in range(target.GetNumBreakpoints())]


def wait_hit(deadline):
    while time.time() < deadline:
        hs = [f for f in glob.glob(os.path.join(HUNT, 'hit_*.txt'))
              if os.path.getmtime(f) >= st['armed_at'] - 1]
        if hs:
            return sorted(hs)[-1]
        time.sleep(0.3)
    return None


def trigger():
    try:
        time.sleep(2.0)  # 让 Continue() 先生效(窗口使能与发送间隔≈2-3s,合 design「3s」形态)
        log('TRIGGER: %s' % SEND_CMD)
        t0 = time.time()
        r = subprocess.run(SEND_CMD, shell=True, capture_output=True, text=True, timeout=90)
        st['send'] = {'rc': r.returncode, 'elapsed': round(time.time() - t0, 1),
                      'stdout_tail': (r.stdout or '')[-1500:],
                      'stderr_tail': (r.stderr or '')[-800:]}
        log('TRIGGER done rc=%s elapsed=%ss' % (r.returncode, st['send']['elapsed']))
        if r.returncode != 0:
            log('TRIGGER stdout_tail=%r stderr_tail=%r' % (
                st['send']['stdout_tail'][-400:], st['send']['stderr_tail'][-400:]))
        h = wait_hit(st['armed_at'] + 75)  # cap TTL=30s;余量给桥延迟+堆扫时长
        st['hit'] = h
        log('hit file: %s' % h)
    except Exception as exc:  # noqa: BLE001
        st['err'] = repr(exc)
        log('TRIGGER ERROR: %r' % (exc,))
    finally:
        try:
            st['stop_rc'] = proc.Stop()
            log('proc.Stop() requested rc=%s' % st['stop_rc'])
        except Exception as exc:  # noqa: BLE001
            log('proc.Stop() FAILED: %r' % (exc,))


threading.Thread(target=trigger, daemon=True).start()

# —— 窗口使能(design Step2.1 主降噪:默认禁用,发起点前使能)——
cap.arm(reason='hunt-r1-bridge-send')  # TTL=默认 30s(design 噪声界)
st['armed_at'] = time.time()
for bp in _bps():
    bp.SetEnabled(True)
log('window ARMED at %.0f (TTL 30s), %d bps enabled' % (st['armed_at'], target.GetNumBreakpoints()))

log('Continue()...')
proc.Continue()  # 阻塞至触发线程 Stop() / 进程退出

log('Continue returned; state=%s' % proc.GetState())

# —— 红线:先禁断点,再 detach ——
for bp in _bps():
    bp.SetEnabled(False)
log('ALL BREAKPOINTS DISABLED (pre-detach, red line)')

det = proc.Detach()
log('Detach() success=%s' % bool(det))

print('[driver] SUMMARY ' + repr({
    'pid': proc.GetProcessID(),
    'armed_at': st['armed_at'],
    'hit': st['hit'],
    'send': st['send'],
    'err': st['err'],
    'bp_hitcounts': [bp.GetHitCount() for bp in _bps()],
    'proc_state_after_detach': proc.GetState(),
}), flush=True)

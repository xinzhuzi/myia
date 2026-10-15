#!/bin/bash
# 媒体钥哨兵发射器:等直发攻坚的 LLDB 脱附(轮次间隙/收工)后武装。
# 判据:没有任何 lldb 进程在跑 → 静默 90 秒二次确认 → 发射本哨兵。
# 产物:/tmp/wx_media_key_sentinel/{KEY(命中),lldb.log,ARMED,EXIT,SKIP}
export HOME=/Users/zhengbingjin
D=/tmp/wx_media_key_sentinel
touch "$D/ARMED"

# —— 阶段 1:等并行 lldb 退场(最多 4 小时)——
for i in $(seq 1 480); do
  if ! pgrep -x lldb >/dev/null 2>&1; then
    break
  fi
  sleep 30
done
if pgrep -x lldb >/dev/null 2>&1; then
  echo "parallel-lldb-still-running" > "$D/SKIP"
  exit 0
fi

# —— 阶段 2:静默窗(对方下一轮若启动,这里会让位)——
sleep 180
if pgrep -x lldb >/dev/null 2>&1; then
  echo "parallel-lldb-returned" > "$D/SKIP"
  exit 0
fi

# —— 阶段 3:发射哨兵(微信若已重启,PID 变化则放弃)——
WPID=$(pgrep -x WeChat | head -1)
if [ "$WPID" != "20632" ]; then
  echo "wechat-pid-changed:$WPID" > "$D/SKIP"
  exit 0
fi

# 校验 oracle 样本仍在
if [ ! -d /tmp/wximg ] || [ -z "$(ls /tmp/wximg/*.dat 2>/dev/null)" ]; then
  echo "samples-missing" > "$D/SKIP"
  exit 0
fi

lldb -b -s "$D/run.cmd" > "$D/lldb.log" 2>&1
rc=$?
echo "$rc" > "$D/EXIT"
exit "$rc"

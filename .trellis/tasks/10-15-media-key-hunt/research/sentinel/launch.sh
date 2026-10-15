#!/bin/bash
# 媒体钥哨兵·持久守望发射器(v2):并行会话(uicreate 等)与哨兵共用微信
# task port,单占互斥。本发射器循环礼让协议,不再单次排队输竞态:
#   等无 lldb → 180s 静默窗(窗内 lldb 回归 = 回队尾重等)→ 核 WeChat
#   在跑+样本在场 → 动态生成 run.cmd(当下 PID)→ 发射哨兵(阻塞)→
#   KEY 落袋 = 终局;哨兵被 TERM(143)/无钥退出 = 回队尾重等。
# 总耐心 6 小时;状态标记落 $D(ARMED/SKIP/EXIT/KEY)供外部守望。
export HOME=/Users/zhengbingjin
D=/tmp/wx_media_key_sentinel
DEADLINE=$(( $(date +%s) + 6*3600 ))
touch "$D/ARMED"

while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  # —— 阶段 1:等并行 lldb 退场 ——
  while pgrep -x lldb >/dev/null 2>&1; do
    sleep 30
    if [ "$(date +%s)" -ge "$DEADLINE" ]; then
      echo "patience-exhausted" > "$D/SKIP"; exit 0
    fi
  done

  # —— 阶段 2:静默窗(窗内回归 = 礼让回队)——
  sleep 180
  if pgrep -x lldb >/dev/null 2>&1; then
    echo "parallel-lldb-returned $(date +%H:%M)" > "$D/SKIP"
    continue
  fi

  # —— 阶段 3:环境核验 + 动态 run.cmd ——
  WPID=$(pgrep -x WeChat | head -1)
  if [ -z "$WPID" ]; then
    echo "wechat-not-running $(date +%H:%M)" > "$D/SKIP"
    continue
  fi
  if [ ! -d /tmp/wximg ] || [ -z "$(ls /tmp/wximg/*.dat 2>/dev/null)" ]; then
    echo "samples-missing $(date +%H:%M)" > "$D/SKIP"
    continue
  fi
  cat > "$D/run.cmd" <<EOF
process attach --pid $WPID
command script import $D/cap.py
breakpoint set -n CCCrypt
breakpoint command add -F cap.on_hit -s python 1
breakpoint set -n CCCryptorCreate
breakpoint command add -F cap.on_hit -s python 2
continue
detach
quit
EOF

  # —— 阶段 4:发射(阻塞;TERM/无钥退出均回队)——
  rm -f "$D/EXIT" "$D/SKIP"
  lldb -b -s "$D/run.cmd" > "$D/lldb.log" 2>&1
  rc=$?
  echo "$rc" > "$D/EXIT"
  if [ -f "$D/KEY" ]; then
    exit 0
  fi
  # 143=被 TERM(并行线要口)或其他退出:回队尾重等
  echo "displaced-rc$rc $(date +%H:%M)" > "$D/SKIP"
done

echo "patience-exhausted" > "$D/SKIP"
exit 0

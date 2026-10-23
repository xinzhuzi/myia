#!/bin/bash
# Disabled 2026-10-16: legacy background and repeated debugger attachments.
# Keep this gate. Fresh authorization does not make this legacy runner safe;
# a separately reviewed foreground single-window runner is required.
printf '%s\n' 'Disabled: background LLDB orchestration and repeated attachments are prohibited; obtain fresh single-window authorization first.' >&2
exit 78

# truepath 第四窗编排:pre 锚点 → 兜底序列化+分发桥捕获(+needle 观察点)→ EXIT5 守望+SIGTERM 兜底 → post 锚点复验。
set -u
BASE="/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
LOG="$BASE/orchestrate5.log"
PID=$(pgrep -x WeChat | head -1)
echo "orchestrate5 start $(date +%H:%M:%S) wechat_pid=$PID" | tee -a "$LOG"
[ -n "$PID" ] || { echo "FATAL: no WeChat pid" | tee -a "$LOG"; exit 1; }
sed -i '' "s/--pid [0-9]*/--pid $PID/" "$BASE/pre.cmd" "$BASE/runcap5.cmd" "$BASE/post.cmd"

echo "== pre verify ==" | tee -a "$LOG"
lldb -s "$BASE/pre.cmd" > "$BASE/pre5_run.log" 2>&1 < /dev/null
grep -h "VERIFY_" "$BASE/pre5_run.log" | tee -a "$LOG"

echo "== capture run 5 ==" | tee -a "$LOG"
rm -f "$BASE/EXIT5" "$BASE/watch4_set.txt"
lldb -s "$BASE/runcap5.cmd" > "$BASE/runcap5.log" 2>&1 < /dev/null &
LPID=$!
echo "lldb cap5 pid=$LPID" | tee -a "$LOG"
D=$((SECONDS + 300))
while [ $SECONDS -lt $D ]; do
  [ -f "$BASE/EXIT5" ] && break
  kill -0 "$LPID" 2>/dev/null || break
  sleep 1
done
if kill -0 "$LPID" 2>/dev/null; then
  echo "SIGTERM fallback -> lldb $LPID" | tee -a "$LOG"
  kill -TERM "$LPID" 2>/dev/null
  sleep 3
  kill -0 "$LPID" 2>/dev/null && kill -TERM "$LPID" 2>/dev/null
fi
wait "$LPID" 2>/dev/null
RC=$?
echo "lldb cap5 exited rc=$RC $(date +%H:%M:%S)" | tee -a "$LOG"

echo "== post verify ==" | tee -a "$LOG"
PID2=$(pgrep -x WeChat | head -1)
echo "post wechat_pid=$PID2" | tee -a "$LOG"
if [ -n "$PID2" ] && [ "$PID2" != "$PID" ]; then
  sed -i '' "s/--pid [0-9]*/--pid $PID2/" "$BASE/post.cmd"
fi
if [ -n "$PID2" ]; then
  lldb -s "$BASE/post.cmd" > "$BASE/post5_run.log" 2>&1 < /dev/null
  grep -h "VERIFY_" "$BASE/post5_run.log" | tee -a "$LOG"
else
  echo "FATAL: WeChat process gone after capture" | tee -a "$LOG"
fi
echo "orchestrate5 end $(date +%H:%M:%S)" | tee -a "$LOG"

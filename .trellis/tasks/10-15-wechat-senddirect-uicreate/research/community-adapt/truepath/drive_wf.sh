#!/bin/bash
# Disabled 2026-10-16: legacy background and repeated debugger attachments.
# Keep this gate. Any replacement requires fresh explicit target/purpose/time
# authorization and a separately reviewed foreground single-window runner.
printf '%s\n' 'Disabled: background LLDB orchestration and repeated attachments are prohibited; obtain fresh single-window authorization first.' >&2
exit 78

# truepath 勘察编排:pre 锚点 → lldb 捕获(桥断点+needle printf 管道)→
# EXIT 文件守望 + SIGTERM 兜底 → post 锚点复验。全链纯读。
set -u
BASE="/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
LOG="$BASE/orchestrate.log"
PID=$(pgrep -x WeChat | head -1)
echo "orchestrate start $(date +%H:%M:%S) wechat_pid=$PID" | tee -a "$LOG"
[ -n "$PID" ] || { echo "FATAL: no WeChat pid" | tee -a "$LOG"; exit 1; }
sed -i '' "s/--pid [0-9]*/--pid $PID/" "$BASE/pre.cmd" "$BASE/runcap.cmd" "$BASE/post.cmd"

echo "== pre verify ==" | tee -a "$LOG"
lldb -s "$BASE/pre.cmd" > "$BASE/pre_run.log" 2>&1 < /dev/null
grep -h "VERIFY_" "$BASE/pre_run.log" | tee -a "$LOG"

echo "== capture run ==" | tee -a "$LOG"
rm -f "$BASE/EXIT"
lldb -s "$BASE/runcap.cmd" > "$BASE/runcap.log" 2>&1 < /dev/null &
LPID=$!
echo "lldb cap pid=$LPID" | tee -a "$LOG"
D=$((SECONDS + 260))
while [ $SECONDS -lt $D ]; do
  [ -f "$BASE/EXIT" ] && break
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
echo "lldb cap exited rc=$RC $(date +%H:%M:%S)" | tee -a "$LOG"

echo "== post verify ==" | tee -a "$LOG"
PID2=$(pgrep -x WeChat | head -1)
echo "post wechat_pid=$PID2" | tee -a "$LOG"
if [ -n "$PID2" ] && [ "$PID2" != "$PID" ]; then
  sed -i '' "s/--pid [0-9]*/--pid $PID2/" "$BASE/post.cmd"
fi
if [ -n "$PID2" ]; then
  lldb -s "$BASE/post.cmd" > "$BASE/post_run.log" 2>&1 < /dev/null
  grep -h "VERIFY_" "$BASE/post_run.log" | tee -a "$LOG"
else
  echo "FATAL: WeChat process gone after capture" | tee -a "$LOG"
fi
echo "orchestrate end $(date +%H:%M:%S)" | tee -a "$LOG"

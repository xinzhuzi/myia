#!/bin/bash
# Disabled 2026-10-16: this legacy runner backgrounds LLDB and reattaches for
# pre/post checks. User policy requires a fresh, explicit target/purpose/time
# authorization and one foreground bounded window. Do not remove or bypass this
# gate; use a separately reviewed foreground runner after fresh authorization.
printf '%s\n' 'Disabled: background LLDB orchestration and repeated attachments are prohibited; obtain fresh single-window authorization first.' >&2
exit 78

# truepath 第三窗编排:pre 锚点 → MMStartTask 捕获+needle 观察点 → EXIT3 守望+SIGTERM 兜底 → post 锚点复验。
set -u
BASE="/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
LOG="$BASE/orchestrate3.log"
PID=$(pgrep -x WeChat | head -1)
echo "orchestrate3 start $(date +%H:%M:%S) wechat_pid=$PID" | tee -a "$LOG"
[ -n "$PID" ] || { echo "FATAL: no WeChat pid" | tee -a "$LOG"; exit 1; }
sed -i '' "s/--pid [0-9]*/--pid $PID/" "$BASE/pre.cmd" "$BASE/runcap3.cmd" "$BASE/post.cmd"

echo "== pre verify ==" | tee -a "$LOG"
lldb -s "$BASE/pre.cmd" > "$BASE/pre3_run.log" 2>&1 < /dev/null
grep -h "VERIFY_" "$BASE/pre3_run.log" | tee -a "$LOG"

echo "== capture run 3 ==" | tee -a "$LOG"
rm -f "$BASE/EXIT3" "$BASE/watch_set.txt"
lldb -s "$BASE/runcap3.cmd" > "$BASE/runcap3.log" 2>&1 < /dev/null &
LPID=$!
echo "lldb cap3 pid=$LPID" | tee -a "$LOG"
D=$((SECONDS + 300))
while [ $SECONDS -lt $D ]; do
  [ -f "$BASE/EXIT3" ] && break
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
echo "lldb cap3 exited rc=$RC $(date +%H:%M:%S)" | tee -a "$LOG"

echo "== post verify ==" | tee -a "$LOG"
PID2=$(pgrep -x WeChat | head -1)
echo "post wechat_pid=$PID2" | tee -a "$LOG"
if [ -n "$PID2" ] && [ "$PID2" != "$PID" ]; then
  sed -i '' "s/--pid [0-9]*/--pid $PID2/" "$BASE/post.cmd"
fi
if [ -n "$PID2" ]; then
  lldb -s "$BASE/post.cmd" > "$BASE/post3_run.log" 2>&1 < /dev/null
  grep -h "VERIFY_" "$BASE/post3_run.log" | tee -a "$LOG"
else
  echo "FATAL: WeChat process gone after capture" | tee -a "$LOG"
fi
echo "orchestrate3 end $(date +%H:%M:%S)" | tee -a "$LOG"

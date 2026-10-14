#!/bin/bash
# 用法: round.sh <轮号> <正文>
# 单轮:attach→ARMED→桥真发 filehelper→等 DONE(判别门命中)→SIGINT 干净收兵→detach。
set -u
N="$1"; MSG="$2"
ROOT=/tmp/wxsend3
PID=$(pgrep -x WeChat | head -1)
if [ -z "$PID" ]; then echo "FATAL: WeChat pid not found"; exit 1; fi
echo "WeChat pid=$PID"

rm -f "$ROOT/ARMED" "$ROOT/DONE" "$ROOT/ERROR" "$ROOT/SHUTDOWN_OK" \
      "$ROOT/SHUTDOWN_ERR" "$ROOT/LLDB_EXIT"

cat > "$ROOT/lldb.cmd" <<EOF
attach -p $PID
command script import /tmp/wxsend3/cap2.py
script cap2.install(lldb.debugger)
continue
script cap2.shutdown()
detach
quit
EOF

lldb -b -s "$ROOT/lldb.cmd" > "$ROOT/lldb$N.log" 2>&1 &
LLDB_PID=$!
echo "$LLDB_PID" > "$ROOT/lldb.pid"

# 等 ARMED/ERROR(≤30s,事件标记轮询)
armed=no
for _ in $(seq 1 150); do
  [ -f "$ROOT/ARMED" ] && { armed=yes; break; }
  [ -f "$ROOT/ERROR" ] && break
  sleep 0.2
done
if [ "$armed" != yes ]; then
  echo "ARMED timeout/ERROR:"; cat "$ROOT/ERROR" 2>/dev/null
  kill -9 "$LLDB_PID" 2>/dev/null
  exit 1
fi
cat "$ROOT/ARMED"

# 触发真发(正文经 stdin,argv 零正文)
printf '%s' "$MSG" > "$ROOT/msg$N.txt"
( cd /Users/zhengbingjin/Project/Github/MYIA/plugins/wechat-bridge && \
  ./bin/wechat-bridge send_text filehelper --file - < "$ROOT/msg$N.txt" ) \
  > "$ROOT/send$N.log" 2>&1
echo "bridge rc=$?"

# 等 DONE(判别门:dump 含 filehelper;≤240s)
found=no
for _ in $(seq 1 1200); do
  [ -f "$ROOT/DONE" ] && { found=yes; break; }
  sleep 0.2
done
[ -f "$ROOT/DONE" ] && cat "$ROOT/DONE"

# 干净收兵:SIGINT→lldb 中断 continue,跑 shutdown(禁断点)+detach+quit
kill -INT "$LLDB_PID" 2>/dev/null
for _ in $(seq 1 150); do
  kill -0 "$LLDB_PID" 2>/dev/null || break
  sleep 0.2
done
if kill -0 "$LLDB_PID" 2>/dev/null; then
  kill -TERM "$LLDB_PID" 2>/dev/null
  sleep 1
fi
wait "$LLDB_PID" 2>/dev/null
echo "lldb_exit=$?" > "$ROOT/LLDB_EXIT"

sleep 1
if pgrep -x WeChat >/dev/null; then echo "WeChat ALIVE"; else echo "WeChat DEAD !!!"; fi
echo "found=$found"

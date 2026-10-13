#!/bin/bash
# 用户态监控段:弹密码框→等断点就位→通知主人重登→等收尾
D=/tmp/wxkey-c
LOG=$D/lldb-extract.log
rm -f "$D/lldb-extract.exit" "$D/shot.done"
: > "$LOG"
osascript -e 'do shell script "bash /tmp/wxkey-c/lldb-run.sh" with administrator privileges with prompt "MYIA 微信取钥:LLDB 断点抓密钥(一次性,只读)"' &
OSA=$!
armed=0
for i in $(seq 1 600); do
  if grep -q "工具将等待最多" "$LOG" 2>/dev/null; then armed=1; break; fi
  [ -f "$D/lldb-extract.exit" ] && break
  sleep 1
done
if [ "$armed" = 1 ]; then
  osascript -e 'display notification "断点即将就位(约 10 秒)。请现在在微信里:设置 → 退出登录 → 重新扫码登录。5 分钟内完成。" with title "MYIA 取钥" sound name "Glass"'
else
  osascript -e 'display notification "取钥任务结束或异常,详见日志" with title "MYIA 取钥"' 2>/dev/null
fi
wait $OSA 2>/dev/null; osa_rc=$?
echo "osa_rc=$osa_rc extract_rc=$(cat "$D/lldb-extract.exit" 2>/dev/null || echo NA)" > "$D/shot.done"

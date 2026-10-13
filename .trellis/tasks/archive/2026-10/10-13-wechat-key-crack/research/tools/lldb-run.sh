#!/bin/bash
# 提权段:跑蓝本 extract(LLDB 抓 passphrase+派生验真),产物落 /tmp/wxkey-c/
export HOME=/Users/zhengbingjin
D=/tmp/wxkey-c
PY=/Users/zhengbingjin/Project/Github/MYIA/.venv/bin/python3
[ -x "$PY" ] || PY=/usr/bin/python3
"$PY" /tmp/wcdb_key_tool_macos.py extract \
  --output "$D/all_keys.json" --timeout 300 > "$D/lldb-extract.log" 2>&1
rc=$?
echo $rc > "$D/lldb-extract.exit"
# 钥匙件属主归还(密码/passphrase 文件 root 写的,归还主人)
chown -R zhengbingjin:staff "$HOME/.wcdb-key-tool" 2>/dev/null
chown zhengbingjin:staff "$D/all_keys.json" "$D/lldb-extract.log" 2>/dev/null
exit $rc

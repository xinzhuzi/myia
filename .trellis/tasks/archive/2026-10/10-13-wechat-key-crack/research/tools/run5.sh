#!/bin/bash
# run5.sh:阶段1.5 实战运行件(需主人一次 sudo;只读 mach,零微信干预)
# 产物:stderr 形状级统计 → final5.log;stdout 的 KEY 行 → hit5.key(chmod 600,
#       命中后按 verify3 → write_key_cache(<myssia_home>/wechat-localdb/keys.json) 落点)
# 预算:缺省验证上限 5000(≈5 分钟);候选超限(HITS 0 且 已验证==5000)时:
#       sudo COLLECTOR5_MAXVERIFY=0 bash run5.sh 重跑不设限(0.061s/候选)
pkill -9 -f "collector5" 2>/dev/null
sleep 2
cd /tmp/wxkey-c
DB=$(ls /Users/zhengbingjin/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/db_storage/message/message_0.db | head -1)
umask 077
./collector5 "$DB" > hit5.key 2> final5.log
RC=$?
chmod 600 hit5.key 2>/dev/null
chown -R zhengbingjin:staff /tmp/wxkey-c 2>/dev/null
if [ -s hit5.key ]; then
  echo "命中!密钥在 /tmp/wxkey-c/hit5.key(600);下一步:"
  echo "  1) 交叉验证: cat hit5.key | head -1 | sed 's/^KEY //' > candidates2.txt && python3 <攻坚档>/research/tools/verify3.py"
  echo "  2) 落点(数据根私有区): 用桥组件 write_key_cache({'message_0': '<hex>'})"
fi
exit $RC

#!/usr/bin/env python3
"""chatlog darwin/v4 协议手撸验证器(全参数可控,不依赖 sqlcipher CLI 形态)。
协议: encKey=PBKDF2(key32,salt,256000,32,SHA512); macSalt=salt^0x3a;
macKey=PBKDF2(encKey,macSalt,2,32); HMAC-SHA512(macKey, page[16:4032]+le32(1))==page[4032:4096]"""
import concurrent.futures as cf
import hashlib, json, os, struct, sys

HOME = os.path.expanduser("~")
DB = None
for root, dirs, files in os.walk(f"{HOME}/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files"):
    if root.endswith("/db_storage/message") and "message_0.db" in files:
        DB = os.path.join(root, "message_0.db"); break
if not DB: sys.exit("找不到 message_0.db")

PAGE = 4096; SALT = 16; DATA_END = PAGE - 80 + 16; HMAC_N = 64
page1 = open(DB, "rb").read(PAGE)
salt = page1[:16]
mac_salt = bytes(b ^ 0x3a for b in salt)
stored_mac = page1[DATA_END:DATA_END + HMAC_N]
prefix = page1[SALT:DATA_END] + struct.pack("<I", 1)

def try_key(hx: str) -> bool:
    try:
        key = bytes.fromhex(hx)
    except ValueError:
        return False
    if len(key) != 32:
        return False
    import hmac
    enc = hashlib.pbkdf2_hmac("sha512", key, salt, 256000, 32)
    mk = hashlib.pbkdf2_hmac("sha512", enc, mac_salt, 2, 32)
    calc = hmac.new(mk, prefix, hashlib.sha512).digest()
    return hmac.compare_digest(calc, stored_mac)

cands = [l.strip() for l in open("/tmp/wxkey-c/candidates.txt") if l.strip()]
print(f"候选 {len(cands)}(pbkdf2 256000×每候选,8 并行)", flush=True)
hits = []
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for i, ok in enumerate(ex.map(try_key, cands, chunksize=16)):
        if ok:
            hits.append(cands[i]); print(f"✅ HIT {cands[i]}", flush=True)
        if (i+1) % 1000 == 0: print(f"进度 {i+1}/{len(cands)} 命中 {len(hits)}", flush=True)
json.dump({"message_0": hits}, open("/tmp/wxkey-c/verified_keys.json", "w"), indent=1)
print(f"完成:命中 {len(hits)}", flush=True)

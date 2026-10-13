#!/usr/bin/env python3
"""key_info_data 逐字节方差分析(10-13-wechat-key-crack 阶段3 step0 零成本预检)。

方法照 luvrell/wechat-msg-extract docs/01-密钥获取实测记录.md(Windows 4.1.13,219 行):
跨行按绝对位置对齐,统计每字节位置是「常量(全行同值)」还是「变量」;
Windows 模板 = [0..16 常量][17..30 变14B][31..66 常量36B][67..170 变104B][171..174 常量]
               [175..178 变4B][179 常量]  → 定性=「固定模板+随机字段」登录凭证,非整体密文。
我方对照判据:
  - 若 macOS 35 行同样出现大片常量区(尤其中段 36B)→ 与 Windows 同构坐实,
    「152B 加密体离线派生」正式判死(Windows 侧四组独立穷举已全灭,再无悬念);
  - 若除信封头外全随机且行间无差异信号 → 维持「整体加密体」原判,离线路线仍死但定性不同;
  - 若仅 1 个唯一值(35 行同 blob)→ 无方差信号可用,如实归档。
只读(mode=ro);输出形状级证据,零密钥材料。
"""
import hashlib
import sqlite3
import sys

DB = ("/Users/zhengbingjin/Library/Containers/com.tencent.xinWeChat/Data/"
      "Documents/xwechat_files/all_users/login/wxid_oc2yhey1xkpw22/key_info.db")

# Windows 4.1.13 模板(luvrell 实测,180B,区间为 [起,止) 语义按其 1-based 描述换算)
WIN_TEMPLATE = (
    [(0, 17, "常量17B"), (17, 31, "变化14B"), (31, 67, "常量36B"),
     (67, 171, "变化104B"), (171, 175, "常量4B"), (175, 179, "变化4B"), (179, 180, "常量1B")]
)


def ranges(mask):
    """把 0/1 掩码压成区间列表 [(start,end,label)]."""
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i)); s = None
    if s is not None:
        out.append((s, len(mask)))
    return out


def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute(
        "SELECT user_name_md5, key_md5, key_info_md5, key_info_data FROM LoginKeyInfoTable"
    ).fetchall()
    print(f"行数={len(rows)}")

    # 身份列形状(非密钥材料):唯一值计数 + wxid md5 对拍(路径已知 wxid,零成本鉴定)
    wxid = "wxid_oc2yhey1xkpw22"
    for col, idx in (("user_name_md5", 0), ("key_md5", 1), ("key_info_md5", 2)):
        vals = {r[idx] for r in rows}
        print(f"{col}: 唯一值={len(vals)} 长度集={ {len(v) for v in vals} }")
    probe = hashlib.md5(wxid.encode()).hexdigest()
    uname = {r[0] for r in rows}
    print(f"md5({wxid})={probe} user_name_md5 匹配={probe in uname}")

    blobs = [bytes(r[3]) for r in rows]
    uniq = set(blobs)
    print(f"key_info_data: 行数={len(blobs)} 唯一blob数={len(uniq)} 长度集={sorted({len(b) for b in blobs})}")
    if len(uniq) <= 1:
        print("结论:全部行同一 blob,无跨行方差信号可用(单登录会话快照)。")
        return

    # 对齐主群(180B)做逐位置方差
    main_len = max({len(b) for b in blobs}, key=lambda L: sum(1 for b in blobs if len(b) == L))
    group = [b for b in blobs if len(b) == main_len]
    print(f"主群长度={main_len}B 行数={len(group)}")
    mask = []  # 1=常量
    per_pos_const_val = []
    for i in range(main_len):
        vals = {b[i] for b in group}
        mask.append(1 if len(vals) == 1 else 0)
        per_pos_const_val.append(next(iter(vals)) if len(vals) == 1 else None)

    print("\n== 常量/变量区间(0-based,[起,止)) ==")
    for s, e in ranges(mask):
        tag = "常量" if mask[s] else "变量"
        cval = f" 值={per_pos_const_val[s]:02x}" if mask[s] else ""
        print(f"  [{s:3d},{e:3d}) {tag} {e - s}B{cval}")

    print("\n== 与 Windows 4.1.13 模板对照 ==")
    for s, e, label in WIN_TEMPLATE:
        seg = mask[s:e]
        c = sum(seg)
        print(f"  Win[{s:3d},{e:3d}) {label}: 我方常量 {c}/{e - s}")

    print("\n== 常量区字节 ==  (形状级,非密钥材料)")
    for s, e in ranges(mask):
        if mask[s]:
            print(f"  [{s:3d},{e:3d}): {' '.join(f'{per_pos_const_val[i]:02x}' for i in range(s, e))}")

    # 信封 protobuf 头解析(全行同构性)
    b0 = group[0]
    print(f"\n首行头32B: {b0[:32].hex()}")


if __name__ == "__main__":
    sys.exit(main())

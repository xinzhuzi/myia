"""合成微信主窗面板渲染器(test_pixel 的 fixture 事实源)。

用途(D2 像素链验证):渲染一张**仿微信会话列表+聊天区**的深色主题面板,
全部文字为合成内容(「合成会话X」/「合成消息…」——零私有数据,可入 git),
带**已知真值**(GROUND_TRUTH)供解析链断言:
    - VisionOCR 真跑(gated)→ parse_sessions/parse_messages 命中率;
    - 单测直接用 GROUND_TRUTH 的几何构造 OcrLine 列表(纯函数断言)。

几何取 2026-10-11 真窗实测形状的等比复刻(2x 渲染,3840×2100):
侧栏亮带 0–0.052、会话名列 x≈0.060、时间列右缘 ≈0.229、行距 ≈0.059、
未读徽标在时间右下(红底白数字)、聊天标题 y≈0.043、居中时间 ≈0.60、
自己气泡右缘 ≈0.98。坐标系:渲染像素 / 1920(宽) 与 /1050(高)。
"""

from __future__ import annotations

from pathlib import Path

#: 画布(逻辑 1920×1050 @2x)。
W, H = 3840, 2100
SX, SY = W / 1920.0, H / 1050.0

FONT_CANDIDATES = (
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
)

# —— 合成真值(几何以归一化坐标给;文本全部显式合成)——
#: 会话行: (名字, 时间, 未读[None|int|"999+"], 预览)
SESSIONS: tuple[tuple[str, str, int | str | None, str], ...] = (
    ("合成会话甲", "23:45", 3, "合成消息:晚上一起吃饭吗"),
    ("SyntheticBeta", "22:10", None, "合成消息:好的,明天见"),
    ("合成会话丙-项目群", "昨天", 999, "合成消息:[图片]"),
    ("Delta合成", "昨天", 1, "合成消息:文件已发你邮箱"),
    ("合成会话戊", "周六", None, "合成消息:这周末安排上了"),
    ("Epsilon群", "10/10", 12, "合成消息:收到"),
    ("合成会话庚", "10/09", None, "合成消息:辛苦了"),
    ("Zeta-合成长名称会话测试用例", "周二", 2, "合成消息:这条预览文本比较长用于测试截断"),
)
#: 聊天标题(标题行 y≈0.043)。
CHAT_TITLE = "合成会话甲"
#: 消息流:(side, 文本[, 发送者名])——渲染顺序自上而下。
MESSAGES: tuple[tuple[str, str, str | None], ...] = (
    ("time", "14:20", None),
    ("left", "合成消息:这是第一段比较长的文本会在气泡里显示", None),
    ("left", "收到,合成回复第一行", "合成同事"),
    ("right", "合成回复:我这边也好了"),
    ("time", "14:35", None),
    ("left", "合成消息:第二条来自群成员", "SyntheticFriend"),
    ("right", "最后一条合成消息"),
)


def _load_font(size: int):
    from PIL import ImageFont

    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return None


def render(out_path: Path) -> Path:
    """渲染合成面板 PNG(3840×2100 深色主题;文字=上表真值)。"""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), (28, 28, 29))
    draw = ImageDraw.Draw(img)
    # 侧栏亮带(实测 0–0.052,偏亮灰)
    draw.rectangle([0, 0, round(0.052 * W), H], fill=(98, 98, 100))
    # 会话列表面板底色(与聊天区同深,列边界仅由文本几何区分——实测同此)
    draw.rectangle([round(0.052 * W), 0, round(0.24 * W), H], fill=(34, 34, 36))

    f_name = _load_font(round(28 * SX / 2))
    f_small = _load_font(round(24 * SX / 2))
    f_time = _load_font(round(22 * SX / 2))
    f_bubble = _load_font(round(26 * SX / 2))
    f_badge = _load_font(round(20 * SX / 2))
    assert f_name is not None, "CJK 字体缺失,无法渲染合成面板"

    # 聊天标题(y≈0.043,聊天区左上)
    draw.text((round(0.44 * W), round(0.041 * H)), CHAT_TITLE, font=f_name, fill=(230, 230, 230))

    # 会话行(名字 y 自 0.086 起,行距 0.059;时间右上;预览=名字+0.018;徽标右下)
    row_y0, pitch = 0.086, 0.059
    for index, (name, when, unread, preview) in enumerate(SESSIONS):
        y = row_y0 + index * pitch
        draw.text((round(0.060 * W), round(y * H)), name, font=f_name, fill=(235, 235, 235))
        tw = draw.textlength(when, font=f_time)
        draw.text((round(0.229 * W) - round(tw), round(y * H) + 6), when, font=f_time, fill=(160, 160, 160))
        draw.text(
            (round(0.060 * W), round((y + 0.018) * H)), preview, font=f_small, fill=(150, 150, 150)
        )
        if unread is not None:
            label = str(unread)
            bw = max(round(0.021 * W), round(draw.textlength(label, font=f_badge)) + 24)
            bx = round(0.229 * W) - bw + 8
            by = round((y + 0.018) * H) - 14
            draw.ellipse([bx, by, bx + bw, by + round(0.021 * W)], fill=(236, 72, 72))
            draw.text(
                (bx + (bw - round(draw.textlength(label, font=f_badge))) // 2,
                 by + (round(0.021 * W) - f_badge.size) // 2),
                label, font=f_badge, fill=(255, 255, 255),
            )

    # 消息流(居中时间 / 左气泡带发送者 / 右气泡)
    msg_y = 0.16
    for entry in MESSAGES:
        side, text, sender = (list(entry) + [None] * 3)[:3]
        if side == "time":
            tw = draw.textlength(text, font=f_time)
            draw.text((round(0.60 * W) - round(tw / 2), round(msg_y * H)), text, font=f_time, fill=(140, 140, 140))
            msg_y += 0.042
            continue
        if side == "left":
            if sender:
                draw.text((round(0.243 * W), round(msg_y * H)), sender, font=f_small, fill=(150, 150, 150))
                msg_y += 0.030  # 名→气泡(实测 ≈0.030)
            draw.text((round(0.243 * W), round(msg_y * H)), text, font=f_bubble, fill=(235, 235, 235))
            msg_y += 0.042
        else:  # right
            tw = draw.textlength(text, font=f_bubble)
            draw.text((round(0.98 * W) - round(tw), round(msg_y * H)), text, font=f_bubble, fill=(235, 255, 235))
            msg_y += 0.042
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":  # pragma: no cover - 手工再生成入口
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "fixtures" / "synthetic_wechat_panel.png"
    print(render(target))

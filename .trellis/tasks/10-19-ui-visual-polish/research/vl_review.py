#!/usr/bin/env python3
"""10-19-ui-visual-polph 取证评审:LM Studio 本地现眼逐图列视觉 finding。"""
import base64
import json
import pathlib
import sys
import urllib.request

ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "qwen3.8-27b-coder390"
IMAGES = {
    "messaging_fullpage": "/tmp/myia-messaging-smoke/messaging-fullpage.png",
    "messaging_viewport": "/tmp/myia-messaging-smoke/messaging-viewport.png",
    "platform_overview": "/tmp/myia-messaging-smoke/platform-overview.png",
    "tg_card": "/tmp/myssia-tg-card-smoke.png",
}
PROMPT = """你是严格的 UI 视觉评审员,在评审一张 MYIA 桌面应用(深色主题情报台,React+Tailwind)截图。
请只凭画面找【视觉/排版】问题,重点维度:
1) 卡片内部留白失衡(如卡片下半大面积空白、内容挤在上半);
2) 图标风格不统一(同一界面混用描边/填充/彩色多种图标风格);
3) 垂直失衡(左右栏高度差悬殊、元素挤压或拉伸、头部与正文比例失调);
4) 提示句/说明文字的形态(是否像悬浮的孤行、与所在卡片缺乏视觉归属);
5) 其他明显排版缺陷(对齐、截断、溢出、间距不一致)。
每条 finding 给:{id, area(在画面哪里), problem(一句话), severity(low/medium/high)}。
没有问题的维度不要硬凑。用中文,输出 JSON 数组,不要输出思考过程。"""


def b64(path: str) -> str:
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def ask(name: str, path: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64(path)}"}},
            ],
        }],
        "max_tokens": 6000,
        "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.load(resp)
    return data["choices"][0]["message"]["content"]


def main() -> int:
    out = {}
    for name, path in IMAGES.items():
        if not pathlib.Path(path).exists():
            print(f"skip - {name}: {path} 缺失", file=sys.stderr)
            continue
        try:
            text = ask(name, path)
        except Exception as exc:  # noqa: BLE001
            text = f"ERROR: {exc}"
        out[name] = text
        print(f"=== {name} ===")
        print(text[:1800])
        print()
    dest = pathlib.Path(".trellis/tasks/10-19-ui-visual-polish/research/vl-findings.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"saved - {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

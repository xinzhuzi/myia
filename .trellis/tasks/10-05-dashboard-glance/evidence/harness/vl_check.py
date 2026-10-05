"""S7 二级核验(本机 mlx-vlm Qwen3-VL-8B,http://127.0.0.1:8080,零出网)。

一级 Vision 触发机械升级判据(多行 ≤0.5)后按 local-ocr SKILL.md 第二级跑:
① 全部 9 图:文字重叠/裁切/溢出定向检查(短答,直指 S7 核验目标);
② 01/02 verdict 行:校对模式(一级 0.30 行逐字复核)。
云端 glm-5.3-flash 已探死(429 code 1113 余额不足),不走向云。
"""

from __future__ import annotations

import base64
import json
import sys
import urllib.request
from pathlib import Path

ENDPOINT = "http://127.0.0.1:8080/v1/chat/completions"
MODEL = "/Users/zhengbingjin/Library/Application Support/MYIA/models/qwen3-vl-8b-mlx"
EVIDENCE = Path("/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-05-dashboard-glance/evidence")

OVERLAP_PROMPT = (
    "仔细检查这张应用界面截图中的文字排版:有没有出现以下任一情况——"
    "①两行文字互相重叠叠印在一起;②文字被容器边缘裁切截断(设计内的省略号截断不算);"
    "③文字溢出所属卡片/容器压到相邻元素。逐条列出(位置+文字);"
    "若完全不存在这些情况,只回答:无重叠无裁切无溢出。"
)


def ask(image_path: Path, question: str, timeout: int = 420) -> str:
    b64 = base64.b64encode(image_path.read_bytes()).decode()
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(
            {
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
                            {"type": "text", "text": question},
                        ],
                    }
                ],
            }
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def main() -> int:
    shots = sorted(p for p in EVIDENCE.glob("*.png"))
    out = {"overlap_checks": {}, "proofreads": {}}
    for shot in shots:
        print(f"[vl-overlap] {shot.name} ...", flush=True)
        try:
            answer = ask(shot, OVERLAP_PROMPT)
        except Exception as exc:  # noqa: BLE001 — 单图失败不拦后续
            answer = f"FAILED: {exc!r}"
        out["overlap_checks"][shot.name] = answer
        print(f"  -> {answer}", flush=True)

    # verdict 两行(一级 0.30 置信)逐字校对
    drafts = {
        "01-verdict-ok.png": "• 一切正常 今日采集128条•5/5 源在线•推送成功5",
        "02-verdict-dead.png": "• 2个源失效 今日采集36条•3/6源在线•推送成功3",
    }
    for name, draft in drafts.items():
        print(f"[vl-proofread] {name} ...", flush=True)
        try:
            answer = ask(
                EVIDENCE / name,
                f"对照图片逐行校对此 OCR 初稿,只修正确有出入的字:{draft}",
            )
        except Exception as exc:  # noqa: BLE001
            answer = f"FAILED: {exc!r}"
        out["proofreads"][name] = {"draft": draft, "corrected": answer}
        print(f"  -> {answer}", flush=True)

    (EVIDENCE / "ocr-level2.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved ocr-level2.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

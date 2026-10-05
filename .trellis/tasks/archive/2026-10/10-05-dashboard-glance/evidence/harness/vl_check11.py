"""S7 补批 11- 二级核验(本机 mlx-vlm Qwen3-VL-8B,http://127.0.0.1:8080,零出网)。

一级 Vision 触发机械升级判据(8 图全部多行 ≤0.5)后按 local-ocr SKILL.md
第二级跑:① 全部 8 图:文字重叠/裁切/溢出定向检查;② 每图 ≤0.5 行的
OCR 初稿逐字校对(校对模式)。云端 glm-5.3-flash 已探死(429 1113 余额
不足,09-30 判例),不走向云。
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

# 每图一级 ≤0.5 行的初稿(取自 11-ocr-level1.txt;校对模式逐字复核)
DRAFTS = {
    "11-unified-window-7d-ok.png": [
        "• 一切正常 近7天采集164条•5/5源在线•推送成功5",
        "の近7天概览（UTC）",
        "近7 天采集",
        "～ 采集量趋势",
        "每日入库条目数（UTC 逐日；窗口随概览时间范围）",
        "近7天共164 条•峰值 128 条/日",
        "近7天累计成功率84%（38/45 次成功）",
        "刻度 0-100%",
    ],
    "12-unified-window-today-ok.png": [
        "• 一切正常",
        "：今日采集128条 •5/5源在线•推送成功5",
        "の今日概览（UTC）",
        "今日采集",
        "今日共128条•峰值 128条/日",
        "今日累计成功率 90%（9/10次成功）",
        "今日（UTC）",
    ],
    "13-verdict-dead.png": [
        "• 2个源失效 今日采集36条•3/6源在线•推送成功3",
    ],
    "14-source-collapse-default.png": [
        "源健康度 6个源•异常优先",
        "• 失效",
        "2 个源正常．展开",
        "• 退化",
        "• 未知",
    ],
    "15-source-collapse-expanded.png": [
        "源健康度 6个源•异常优先",
        "2个源正常•收起",
        "• 正常",
        "19 分钟前",
        "科技资讯•最近4条",
        "• 未知",
    ],
    "16-verdict-warning-cred.png": [
        "• 2项告警 今日采集128条•5/5源在线•推送成功5",
    ],
    "17-alert-cred-credentials.png": [
        "（ 今日概览（UTC）",
        "• 异常 凭据 一缺少 TG_TOKEN 凭据",
        "• 提醒 凭据 - mail 凭据30天内到期",
        "今日（UTC~",
    ],
    "18-verdict-unknown-doctorfail.png": [
        "• 部分数据不可达，状态未知 其余分区已降级显示•今日采集128条•推送成功5",
        "诊断/源健康度：核心内部错误—重试通常可恢复，持续出现请重启应用 【internal_error］",
        "（ 今日概览（UTC）",
        "诊断不可达．doctor 分区失败",
        "今日（UTC）",
    ],
}


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
    out = {"overlap_checks": {}, "proofreads": {}}
    for name in sorted(DRAFTS):
        shot = EVIDENCE / name
        print(f"[vl-overlap] {name} ...", flush=True)
        try:
            answer = ask(shot, OVERLAP_PROMPT)
        except Exception as exc:  # noqa: BLE001 — 单图失败不拦后续
            answer = f"FAILED: {exc!r}"
        out["overlap_checks"][name] = answer
        print(f"  -> {answer}", flush=True)

    for name, draft_lines in sorted(DRAFTS.items()):
        shot = EVIDENCE / name
        draft = " || ".join(draft_lines)
        print(f"[vl-proofread] {name} ...", flush=True)
        try:
            answer = ask(
                shot,
                "对照图片逐行校对这些 OCR 行(逐字,只输出与图有出入的字的修正,无出入则回答:全部一致):"
                + draft,
            )
        except Exception as exc:  # noqa: BLE001
            answer = f"FAILED: {exc!r}"
        out["proofreads"][name] = {"draft": draft, "corrected": answer}
        print(f"  -> {answer}", flush=True)

    (EVIDENCE / "11-ocr-level2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("saved 11-ocr-level2.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

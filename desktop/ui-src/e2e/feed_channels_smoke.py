#!/opt/homebrew/bin/python3
"""feed 渠道下钻无头冒烟(feed_channels_smoke)—— 10-06-feed-channel-groups。

程序化 UI 验证(主人令:UI 验证一律写程序,不许控制电脑):复用
package_smoke 的「同源 HTTP 桥(静态 dist + /rpc + /events SSE)+
__TAURI_INTERNALS__ shim」判例,零窗口零焦点。

对象:
  * UI = desktop/ui(vite 构建产物,与装机包同源树)
  * sidecar = **装机包内** Resources/myssia-src(/Applications/世事.app)
    经仓库 .venv 解释器 serve(自管 Python 布局;装机源,非开发树)
  * 数据 = MYIA_HOME 沙箱(五类渠道种子数据:telegram/RSS/urlwatch/
    prompt 日报/games 价格)

断言(三级下钻 + 分型 + 当日窗 + 实时滚动):
  1. L1 品类列表:置顶「全部条目 · 滚动流」+ 品类行(health 词汇源)+ 当日窗知会;
  2. L2 渠道列表:渠道行带类型词(频道/新闻/监控/日报/优惠)+ 窗内计数;
  3. L3 渠道流:store.items 带 category+source 精确等值(桥日志可证);
  4. 分型卡面:telegram 气泡 / watch「有更新」+目标页链接 / document markdown
     展开 / deal 价格行(¥0.00 + 限免 + 原价划线)/ news 列表;
  5. 面包屑回退:L3 → L2 → L1;
  6. 实时滚动:沙箱库直插新行 + visibilitychange 触发 liveRefresh → 新条目前插;
  7. 截图证据落 e2e/artifacts/feed-channels/(headless chromium 截图,非屏控)。

用法:.venv 解释器亦可,但 sidecar 一律用仓库 .venv(依赖齐):
    /opt/homebrew/bin/python3 desktop/ui-src/e2e/feed_channels_smoke.py

退出码:0 = 全部 PASS;1 = 任一 FAIL。沙箱纪律同 package_smoke(mkdtemp,
不碰真实数据根)。
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DESKTOP_UI = REPO / "desktop" / "ui"
BUNDLED_SRC = Path("/Applications/世事.app/Contents/Resources/myssia-src")
VENV_PY = REPO / ".venv" / "bin" / "python3"
ARTIFACTS = Path(__file__).resolve().parent / "artifacts" / "feed-channels"

# package_smoke 判例件(SidecarProcess / BridgeServer / SHIM_JS / chrome 探测)
_spec = importlib.util.spec_from_file_location("package_smoke", Path(__file__).with_name("package_smoke.py"))
ps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ps)  # type: ignore[union-attr]


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[bool, str, str]] = []

    def check(self, name: str, ok: bool, note: str = "") -> bool:
        self.items.append((ok, name, note))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {note}" if note and not ok else ""))
        return ok

    def summary(self) -> int:
        fails = [item for item in self.items if not item[0]]
        print(f"\n== feed_channels_smoke:{len(self.items) - len(fails)}/{len(self.items)} PASS ==")
        for _ok, name, note in fails:
            print(f"  FAIL {name} — {note}")
        return 1 if fails else 0


REPORT = Report()


class VenvSidecar(ps.SidecarProcess):  # type: ignore[misc]
    """自管 Python 布局的 sidecar:<venv python> -m myssia_desktop_entry serve,
    PYTHONPATH = 装机包内 myssia-src(装机源,协议面与本冒烟被测面一致)。
    不走父类 spawn(父类按「可执行文件 serve」两参形态),状态字段同构复制。"""

    def __init__(self, home: Path, stderr_path: Path) -> None:
        import os
        import subprocess as sp
        import threading

        env = {**os.environ, "MYIA_HOME": str(home), "PYTHONPATH": str(BUNDLED_SRC)}
        env.pop("MYIA_PLUGIN_DIR", None)
        self.stderr_path = stderr_path
        self._stderr = open(stderr_path, "wb")
        self.proc = sp.Popen(
            [str(VENV_PY), "-m", "myssia_desktop_entry", "serve"],
            stdin=sp.PIPE, stdout=sp.PIPE, stderr=self._stderr, env=env,
        )
        import queue as _queue

        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._pending: dict[int, dict | None] = {}
        self._next_id = 1
        self.event_queues: list[_queue.Queue[str]] = []
        self.non_json_lines = 0
        self._reader = threading.Thread(target=self._pump, daemon=True, name="sidecar-reader")
        self._reader.start()


def seed_extra_row(db: Path) -> None:
    """实时滚动验证用:沙箱库直插一条新 telegram 行(服务端视角 = 采集落地)。"""
    con = sqlite3.connect(db)
    con.execute(
        "INSERT INTO items (url, dedup_key, title, source, category, tags, first_seen, raw)"
        " VALUES (?, ?, ?, ?, ?, '[]', ?, NULL)",
        (
            "https://t.me/durov/999",
            "tg-durov-999",
            "实时滚动新到消息(冒烟)",
            "telegram-durov",
            "telegram-channels",
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    con.commit()
    con.close()


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    sandbox = Path(tempfile.mkdtemp(prefix="myia-smoke-feed-"))
    sandbox_db = sandbox / "myssia.db"
    # 种子:复制现成沙箱库(五类九行)而非重建
    shutil.copy2("/tmp/myia-smoke-feed-channels2/myssia.db", sandbox_db)
    (sandbox / "plugins").mkdir()
    for yaml in Path("/tmp/myia-smoke-feed-channels2/plugins").glob("*.yaml"):
        shutil.copy2(yaml, sandbox / "plugins" / yaml.name)
    print(f"沙箱 MYIA_HOME={sandbox}(独立 .instance.lock 域,不碰真根)")

    sidecar = VenvSidecar(sandbox, sandbox / "sidecar-stderr.log")
    bridge = ps.BridgeServer(DESKTOP_UI, sidecar)
    import threading

    thread = threading.Thread(target=bridge.serve_forever, daemon=True)
    thread.start()
    port = bridge.server_address[1]
    print(f"bridge http://127.0.0.1:{port}/(静态 {DESKTOP_UI};sidecar = 装机包源 + 仓库 venv)")

    from playwright.sync_api import sync_playwright

    chrome = ps.find_chrome()  # type: ignore[attr-defined]
    rc = 1
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=chrome)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        rpc_log: list[dict] = []
        # RPC 作用域证据:服务端侧包一层 request(不动 HTTP 体;断言 3 的证据)
        orig_request_method = type(sidecar).request

        def logged_request(self: ps.SidecarProcess, method: str, params: dict, timeout: float = 90.0) -> dict:
            if method == "store.items":
                rpc_log.append(dict(params))
            return orig_request_method(self, method, params, timeout)

        type(sidecar).request = logged_request  # type: ignore[assignment]

        page.add_init_script(ps.SHIM_JS)
        page.goto(f"http://127.0.0.1:{port}/index.html#/feed")
        page.wait_for_selector("[data-testid=\"feed-l1\"]", timeout=15_000)
        time.sleep(1.0)  # health/store.items 首轮到位

        # ── 1. L1 ──
        REPORT.check("L1-当日窗知会", page.locator("[data-testid=feed-day-window]").count() >= 1,
                     page.locator("[data-testid=feed-day-window]").all_inner_texts().__str__())
        all_row = page.locator("[data-testid=feed-drill-all]")
        REPORT.check("L1-置顶全局滚动流行", all_row.count() == 1, all_row.inner_text())
        for cat in ["telegram-channels", "ai-news", "ai-vendor-watch", "games", "wool"]:
            found = page.locator(f"[data-testid=feed-drill-cat-{cat}]").count() == 1
            REPORT.check(f"L1-品类行 {cat}", found,
                         page.locator("[data-testid^=feed-drill-cat-]").all_inner_texts().__str__())
        page.screenshot(path=str(ARTIFACTS / "01-l1-categories.png"))

        # ── 2. L2(ai-news)──
        page.click("[data-testid=feed-drill-cat-ai-news]")
        page.wait_for_selector("[data-testid=feed-l2]", timeout=10_000)
        page.wait_for_selector("[data-testid=feed-drill-ch-openai-news]", timeout=10_000)
        ch_news = page.locator("[data-testid=feed-drill-ch-openai-news]").inner_text()
        ch_watch = page.locator("[data-testid=feed-drill-ch-anthropic-news-watch]").inner_text()
        REPORT.check("L2-渠道行类型词(news=新闻)", "新闻渠道" in ch_news, ch_news)
        REPORT.check("L2-渠道行类型词(watch=监控)", "监控渠道" in ch_watch, ch_watch)
        REPORT.check("L2-品类批量入口在场", page.locator("[data-testid=feed-category-mark-all]").count() == 1)
        page.screenshot(path=str(ARTIFACTS / "02-l2-channels.png"))

        # ── 3. L3 urlwatch 渠道流 ──
        page.click("[data-testid=feed-drill-ch-anthropic-news-watch]")
        page.wait_for_selector("[data-testid=feed-l3]", timeout=10_000)
        page.wait_for_selector("text=Anthropic 新闻页 官网有更新", timeout=10_000)
        scoped = [params for params in rpc_log if params.get("source") == "anthropic-news-watch"]
        REPORT.check("L3-store.items 带 category+source 精确等值", bool(scoped)
                     and all(params.get("category") == "ai-news" for params in scoped), json.dumps(rpc_log[-3:]))
        badge = page.locator("[data-testid^=feed-watch-badge-]").first.inner_text()
        REPORT.check("分型-watch「有更新」徽标", "有更新" in badge, badge)
        target = page.locator("[data-testid^=feed-watch-target-]").first.inner_text()
        REPORT.check("分型-watch 目标页链接(watch_page 主机名)", "www.anthropic.com" in target, target)
        page.screenshot(path=str(ARTIFACTS / "03-l3-watch-channel.png"))

        # ── 5. 面包屑回退 L3→L2→L1 ──
        page.click("[data-testid=feed-crumb-category]")
        page.wait_for_selector("[data-testid=feed-l2]", timeout=10_000)
        page.click("[data-testid=feed-crumb-home]")
        page.wait_for_selector("[data-testid=feed-l1]", timeout=10_000)
        REPORT.check("面包屑回退 L3→L2→L1", True)

        # ── 4. telegram 气泡 ──
        page.click("[data-testid=feed-drill-cat-telegram-channels]")
        page.wait_for_selector("[data-testid=feed-drill-ch-telegram-durov]", timeout=10_000)
        tg_text = page.locator("[data-testid=feed-drill-ch-telegram-durov]").inner_text()
        REPORT.check("L2-telegram 渠道类型词(频道)", "频道渠道" in tg_text, tg_text)
        page.click("[data-testid=feed-drill-ch-telegram-durov]")
        page.wait_for_selector("[data-testid=feed-l3]", timeout=10_000)
        page.wait_for_selector("[data-testid^=feed-tg-bubble-]", timeout=10_000)
        bubble = page.locator("[data-testid^=feed-tg-bubble-]").first.inner_text()
        REPORT.check("分型-telegram 消息气泡(正文在泡内)", "Telegram 消息" in bubble, bubble[:80])
        ch_name = page.locator("[data-testid^=feed-item-] .text-2xs.font-medium").first.inner_text()
        REPORT.check("分型-telegram 频道名(去平台前缀)", ch_name.strip() == "durov", ch_name)
        page.screenshot(path=str(ARTIFACTS / "04-l3-telegram-bubble.png"))

        # ── 4. document 日报 markdown ──
        page.click("[data-testid=feed-crumb-home]")
        page.wait_for_selector("[data-testid=feed-drill-cat-ai-vendor-watch]", timeout=10_000)
        page.click("[data-testid=feed-drill-cat-ai-vendor-watch]")
        page.wait_for_selector("[data-testid=feed-drill-ch-ai-vendor-watch]", timeout=10_000)
        doc_ch = page.locator("[data-testid=feed-drill-ch-ai-vendor-watch]").inner_text()
        REPORT.check("L2-日报渠道类型词", "日报渠道" in doc_ch, doc_ch)
        page.click("[data-testid=feed-drill-ch-ai-vendor-watch]")
        page.wait_for_selector("text=AI 厂商日报(演示)", timeout=10_000)
        doc_card = page.locator("[data-kind=document]").first
        doc_card.get_by_role("button", name="展开条目").click()
        page.wait_for_selector("[data-testid^=feed-doc-body-]", timeout=10_000)
        doc_body = page.locator("[data-testid^=feed-doc-body-]").first.inner_text()
        REPORT.check("分型-document markdown 展开(标题/列表/加粗)",
                     "今日要点" in doc_body and "OpenAI 发布新模型" in doc_body, doc_body[:80])
        page.screenshot(path=str(ARTIFACTS / "05-l3-document-markdown.png"))

        # ── 4. deal 价格行 ──
        page.click("[data-testid=feed-crumb-home]")
        page.wait_for_selector("[data-testid=feed-drill-cat-games]", timeout=10_000)
        page.click("[data-testid=feed-drill-cat-games]")
        page.wait_for_selector("[data-testid=feed-drill-ch-epic-free]", timeout=10_000)
        page.click("[data-testid=feed-drill-ch-epic-free]")
        page.wait_for_selector("text=Epic 演示限免游戏", timeout=10_000)
        price = page.locator("[data-testid^=feed-deal-price-]").first.inner_text()
        REPORT.check("分型-deal 价格行(¥0.00 + 限免 + 原价划线)",
                     "¥0.00" in price and "限免" in price and "¥39.00" in price, price)
        page.screenshot(path=str(ARTIFACTS / "06-l3-deal-price.png"))

        # ── 6. 实时滚动:沙箱直插新行 + visibilitychange → liveRefresh ──
        page.click("[data-testid=feed-crumb-home]")
        page.wait_for_selector("[data-testid=feed-drill-cat-telegram-channels]", timeout=10_000)
        page.click("[data-testid=feed-drill-cat-telegram-channels]")
        page.click("[data-testid=feed-drill-ch-telegram-durov]")
        page.wait_for_selector("[data-testid=feed-l3]", timeout=10_000)
        seed_extra_row(sandbox_db)
        page.evaluate(
            """() => {
              Object.defineProperty(document, "hidden", { configurable: true, get: () => false });
              document.dispatchEvent(new Event("visibilitychange"));
            }"""
        )
        try:
            page.wait_for_selector("text=实时滚动新到消息(冒烟)", timeout=10_000)
            REPORT.check("实时滚动-新条目前插进流(visibilitychange → liveRefresh)", True)
        except Exception:
            REPORT.check("实时滚动-新条目前插进流(visibilitychange → liveRefresh)", False,
                         "10s 内未见新行(检查 sidecar 日志 " + str(sandbox / "sidecar-stderr.log") + ")")
        page.screenshot(path=str(ARTIFACTS / "07-live-refresh.png"))

        browser.close()
        rc = REPORT.summary()
    bridge.shutdown()
    sidecar.close()
    print(f"沙箱留存(排查用):{sandbox}")
    return rc


if __name__ == "__main__":
    sys.exit(main())

<div align="center">

<img src="desktop/branding/myssia-icon-1024.png" width="160" alt="世事 — 眼睛与雷达虹膜" />

# myssia(中文名:世事)

**AI 原生情报中枢 · AI-native intelligence hub**

**说需求,AI 做其余。** · Say what you want — AI does the rest.

<p>
<a href="https://github.com/xinzhuzi/myia/actions/workflows/ci.yml"><img src="https://github.com/xinzhuzi/myia/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
<img src="https://img.shields.io/badge/tests-1300%2B%20passing-2EA44F" alt="tests: 1300+ passing" />
<img src="https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white" alt="python 3.11+" />
<img src="https://img.shields.io/badge/license-MIT-3DA639" alt="MIT license" />
<img src="https://img.shields.io/badge/status-0.0.1%20first%20release-2EA44F" alt="status: v0.0.1 first release" />
</p>
<p>
<img src="https://img.shields.io/badge/fetch%20engines-6%20(L1%E2%80%93L6)-22D3EE" alt="6 fetch engines, L1–L6" />
<img src="https://img.shields.io/badge/push-Feishu%20%C2%B7%20Telegram%20%C2%B7%20webhook%20%C2%B7%20stdout-8B5CF6" alt="push: Feishu · Telegram · webhook · stdout" />
<img src="https://img.shields.io/badge/weight-SQLite%20single%20file%20%C2%B7%20no%20daemon-64748B" alt="SQLite single file, no daemon" />
</p>

<img src="docs/demo/assets/shishi-demo.gif" width="800" alt="世事 demo:一个 YAML → 情报推送(录制于 shishi 命名时期,物料为时代锁定原样保留;现 CLI 为 myssia run → 收到推送卡片)" />

<sub>世事 三分钟 —— 一个 YAML → 情报推送。录制脚本与分镜:<a href="docs/demo/"><code>docs/demo/</code></a></sub>

<br/>
<br/>

<code>fetch</code> ➜ <code>classify</code> ➜ <code>dedup</code> ➜ <code>analyze</code> ➜ <code>enrich</code> ➜ <code>push</code>

<br/>
<br/>

**[中文](README.md)** · **English**

</div>

---

## The idea

Every intelligence need — AI news, stock moves, restocks, GPU prices,
freebies and deals — has the same shape: **watch some sources, keep what
matters, ignore the rest, tell me when it counts.** Existing tools each give
you one slice: a crawler, a feed, a diff watcher. 世事 is the whole chain,
config-driven, and built to be driven by your AI agent.

Describe any category as **one YAML file**. 世事 fetches it (six engines on
an auto-degrading ladder), classifies and dedups it, scores it (keywords
first — zero tokens; optional LLM for precision), and pushes what matters to
your messaging apps. The YAML itself is written by your coding agent: it
reads the schema, generates the config, trial-fetches with `myssia test`, and
repairs broken sources on its own from `myssia doctor` output.

Weixin outbound is a bridge via a local Hermes-Agent install — without one,
the weixin channel is unavailable (myssia itself holds zero WeChat credentials).

**Humans decide; AI does the rest.**

## Why 世事

| Existing tools | What they give you | What they miss |
|---|---|---|
| Crawlab / Kestra | crawler & workflow orchestration | a vehicle only — no classification, dedup or push |
| changedetection.io | website change monitoring | watches diffs — no collection pipeline, no analysis, no LLM scoring |
| RSSHub | turns sites into RSS feeds | source conversion only — no filtering, scoring or delivery |
| Single-purpose watchers (credential / deal trackers) | one niche category each | category-locked; every new target means new tooling |
| **世事** | **category-agnostic fetch → classify → analyze → push, all config-driven** | — |

## Highlights

<table>
<tr>
<td width="50%" valign="top">

🧠 **Intelligence, not just crawling**
A seven-category keyword classifier (zero tokens, shipped as the standalone
[`myssia-classifier`](myssia-classifier/) package) plus optional LLM enrichment
scoring value / relevance / credibility 0–10. Thresholds route the result:
score ≥ 8 pushes immediately, ≥ 5 waits for the AM/PM digest, the rest is
archived.

</td>
<td width="50%" valign="top">

🪜 **A six-engine fetch ladder**
`direct_api` → `static_html` → `crawl4ai` / `firecrawl` → `Scrapling` →
stealth browser → LLM browser. Sources never hard-code an engine: when one
rung fails, the next takes over, and the winning engine is remembered per
source (in SQLite — never written back into your YAML).

</td>
</tr>
<tr>
<td width="50%" valign="top">

📬 **Push that respects your attention**
URL-key dedup registry + AM/PM digest slots — production-proven semantics;
you never receive the same item twice. Feishu card, Telegram, webhook and
stdout channels.

</td>
<td width="50%" valign="top">

🔐 **Secrets stay secret**
Credentials never live in YAML — only `env:VAR` / `keychain:myia/<scope>/<name>`
references. A plaintext credential in a config file is rejected at load time.
macOS Keychain / Windows DPAPI backed.

</td>
</tr>
<tr>
<td width="50%" valign="top">

🤖 **Agent-native by design**
A fully documented 12-section YAML schema with defaults everywhere,
`--json` on every command (stdout is always exactly one JSON document),
structured diagnostics. Every interface is built so an agent can drive it —
not just a human.

</td>
<td width="50%" valign="top">

🔁 **A feedback loop that tunes itself**
Mark pushed items valuable / not valuable (CLI today; in-card desktop
buttons have landed on main in the desktop-parity batch and ship with the
next release; Telegram/Feishu callback receivers are ready) —
negative feedback retunes watchlist weights and thresholds over time.

</td>
</tr>
<tr>
<td colspan="2" width="100%" valign="top">

⏰ **Scheduled jobs: run it on a clock, deliver the summary**
`myssia cron serve` daemon, the desktop app's built-in ticker, or a manual
`cron tick` from system crontab — one substrate coexisting under a tick
file lock + fire claims. Each due fire runs the category pipeline once and
delivers the run summary (local archive / Feishu / Telegram and other
platform specs). Schedules take natural language (`every monday 9am`) or
5-field cron (POSIX dow).

</td>
</tr>
</table>

Batteries included: SQLite single-file storage (no Redis, no Postgres, no
daemon), retention + auto-VACUUM, in-process scheduling.

## Quickstart

```bash
git clone https://github.com/xinzhuzi/myia
cd myssia
uv sync                     # uv workspace (primary): installs myssia + myssia-classifier
uv run myssia --version       # myssia 0.0.1
```

> This repo is a uv workspace (`myssia-classifier` is a workspace member): a bare
> `pip install -e .` won't pull it in — install from source with `uv sync`;
> `pip install myssia` becomes available once the package lands on PyPI.

Heavy fetch engines are optional extras; a missing engine degrades gracefully
down the ladder with a structured `dependency_missing` error instead of
crashing:

```bash
uv sync --extra crawl4ai    # L3 JS-rendered page engine
uv sync --extra llm         # LLM enrich scoring / event aggregation
uv sync --extra table       # table restore (rapid_table: screenshot tables → metadata.tables)
uv sync --extra trafilatura # L2 article fallback (single-page body extraction for rule-less/revamped sources, MYIA_EXTRACT_FALLBACK=1 to enable)
```

Table restore is the first **optional component** for the managed Python
environment: on the desktop, the "table restore" switch under
Settings → Python environment installs the pinned component into the managed
environment (no repackaging, mirror overrides apply); categories opt in with
`images.table: true`. CLI-side that's the `--extra table` above. A missing
component never blocks the pipeline (it only degrades, writing
`metadata.table_status`), and `myssia doctor` discloses it ahead of time as
`table_dependency_missing`.

The trafilatura article fallback likewise never blocks when missing
(rule-less sources keep the `extract_required` degrade-chain behavior), and
installing it only provides the capability — `MYIA_EXTRACT_FALLBACK=1` must
be set explicitly (CLI: env prefix on the command line; installed app:
`launchctl setenv MYIA_EXTRACT_FALLBACK 1` then restart; off by default =
zero behavior change for existing sources; see
[getting started](docs/en/getting-started.md)).

Beyond the global env the switch can also be **overridden per source**:
`engine_options.static_html.extract_fallback: true/false` in category YAML
takes precedence over the global variable (precedence = source-level > global
`MYIA_EXTRACT_FALLBACK` > off by default; with the key unset, behavior is
byte-identical to the global setting) — full details in the `extract` row of
the [schema reference](docs/en/schema.md).

### Self-hosted Firecrawl fallback (optional L3 rendering backend)

The L3 `firecrawl` engine's rendering backend doesn't have to be a cloud
purchase — a self-hosted stack works too (zero dollars, and rendering
traffic never leaves your machine): deployment steps and the recipe live
in the upstream official [self-host guide](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md)
(we do not replicate the recipe here). The engine's built-in default endpoint is
the standard port `http://127.0.0.1:3002`; set `MYIA_FIRECRAWL_URL` only for
a non-standard port or a remote machine. Self-host runs with auth off, so
`MYIA_FIRECRAWL_API_KEY` stays unset (only the `api.firecrawl.dev` cloud
needs a key). The upstream server is AGPL-3.0 — 世事 consumes it purely as
a service (HTTP API calls, zero source copying, same as the RSSHub
precedent) and never vendors its code; hard anti-bot bypass / screenshots
and other Fire-engine capabilities are cloud-only and absent from the
self-hosted stack. 世事-side wiring (the cloud / self-host endpoint
three-level resolution and the degrade chain), the cloud-only gap list and
the historical verification receipt live in [zero-cost setup §4](docs/en/zero-cost.md).

Run your first category — a complete, zero-credential config in one small
file:

```bash
cat > plugins/demo-min.yaml <<'YAML'
id: demo-min
name: Minimal demo
schedule: "0 9 * * *"
sources:
  - name: example-news
    engine: static_html
    url: "https://example.com/news"
    extract:
      type: list
      item: "article"
      fields:
        title: "h2 a"
        url: "h2 a@href"
classify:
  builtin: false                 # demo items match no category; disable the filter
push:
  - channel: stdout              # zero-credential local verification
YAML

uv run myssia test plugins/demo-min.yaml --json            # trial fetch: no DB, no push
uv run myssia run plugins/demo-min.yaml --dry-run --json   # full rehearsal, no push
uv run myssia run plugins/demo-min.yaml                    # real run; add --loop for scheduling
```

Full walk-through: [docs/en/getting-started.md](docs/en/getting-started.md).

> PyPI packages (`myssia`, `myssia-classifier`) will publish via a manual release
> workflow; until then, install from source as above — or grab the desktop
> installer below.

## Download & install (desktop app)

The macOS (Apple Silicon) installer ships via GitHub Releases:

1. Download `myssia_<version>_aarch64.dmg` from
   [Releases](https://github.com/xinzhuzi/myia/releases) (the version token
   rotates per release — the Releases page is authoritative) and drag 世事 into
   Applications;
2. On first launch: **right-click 世事 in Applications → Open → Open**
   (or, after a blocked double-click: System Settings → Privacy & Security →
   Open Anyway);
3. The package is not Apple-notarized (notarization requires a paid developer
   account) — the code is fully open-source and auditable, and every installer
   is built in public by GitHub Actions with traceable logs. One right-click
   open clears Gatekeeper; subsequent launches open normally;
4. **First-time Python runtime setup**: the runtime and dependencies do not
   ship inside the installer (which keeps it much smaller) — after launching,
   open Settings → Python environment and click "Start setup" to download the
   pinned runtime
   ([indygreg/python-build-standalone](https://github.com/indygreg/python-build-standalone)
   `cpython-3.12.7+20241016`, sha256 pinned by the bundled manifest) and
   install the locked dependency list into `python/` under the data root.
   Both the runtime download URL and the PyPI index can be overridden with
   mirrors in settings (address only — the check is never bypassed); the
   first setup needs network. See
   [Getting started §1.1](docs/en/getting-started.md).

On Windows (x64) the flow is the same: the msi installer (shipping via
Releases — see the roadmap note) downloads the `x86_64-pc-windows-msvc`
equivalent of the same pinned runtime on first setup; the data root is
`%APPDATA%\MYIA` with the managed Python under `python\`; upgrades go through
"Check for updates" (silent passive msi install + restart, see
[desktop/UPDATER.md](desktop/UPDATER.md)) — data carries over untouched and a
one-time banner walks you to settings for the single setup.

Once the Python environment is configured, a fresh install auto-seeds the
official plugins (including the zero-credential demo `myssia-demo`: GitHub's
new-star board), so the first click of "run your first plugin" shows real
data; the settings screen offers "Check for updates" over a signed update
channel, and when an app update changes the dependency list the same section
grows a one-click "Sync dependencies" action (idempotent — installed packages
are skipped).

The five desktop screens (fed by real demo-plugin data):

<p align="center">
<img src="docs/screenshots/dashboard.png" width="400" alt="Dashboard: plugin run status and recent collection overview" />
<img src="docs/screenshots/feed.png" width="400" alt="Feed: deduplicated intelligence items" />
</p>
<p align="center">
<img src="docs/screenshots/sources.png" width="260" alt="Sources: plugin and source configuration" />
<img src="docs/screenshots/logs.png" width="260" alt="Logs: run log tail" />
<img src="docs/screenshots/settings.png" width="260" alt="Settings: credentials into the keychain + software update" />
</p>

## The AI-native loop

Hand the loop to any coding agent (Claude Code, Cursor, …). The
[Agent Skill](skill/SKILL.md) is a self-contained cheat sheet, installed with
one command (`myssia skill install --agent claude`; also `cursor` / `zcode`,
`--path` for a custom dir, `--link` to symlink instead of copy):

```
myssia skill install --agent claude         # one-time: skill sheet → ~/.claude/skills/myia/
myssia init --json                          # structured checklist of what to collect
( agent writes <id>.yaml )                # against the 12-section schema
myssia test plugins/<id>.yaml --json        # trial fetch, inspect fields + dedup keys
myssia run plugins/<id>.yaml --dry-run      # rehearsal
myssia run plugins/<id>.yaml --loop         # scheduled operation
myssia doctor --json                        # findings; the agent repairs and re-checks
```

## Architecture

```
User layer      myssia CLI · Agent Skill · desktop app (Tauri, v1.1) · Web UI (planned)
                     │
Orchestration   Pipeline: fetch → classify → dedup → analyze → enrich → push
                (in-process APScheduler + asyncio; no external orchestrator, no daemon)
                     │
Plugin layer     One YAML per category · 7 official categories · market plugins
                desktop tier = in-process adapter (zero docker) · remote/server tier
                (proxy pool · changedetection · OSINT · douyin · maxun · …)
                     │
Fetch engines   L1 direct_api → L2 static_html → L3 crawl4ai ⇄ firecrawl
                → L4 scrapling → L5 stealth_browser → L6 llm_browser
                (auto degrade chain; winning engine persisted per source)
                     │
Analysis        builtin 7-category keyword classifier (myssia-classifier)
                + optional LLM enrich (value / relevance / credibility, 0–10)
                     │
Storage         SQLite single file · retention + VACUUM · change baselines
                     │
Push            Feishu card · Telegram · webhook · stdout, threshold-routed
                (immediate / digest AM-PM / archive) + feedback loop
```

## Documentation

Bilingual docs ship in-repo, kept consistent with the code by tests
(`tests/test_docs.py`) — every example YAML loads through the real schema
entry point, and zh/en trees cannot drift apart:

| | English | 中文 |
|---|---|---|
| Getting started | [docs/en/getting-started.md](docs/en/getting-started.md) | [docs/zh/getting-started.md](docs/zh/getting-started.md) |
| Write a plugin | [docs/en/write-a-plugin.md](docs/en/write-a-plugin.md) | [docs/zh/write-a-plugin.md](docs/zh/write-a-plugin.md) |
| Schema reference | [docs/en/schema.md](docs/en/schema.md) | [docs/zh/schema.md](docs/zh/schema.md) |
| FAQ (ethics & boundaries) | [docs/en/faq.md](docs/en/faq.md) | [docs/zh/faq.md](docs/zh/faq.md) |
| Scheduled jobs (cron) | [docs/en/cron.md](docs/en/cron.md) | [docs/zh/cron.md](docs/zh/cron.md) |

Agent-facing condensed reference: [`skill/SKILL.md`](skill/SKILL.md).

## Roadmap

The core pipeline is implemented and tested — 1300+ tests run in CI, none of
them touch the real network. The desktop app is ready for daily use
(unified data paths, bundled official plugins, an out-of-the-box demo, a
signed update channel — shipping in Releases since v0.0.1); in-card
feedback buttons, the settings feedback toggle and collection trends have
landed on main in the desktop-parity batch and ship with the next release
(the feedback loop already works via CLI); the Windows build did not ship
in this release (no Windows installer in Releases yet; planned for a
follow-up batch).

| Milestone | Scope | Status |
|---|---|---|
| v0.1 skeleton | Core pipeline, direct_api/static/firecrawl engines, 12-section schema, change fingerprint, classifier, Feishu routing | ✅ shipped |
| v0.2 usable | SQLite store + registry + retention, full CLI (init/test/list/doctor), crawl4ai L3, LLM enrich + budget guardrails, docker compose, Telegram, keychain secrets | ✅ shipped |
| v0.3 ecosystem | Agent Skill, plugin market (local/remote dual-mode), Scrapling L4, feedback loop (CLI + callback receivers) | ✅ shipped |
| v0.4 deep water | stealth_browser L5, llm_browser L6, trend baselines, event aggregation | ✅ shipped |
| v1.0 launch | Bilingual docs, demo assets, GitHub facade, public delivery | ✅ shipped |
| v1.1 desktop-first | Tauri desktop shell (Python core as sidecar), five-screen UI, in-process plugin tier; in-card feedback buttons / settings feedback toggle / collection trends have landed in the desktop-parity batch and ship with the next release (feedback works via CLI today) | ✅ shipped |
| v1.1.1 data paths | Desktop data-path unification (MYIA_HOME / bundled official plugins / first-run seed), out-of-the-box demo plugin, signed update channel (check + install) | ✅ shipped |
| Web UI | browser front-end on the same core | 📋 planned |

## Ethics & boundaries

世事 is polite by default: robots.txt respected, rate-limited fetching,
credentials never in plaintext. Sources that demand human verification
(CAPTCHA, phone numbers) fail with a structured error — 世事 does not attempt
to bypass them. Full statement in the
[FAQ](docs/en/faq.md) · [中文 FAQ](docs/zh/faq.md).

## Community

- Bug reports & feature requests: [issue templates](.github/ISSUE_TEMPLATE/)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy & credential-handling design: [SECURITY.md](SECURITY.md)

## Acknowledgments

世事's own code is original (MIT), but it stands on giants — consumed as
dependencies, plugin backends and design references:

- [crawl4ai](https://github.com/unclecode/crawl4ai) — L3 fetch engine (optional dependency)
- [Scrapling](https://github.com/D4Vinci/Scrapling) — L4 adaptive anti-bot engine (optional dependency)
- [Firecrawl](https://github.com/firecrawl/firecrawl) — L3 cloud/self-hosted rendering backend (optional dependency, called as an API)
- [Skyvern](https://github.com/Skyvern-AI/skyvern) — L6 LLM-browser fallback (optional dependency)
- [rapid-table](https://github.com/RapidAI/RapidTable) (RapidAI family) — table-restore component (optional dependency, `myssia[table]`)
- [trafilatura](https://github.com/adbar/trafilatura) — L2 article-fallback component (optional dependency, `myssia[trafilatura]`, switch `MYIA_EXTRACT_FALLBACK`)
- [changedetection.io](https://github.com/dgtlmoon/changedetection.io) — source-management & diff UX reference; `myssia-monitor` plugin backend
- [RSSHub](https://github.com/DIYgod/RSSHub) — the "everything is a feed" philosophy
- [jhao104/proxy_pool](https://github.com/jhao104/proxy_pool) — `myssia-proxy` plugin backend
- [Photon](https://github.com/s0md3v/Photon) — `myssia-osint` plugin backend (vendored via git submodule)
- [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) — `myssia-douyin` plugin backend
- [Maxun](https://github.com/getmaxun/maxun) — `myssia-maxun` plugin backend
- [Tauri](https://github.com/tauri-apps/tauri) — desktop shell (Python core embedded as a sidecar)

No upstream source is copied into this repository except clearly-marked git
submodules; dependency policy in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 xinzhuzi

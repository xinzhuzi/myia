# Getting Started

> Run your first category in three minutes: install → credentials → trial
> fetch → real run → where the data lands.
> Then continue with the [plugin guide](write-a-plugin.md) and the
> [schema reference](schema.md); see the [FAQ](faq.md) for crawling ethics
> and boundaries.
> Building the desktop app from source (Windows MSI): see
> [Windows local build](build-windows.md).

## 1. Install

### 1.1 Desktop app (recommended)

Grab the desktop installer (macOS dmg / Windows msi) from
[Releases](https://github.com/xinzhuzi/myia/releases). **The Python runtime
and third-party dependencies do not ship inside the installer** (which keeps
it much smaller): on first launch open **Settings → Python environment** and
click "Start setup" — the app then installs a self-managed environment
online, with every step visible and retryable:

- The install chain has five steps: **download → sha256 verify → extract into
  the data root → pip install the locked dependency list → self-check
  handshake**, each lit up on the settings page. If it fails mid-way (offline,
  corrupt archive) a retry skips the steps already completed (idempotent
  resume) — you never start from scratch.
- The runtime is **pinned** to
  [indygreg/python-build-standalone](https://github.com/indygreg/python-build-standalone)
  `cpython-3.12.7+20241016` (install_only build, sha256 pinned by the bundled
  manifest — a mirror cannot bypass the check). It lands in `python/` under
  the data root (macOS `~/Library/Application Support/MYIA/python/`, Windows
  `%APPDATA%\MYIA\python\`), never in the install directory.
- **Both mirrors are overridable** (friendly for slow or restricted networks):
  the settings page can replace the runtime download URL and the PyPI index
  (e.g. `https://pypi.tuna.tsinghua.edu.cn/simple`) at the same time. A mirror
  only changes where bytes come from — the pinned version and the sha256
  check stay in force.
- The first setup needs network and ~500 MB of free disk. Until the
  environment is ready every screen shows a "Python runtime not configured"
  guide — **nothing downloads in the background**; once setup completes the
  core process starts automatically.
- Upgrading from an older version: your database / plugins / models / keychain
  credentials carry over untouched (zero migration); a one-time banner on
  first launch walks you to settings for that single setup. Later app updates
  that change the dependency list surface a "Sync dependencies" button in the
  same section — one idempotent click.

Once the environment is ready, categories on the desktop run in exactly the
same shape as the CLI — one YAML file (official plugins are auto-seeded,
including the zero-credential demo `myssia-demo`: GitHub's new-star board,
abridged below):

```yaml
id: myssia-demo
name: Demo · GitHub new stars
schedule: "0 9 * * *"
sources:
  - name: github-new-stars
    engine: direct_api
    url: "https://api.github.com/search/repositories?q=created:%3E2026-09-01&sort=stars&order=desc&per_page=30"
    extract:
      type: json_path
      fields:
        title: "$.items[*].full_name"
        url: "$.items[*].html_url"
push:
  - channel: stdout              # zero-credential channel; runs out of the box once configured
```

### 1.2 From source (CLI / development)

世事 is a pure-Python package (Python 3.11+) with zero heavy core
dependencies. Note: the root package depends on the in-repo subpackage
`myssia-classifier` (a uv workspace member, not published to PyPI), so
installing from source requires `uv sync` — a bare `pip install -e .`
cannot resolve that dependency and fails outright:

```bash
git clone https://github.com/xinzhuzi/myia
cd 世事
uv sync                     # the only from-source install (workspace deps resolve via uv alone)
uv run myssia --version       # prints myssia x.y.z (the installed version)
```

Heavy fetch engines are optional extras. When one is missing the pipeline
raises a structured `dependency_missing` error and keeps going down the
degrade chain — it never crashes the run:

```bash
uv sync --extra crawl4ai    # L3 JS-rendered page engine
uv sync --extra llm         # enrich scoring / aggregate event merging (openai client)
```

There are five extras in total: `crawl4ai` / `scrapling` / `firecrawl` /
`skyvern` / `llm`. For an always-on server deployment use the compose form:
`docker compose -f docker/docker-compose.yml up -d` (see
`docker/README.md`).

## 2. Configure credentials

世事 **never accepts plaintext credentials in YAML** — you write references
that are resolved at run time:

- `env:VAR_NAME` — read from the environment at run time;
- `keychain:myia/<scope>/<name>` — read from the OS keychain (macOS
  Keychain / Windows DPAPI). The namespace is canonical: store the value
  first with `myssia secret set`, then reference it in YAML. Flat legacy
  names (e.g. `keychain:linuxsb_cookie`) are refused at resolve time.

```bash
# Push channel (Feishu bot; for Telegram it is TELEGRAM_CHAT_ID / TELEGRAM_BOT_TOKEN)
export FEISHU_CHAT_ID=...
export FEISHU_BOT_TOKEN=...

# LLM scoring endpoint (OpenAI-compatible; 世事 has no built-in endpoint, no default key)
export MYIA_LLM_BASE_URL=...
export MYIA_LLM_KEY=...

# Credentials that should not live in the environment (e.g. a site cookie)
# go into the keychain: pipe the value over stdin — never pass it as a
# command-line argument (it would land in shell history and process lists)
myssia secret set myia/stocks/site_cookie < cookie.txt
```

The Weixin channel is an optional bridge: outbound goes through a local
resident Hermes-Agent install that holds the login — without one, that
platform is unavailable (myssia stores zero WeChat credentials; the platform
card honestly says "needs a local Hermes").

Don't want to configure a paid endpoint? Both vision and enrich have
zero-cost paths (local mlx-vlm/Ollama → cloud free tiers → light Gemini
daily batches); see [Zero-cost setup](zero-cost.md) for endpoint choices
and the quota snapshot.

Misconfiguration needs no guesswork: `myssia doctor --json` probes every
reference for existence (is the env var set / is the keychain name present)
and turns a missing one into a concrete repair action (e.g. run
`myssia secret set ...`).

## 3. Run your first category

A minimal category with zero credentials and zero cost — save this as
`plugins/demo-min.yaml` (point `url` at any server-rendered list page):

```yaml
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
  builtin: false                 # demo items match none of the seven built-in categories
push:
  - channel: stdout              # zero-credential local verification; every other field defaults
```

Three commands cover verify → rehearse → run:

```bash
uv run myssia test plugins/demo-min.yaml --json            # trial-fetch each source, no push/storage
uv run myssia run plugins/demo-min.yaml --dry-run --json   # full rehearsal, no push
uv run myssia run plugins/demo-min.yaml                    # the first real run
```

- `myssia test --json` reports per source: `ok` (did the chain get data),
  `engine` (the engine actually chosen), `items[].fields` (extracted-field
  preview) and `fingerprint.verdict` (`unchanged_skip` = content unchanged,
  normal; `changed_or_first_fetch` = items will be extracted).
- `myssia run --json` reports `stages[]` (fetch/classify/dedup/analyze/push
  items_in→items_out with skip reasons) and `pushes[]` (route buckets and
  send results).
- For long-term use add `--loop`: resident scheduling by the YAML's
  `schedule` + `timezone`. **Note** (one bot token = one poller): every
  resident process configured with a `telegram` channel polls the same
  `getUpdates` stream (the bot token always comes from
  `env:TELEGRAM_BOT_TOKEN`), and Telegram answers concurrent pollers with
  409 Conflict — keep at most one `--loop` category per token and move the
  other categories to other push channels; `myssia doctor` flags shared
  setups as `telegram_token_poll_conflict`.

The official categories in the repo (freebies / stocks / AI news / GPU
prices, …) work the same way, e.g. `uv run myssia run plugins/wool.yaml`;
every credential slot in an official plugin is already an `env:` /
`keychain:` reference — prepare the values as in section 2.

Or just tell an AI agent what you want — it reads the
[plugin guide](write-a-plugin.md) (condensed version:
[skill/SKILL.md](../../skill/SKILL.md)), generates the category YAML, and
verifies and runs it with the same commands.

## 4. Where data lives

Everything is stored in a single SQLite file (default `./myssia.db`, override
with `--db`): fetched items, the dedup registry, change baselines and
numeric history, push feedback, run history and per-source health.
`storage.retention` in the plugin YAML controls the retention window (expired
items are purged automatically) and `storage.vacuum` the VACUUM cadence;
categories declaring `baseline:` keep their numeric history for twice the
item retention (so the "vs last week" window stays complete).

## 5. Next steps

- [Plugin guide](write-a-plugin.md): the full path from a natural-language
  request to a running YAML — same source as
  [skill/SKILL.md](../../skill/SKILL.md).
- [Schema reference](schema.md): the twelve sections field by field, plus
  the v0.3/v0.4 sidecar sections (`plugin:` scenario plugin / `baseline:`
  trend baseline / `aggregate:` event aggregation).
- [FAQ](faq.md): crawling ethics and boundaries (robots.txt, captchas,
  human-verification walls), credential safety, and self-repair paths for
  common failures.
- [Zero-cost setup](zero-cost.md): the free LLM endpoint guide — local
  mlx-vlm/Ollama (the default) → cloud free tiers (Zhipu free models,
  OpenRouter `:free`) → light Gemini daily batches, with the quota
  snapshot and per-vendor wiring steps.
- Feedback loop: the "valuable / not valuable" buttons on pushed cards feed
  back and keep tuning; the CLI equivalents are
  `myssia feedback list / stats / mark`.

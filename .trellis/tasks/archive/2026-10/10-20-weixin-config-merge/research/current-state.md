# 现状实证(2026-10-20 主会话排查;同日 grill 深化补全)

> 来源:主人问「微信监控配置里有 4 个,配置文档里只看到 1 个」。全部为当场实测,非推断。
> grill 轮补全的实证以 **[G]** 标注。

## 数据根四档实况(`~/Library/Application Support/MYIA/config/`)

| 文件 | 品类 id / name | schedule(yaml 蓝本) | 装机 job 实跑 expr **[G]** | 源(name 逐字) |
|---|---|---|---|---|
| `weixin.yaml` | weixin / 微信监控 | `*/30 * * * *` | `*/2 9-22 * * *`(job 0e9f2daf2d6a) | `weixin-TMS 中转站交流`(localdb,chat: `50438708676@chatroom`) |
| `weixin-ai-token.yaml` | weixin-ai-token / 微信AI中转站 | `*/2 9-22 * * *` | `*/2 9-22 * * *`(job 897e224ef024) | `weixin-AI中转站-♾️ AI Token`(localdb,chat: `48114732647@chatroom`) |
| `weixin-sns.yaml` | weixin-sns / 微信朋友圈 | `*/5 * * * *` | `*/5 * * * *`(job 90ae9c28788e) | `weixin-朋友圈`(sns,feed_kind: feed)、`weixin-朋友圈互动`(sns,feed_kind: notices) |
| `weixin-notify.yaml` | weixin-notify / 微信通知 | `*/1 * * * *` | `*/1 * * * *`(job d72dbcbb7cbb) | `weixin-通知`(notify,chat_whitelist: [`50438708676@chatroom`],notify_self: false,read_timeout_seconds: 120) |

⚠ **[G] yaml schedule ≠ 实跑节奏**:发火权威是 cron job 内嵌的 `schedule.expr`
(jobs.json),`weixin.yaml` 蓝本里的 `*/30` 已陈旧(装机「微信监控」job 实跑
`*/2 9-22`)。合并时 yaml 与 job expr **两处都要**写成 `*/5 * * * *`。

## [G] 四档 schema 十二节对齐结论(合并语义安全面)

品类级冲突**仅两处且均已裁决**:schedule(D1 终裁 */5)与 push(D3 预挂带进)。
其余逐节核对全同形或无冲突:

- `timezone`(Asia/Shanghai×4)、`watchlist`(空×4)、`classify`(false/[]×4)、
  `dedup`(key 全 `{url}`×4)、`enrich`(false×4)、`storage`(30d monthly×4)——全同。
- `timeouts.fetch`:notify 120 / 其余 660。合并档取 660;notify 源级
  `read_timeout_seconds: 120 ≤ 660` 约束(「须 ≤ 品类 timeouts.fetch」)仍满足。
- **sidecar 节全空**:四档均无 `images:`/`baseline:`/`aggregate:`/`value_gate:`/
  `plugin:` 顶层节——合并无 sidecar 语义可丢。
- 源级 `engine_options` 三通道形态(localdb/sns/notify)是合并的逐字照抄重点:
  含 notify 的 `chat_whitelist`/`notify_self`/`read_timeout_seconds` 与 sns 的
  `feed_kind` 双模式,一个字符都不能动(源名=键,选项=行为)。

## [G] 水位/锚/验证面(AC2/AC3 的可执行配方)

- 水位键:`wechat-local://watermark/<源名>`,落 **myia.db `change_baseline` 表**
  (`src/myssia/store/sqlite.py:159`;notify 档注释 L11 亦明载 store change_baseline
  键)。键无品类维度 → 合并零重灌实锤。
- 锚族(引擎按通道铸,与品类文件无关):`#wx-`(localdb 聊天)/`#wxsns-`(朋友圈)/
  `#wxn-`+`#wxnr-`(通知新消息/撤回)。dedup_registry 表承载。
- 验证配方:
  ```bash
  DB="$HOME/Library/Application Support/MYIA/myia.db"
  # 合并前留档(期望 5 键,与 5 源一一对应):
  sqlite3 "$DB" "SELECT url FROM change_baseline WHERE url LIKE 'wechat-local://watermark/weixin-%'"
  # 合并+拉取一轮后:同 5 键在场、指纹推进;items 按源计数不重复(dedup 锚不动)
  ```

## [G] cron 管理正门(CLI,禁手改 jobs.json)

- **操作一律走 CLI**:jobs.json 由 store 层 mkstemp+rename 原子写管着,手改绕过锁。
- 数据根锚定:CLI `--db` 缺省 = `$MYIA_HOME/myssia.db`(db 父目录定数据根;
  `cli.py:229` `_cron_default_db`)。操作装机机时先
  `export MYIA_HOME="$HOME/Library/Application Support/MYIA"`。
- 四 job 现状全部 enabled / last_status ok:
  `0e9f2daf2d6a 微信监控`、`897e224ef024 微信AI中转站`、`d72dbcbb7cbb 微信通知`、
  `90ae9c28788e 微信朋友圈`。
- 合并收敛操作(留「微信监控」job 历史顺带归一):
  ```bash
  myssia cron edit 微信监控 --schedule '*/5 * * * *'   # schedule 变更自动重算 next_run_at
  myssia cron remove 微信AI中转站 && myssia cron remove 微信通知 && myssia cron remove 微信朋友圈
  myssia cron run 微信监控    # 手动触发:下次 tick 立即跑(AC3 验证不必等窗口)
  ```
  (`job_id` 接受 id 或名字;`create --category` 自带完整装载校验早失败。)

## [G] 仓库种子/装配面实况(与 PRD AC4/AC5 对齐用)

- **仓库 `config/weixin.yaml` 种子 = 教学模板形态**(像素链样例源
  `weixin-文件传输助手`——注释明言「每个微信账号都有,零隐私面」+ 合成样例
  `weixin-localdb样例会话` + 注释掉的朋友圈模板),与数据根真实配置**刻意漂移**;
  并行档 10-20-config-blueprint-drift-doctor 正在做「蓝本 vs 数据根」只读对账。
- `config/weixin-ai-token.yaml`、`config/weixin-notify.yaml` 种子与数据根**逐字相同**
  (真实配置入库先例);`config/weixin-sns.yaml` **从未入库**(装机机独有)。
- **tauri.conf.json resources 是显式清单**(非 glob):weixin 系只含
  `weixin.yaml` + `weixin-notify.yaml`——**weixin-ai-token.yaml 从未入包**。
- installer 测试期望面:`tests/desktop/test_installer_resources.py` 期望清单含
  `weixin.yaml`+`weixin-notify.yaml`;`tests/desktop/test_bundled_plugins_install.py`
  注释记「随包品类面 18 件」。合并后:删 weixin-notify 装配条目与期望项(18→17)。
- ⚠ 并行会话在场:tauri.conf.json、tests/fixtures 等当前是脏文件(他人线在写)。
  批二动手前重读新鲜度,提交走 pathspec 外科(共享暂存区纪律)。

## [G2] 二轮 grill 实证(执行器级)

- **表结构(验证 SQL 用真列名)**:`change_baseline(url PK, etag, last_modified,
  content_hash, last_changed)`;`items(source, category, url, dedup_key, first_seen,
  read, starred …)`;`dedup_registry(key PK, …)`。无重灌核对用
  `SELECT source, COUNT(*) FROM items WHERE source LIKE 'weixin-%' GROUP BY source`
  合并前后对照(计数稳定、无新增重复 dedup_key)。
- **fetch 超时帽按源算**(pipeline.py:289 注释原话「``fetch`` applies per source」),
  且多源 `asyncio.gather` 并发拉(L1882)→ 合并 5 源各自 660s 帽,无叠加风险。
- **补种语义(排雷)**:sidecar `_seed_first_run`(entry.py:624)**每次启动幂等补缺
  自包内 config**——只补缺、不覆盖(`.seeded` 标志只是记录不是抑制器)。推论:
  - `weixin-notify.yaml` **在包内** → 数据根删除后,sidecar 重启(换装必重启)会把它
    **补种复活**;复活档无 cron job = 「在场不在跑」缺省关语义,无实害,但 AC1 的
    「只剩 weixin.yaml」终验必须放在**换装之后**(复活即再删,预期内)。
  - ai-token/sns 从未入包 → 删了不复活。
  - 数据根合并档 weixin.yaml 不会被包内模板覆盖(只补缺不覆盖)。
- **CLI 调用形态**:`myssia` 不在 PATH;用 `.venv/bin/myssia` 直调。
  ⚠ 禁裸 `uv sync`/`uv run` 触发依赖剪除(本机 venv 带 extras 判例)。
- **cron serve 现跑中**:装机 python `-m myssia_desktop_entry serve`(2026-10-20
  上午实测在跑)。tick 层 flock 单 ticker(tick.py:158 LOCK_EX|LOCK_NB);CLI
  edit/remove/run 走 store 同款锁协议,与 serve 并发安全。
- **golden 夹具无关**:`tests/fixtures/push_targets_golden_before.json` 的 weixin
  命中全是协议字段(`weixin_hermes_bin`/`weixin_local_enabled`),不涉品类档,
  无需同步。
- **历史条目 category 字段不回填**:旧 sns/notify 条目的 `items.category` 保持
  `weixin-sns` 等历史值,不做数据迁移(渠道视图按源名前缀不受影响;D2 已裁)。
- **换装判例**:换装后必清 WKWebView 缓存;亮窗验证走 `MYIA_SHOW_ON_START=1` 直跑
  二进制(在册判例,批三照办)。

## 架构事实(schema 实读,`src/myssia/schema.py`)

- `CategoryConfig`(L1871)持有 `schedule`/`push`/`storage`/`timeouts` 等 → **一个
  配置文件 = 一个品类 = 一份节奏**;`SourceConfig`(L853)无调度字段 → 合并即共享节奏。
- 水位键无品类维度 → 合并同理零重灌;feed 渠道归属按**源名前缀 `weixin-`** 判定
  → 合并后渠道视图不变。
- 数据根 `weixin.yaml` 67-79 行注释记录拆档史(ai-token 10-13 拆出、sns 10-14 拆出,
  备份 `weixin.yaml.bak-20261014-sns-split` 在场);其注释还引用「仓库样例」指针
  (pixel 形态参考仓库 config/weixin.yaml 样例)——种子若改形态需同步该指针。

## push 面备注

四档当前全不发送(10-17 深夜主人令「太频繁」全停)。ai-token 档预挂
`feishu_card` archive 路由(bot: analyst,keychain open_id 寻址,`mode: archive`
= 只入库,当前零发送,防翻案复发件)。

## 澄清记录

- 「多个账号」:这 4 件都是本机**同一个微信**账号下的会话;wechat_local 引擎只读本机
  单登录实例,真多账号架构不支持。
- TG 侧 `telegram-*.yaml`(channels/groups/web/api 等)是同模式拆档,如要合并另立档
  (PRD D4 范围外)。

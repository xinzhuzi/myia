# 微信监控配置合并(四档归一)

## 背景

主人问「微信监控配置里有 4 个,为啥配置文档里只看到 1 个」——排查实况:微信监控现散在
4 个品类文件、共 5 个源,全部监控的是**本机同一个微信账号**下的会话(不是多账号)。
主人裁决:合并到 1 个配置文件。

现状清单(2026-10-20 实测 + grill 深化,详见 `research/current-state.md`;
⚠ 发火权威是 cron job 内嵌 expr,yaml schedule 是蓝本——两者已漂移):

| 文件(数据根 = `~/Library/Application Support/MYIA/config/`) | 品类 | yaml 蓝本 / 装机 job 实跑 | 源 |
|---|---|---|---|
| `weixin.yaml` | 微信监控 | `*/30` / **`*/2 9-22`** | weixin-TMS 中转站交流 |
| `weixin-ai-token.yaml` | 微信AI中转站 | `*/2 9-22` / 同 | weixin-AI中转站-♾️ AI Token |
| `weixin-sns.yaml` | 微信朋友圈 | `*/5` / 同 | weixin-朋友圈、weixin-朋友圈互动 |
| `weixin-notify.yaml` | 微信通知 | `*/1` / 同 | weixin-通知 |

历史上拆档的主因是节奏差异;如今 push 已全停、retention 全 30d、enrich 全关,
**四档十二节逐节核对后品类级冲突只剩 schedule 与 push 两处**(research「十二节对齐
结论」节),均已裁决,是合并的好时机。

## Goal

数据根与仓库的微信四品类档合并为单一 `weixin.yaml`(5 源),源名/锚/水位零重灌,
cron 注册收敛为单 job,仓库种子/装配/文档引用面全同步。

## 决议(D1/D5 为主人终裁,其余按推荐执行)

- **D1 终裁(主人 2026-10-20 拍板「合并成 1 个 yaml 配置」):四档并一,合并为单一
  `weixin.yaml`,节奏统一 `*/5 * * * *` 全天**。朋友圈不变、聊天提频无害(localdb 本地
  库读)、通知从 1 分钟降为 5 分钟、AI Token 的 9-22 窗丢弃(夜间安静窗口空结果,
  `empty_ok` 消化)。
  - 翻案记录:曾备「分两档保通知分钟级」选项(快档 `*/1`-`*/2` + 慢档 `*/30`,
    4 件 → 2 件),主人选定单档方案,翻案关闭。
- **D2 feed 品类筛选变化**:「微信AI中转站/微信朋友圈/微信通知」三个品类筛选入口消失,
  条目仍在、微信渠道视图(按源名前缀 `weixin-` 归属)不变。接受。
- **D3 push 面**:保持全关态。ai-token 档里预挂的 feishu_card archive 路由(10-19
  botswitch 防翻案复发件,当前零发送)带进合并档,语义不变(archive = 只入库)。
- **D5 终裁(主人 2026-10-20 拍板「按推荐」):仓库种子取 A 模板形态**——合并后的
  仓库 `config/weixin.yaml` 保持教学模板(样例源更新为「单文件多通道」:pixel
  文件传输助手样例 + localdb 样例 + **注释形态的 sns/notify 样例**),真实会话只活在
  数据根;删除 `weixin-ai-token.yaml`、`weixin-notify.yaml` 两粒种子。理由:weixin.yaml
  是**入包产品面**,现种子刻意零隐私(样例注释自述),镜像真实配置会把主人会话面
  带进发行包;且与并行档 10-20-config-blueprint-drift-doctor 的「蓝本 vs 数据根对账」
  口径自洽。
  - 翻案记录:曾备 B 镜像形态(种子 = 数据根合并档逐字镜像,sns 缺件消解,代价是
    发行包携带真实会话声明),主人选定 A,翻案关闭。
- **D6 范围外**:TG 侧 `telegram-*.yaml` 多件同模式,如要合并另立档;微信多账号
  (wechat_local 引擎只读本机单登录实例)架构不支持,不在本档。

## 约束(红线)

- **源名与源级 `engine_options` 逐字不变**:源名是 feed 渠道名/去重匹配键/水位键
  (`wechat-local://watermark/<源名>`)的载体;engine_options 是三通道行为面
  (notify 的 `chat_whitelist`/`notify_self`/`read_timeout_seconds: 120`,sns 的
  `feed_kind` 双模式,localdb 的 `chat`/`since_days`)——合并迁源一个字符都不能动。
- **零重灌**:水位键无品类维度(拆档时已实证),合并不得触发历史消息重拉;
  验证配方见 research(合并前后 `change_baseline` 表 5 键对照)。
- **cron 只走 CLI,禁手改 jobs.json**:store 层原子写管着,`MYIA_HOME` 锚定数据根;
  调用形态 `.venv/bin/myssia`(**禁裸 uv sync/uv run**,剪 extras 判例);
  收敛 = `cron pause` → 换档 → `cron remove` ×3 + `cron edit --schedule` + `resume`,
  手动触发 = `cron run`。
- **补种语义约束**:sidecar 每次启动幂等补缺自**包内** config(只补缺不覆盖)——
  `weixin-notify.yaml` 在包内,数据根删除后换装重启会**复活**(无 job 不跑,无实害);
  AC1 的「只剩 weixin.yaml」终验点在换装之后(复活即再删,预期内)。ai-token/sns
  不在包内不复活;数据根合并档不会被包内模板覆盖。
- **隐私红线继承**:enrich 关、push 不新增外发通道、retention 30d、日报零微信分区。
- **先备份后动手**:数据根 4 件 + `cron/jobs.json` + 水位/条目基线
  (`change_baseline` 5 键、`items` 按源计数)合并前留档。
- 并行会话在场:批二触 tauri.conf.json/tests 等脏文件前重读新鲜度,提交走 pathspec
  外科(共享暂存区纪律)。

## Acceptance Criteria

- [ ] **AC1 数据根收敛**:数据根 `config/` 只剩 `weixin.yaml` 承载全部 5 源,3 个旧档
      删除(合并前 `.bak` 备份在场),品类装载校验通过;**终验点在换装后**
      (包内 weixin-notify 补种复活件再删,见约束「补种语义」)。
- [ ] **AC2 源名与 engine_options 零变化**:合并档 5 个源的 `name` 与
      `engine_options` 与合并前逐字一致(对照 research 表)。
- [ ] **AC3 cron 收敛 + 零重灌**:jobs.json 由 4 job 收敛为 1 job(名「微信监控」,
      expr `*/5 * * * *`,历史保留);`cron run` 手动触发一轮后:`change_baseline`
      5 键与合并前同键、指纹推进(content_hash/last_changed);`items` 按源计数
      与合并前一致、无重复入库(SQL 配方见 research)。
- [ ] **AC4 仓库同步(D5 终裁:A 模板形态)**:仓库 `config/weixin.yaml` = 合并版模板(含注释
      形态 sns/notify 样例);删 `config/weixin-ai-token.yaml`、`config/weixin-notify.yaml`
      种子;`tauri.conf.json` resources 删 weixin-notify 条目;installer 测试期望
      18→17 件;`tests/fixtures/push_targets_golden_before.json` 等夹具如涉同步。
- [ ] **AC5 文档同步**:`docs/zh|en/wechat-local.md`、`docs/zh|en/write-a-plugin.md`、
      `skill/SKILL.md` 活口径改「单档多通道」;**CHANGELOG 只增新条不改旧史**;
      数据根 weixin.yaml 注释里「pixel 形态参考仓库样例」指针随种子形态核实;
      `tests/test_docs.py` 绿。
- [ ] **AC6 前端契约**:`feed-screen.tsx` B3 深链(只预选 `weixin.yaml`)仍成立;其
      3190-3195 注释中「生产数据根另有 weixin-ai-token.yaml 第二品类文件」句随合并更新;
      相关 vitest 绿。
- [ ] **AC7 门禁与装机件**:全量 pytest + vitest 零新红;装配面变化(18→17)按
      「交付完成判定含装机包」判例重打包换装并核验 weixin-notify 不在包内
      (或按主人指示留窗,留窗须在完成汇报首段显式声明)。

## 风险与回滚

- **补种复活(预期内,非故障)**:换装重启后数据根 weixin-notify.yaml 可能自包内
  复活(旧包)/ 不再复活(新包已删);终验在换装后,复活即再删。
- 回滚 = 恢复 4 件 `.bak` + `cron/jobs.json` `.bak`(或 `cron create` 重建 3 个旧
  job;锚/水位不受合并方向影响,双向无损)。
- 批二仓库件失败:git 还原即可,与数据根互不影响。
- notify 降速(1 分钟→5 分钟)是 D1 已裁的产品语义,非缺陷;如翻案单开小步。
- fetch 超时帽按源算且多源并发(pipeline 实证),5 源合并无叠加风险,无需调帽。

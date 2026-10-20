# 执行清单(数据根现场件先行,仓库件随后)

> 顺序敏感,命令与机制全部来自 `research/current-state.md`(两轮 grill 实证),照抄勿发明。
> CLI 一律 `.venv/bin/myssia`(不在 PATH;**禁裸 uv sync/uv run**——剪 extras 判例)。
> 预期内坑:`weixin-notify.yaml` 在包内,换装重启会被补种复活 → AC1 终验在换装后。

## 批一:数据根合并(装机机现场)

- [ ] 1. 备份:数据根 4 件 weixin 档 + **`cron/jobs.json`** 各留带日期 `.bak`;水位与
      条目基线落盘:
      ```bash
      export MYIA_HOME="$HOME/Library/Application Support/MYIA"
      DB="$MYIA_HOME/myia.db"
      sqlite3 "$DB" "SELECT url FROM change_baseline WHERE url LIKE 'wechat-local://watermark/weixin-%'" > /tmp/wx-watermark-before.txt
      sqlite3 "$DB" "SELECT source, COUNT(*) FROM items WHERE source LIKE 'weixin-%' GROUP BY source" > /tmp/wx-items-before.txt
      ```
      (水位期望 5 键;不足 5 先查原因再动手。)
- [ ] 2. **先按停再换档**(避免换档窗口被 tick 撞上;cron serve 在跑是常态):
      ```bash
      .venv/bin/myssia cron pause 微信监控
      ```
- [ ] 3. 合并 `weixin.yaml`(品类 id/name 沿用 `weixin`/微信监控):
      - 4 源并入:AI Token / 朋友圈 / 朋友圈互动 / 通知,连同各自
        `engine_options` **逐字照抄**(notify 的 `chat_whitelist`/`notify_self`/
        `read_timeout_seconds: 120`,sns 的 `feed_kind`,localdb 的 `chat`/`since_days`)。
      - `schedule: "*/5 * * * *"`(D1 终裁);`timeouts.fetch: 660`(fetch 帽按源算,
        5 源并发 gather 无叠加风险)。
      - ai-token 预挂 feishu_card archive 路由带进 push 节(D3)。
      - 头部注释改写合并史(四档归一、水位键无品类维度零重灌、四通道锚族谱)。
- [ ] 4. 删除数据根 3 个旧档(ai-token/sns 删了不复活;notify 换装时会复活,
      批三终验再删——预期内)。
- [ ] 5. cron 收敛并复跑:
      ```bash
      .venv/bin/myssia cron remove 微信AI中转站
      .venv/bin/myssia cron remove 微信通知
      .venv/bin/myssia cron remove 微信朋友圈
      .venv/bin/myssia cron edit 微信监控 --schedule '*/5 * * * *'   # 保留 job 历史
      .venv/bin/myssia cron resume 微信监控
      .venv/bin/myssia cron list                                     # 核:微信系 1 job,expr */5
      .venv/bin/myssia cron run 微信监控                              # 手动触发,不等窗口
      ```
- [ ] 6. 真跑验证(AC2/AC3):`change_baseline` 同 5 键、指纹推进(content_hash/
      last_changed);`/tmp/wx-items-before.txt` 对照各源计数稳定、无重复入库;
      失败 → 按风险节回滚。

## 批二:仓库同步(D5 主人终裁:A 模板形态)

- [ ] 7. 仓库 `config/weixin.yaml` 改为合并版**教学模板**:头部「双通道」注释扩为
      **四通道**(pixel/localdb/sns/notify);保留 pixel `weixin-文件传输助手` 样例 +
      localdb 样例;把 sns(feed/notices 双模式)与 notify(chat_whitelist 等)以
      **注释形态**收进样例区(键名照抄被删真实档)。
- [ ] 8. 删种子 `config/weixin-ai-token.yaml`、`config/weixin-notify.yaml`;
      `desktop/src-tauri/tauri.conf.json` resources 删 weixin-notify 条目
      (**动前重读:该文件是并行会话脏文件**);installer 测试期望 18→17
      (`test_installer_resources.py` / `test_bundled_plugins_install.py`)。
      (golden 夹具已实证无关,不动。)
- [ ] 9. 文档改活口径(AC5):`docs/zh|en/wechat-local.md`、`docs/zh|en/write-a-plugin.md`、
      `skill/SKILL.md`;CHANGELOG **只增新条**;数据根 weixin.yaml 注释里
      「pixel 形态参考仓库样例」指针核实仍指向存在的样例;`tests/test_docs.py` 过。
- [ ] 10. `feed-screen.tsx` 3190-3195 注释更新(AC6):删「另有 weixin-ai-token.yaml
       第二品类文件」句,改单档表述。

## 批三:门禁与交付

- [ ] 11. 全量 pytest + vitest 零新红(AC7);GitNexus `detect-changes -r shishi
       --scope staged` 核改动面;提交走 pathspec 外科,不收并行会话脏文件。
- [ ] 12. 装配面已变(18→17)→ 重打包换装;换装后三件套核验:
       ①装机包内无 weixin-notify.yaml、weixin.yaml 为模板形态;②**数据根复核:
       补种复活的 weixin-notify.yaml(若有)再删一次**,AC1 终验在此刻成立;
       ③清 WKWebView 缓存,`MYIA_SHOW_ON_START=1` 亮窗目验 feed 微信渠道照常。
       (或按主人指示留窗,留窗须在完成汇报首段显式声明。)

## 回滚点

- 批一失败:恢复 4 件 yaml `.bak` + `cron/jobs.json` `.bak`(或 `cron edit 微信监控
  --schedule '*/2 9-22 * * *'` 回原 expr + `cron create` 重建 3 旧 job;锚/水位
  双向无损)。
- 批二失败:git 还原仓库件即可,与数据根互不影响。

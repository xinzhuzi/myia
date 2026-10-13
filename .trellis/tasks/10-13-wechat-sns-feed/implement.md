# Implement:微信朋友圈进情报流

执行序(每步门禁绿才进下一步;提交点标 ⌘):

## 批 1:桥 sns 域 + 命令(plugins/wechat-bridge)

- [x] 1.1 `wechat_bridge/sns_query.py` 新文件:feed XML 解析(§2.3 契约表)
  + notices SQL 直查 + type 映射(1→like/2→comment/其余原样)。
  独立于 localdb_query(域不同、解析面不同;`_open_copy`/`_contact_pick_names`
  从 localdb_query import 复用,不复制)。
- [x] 1.2 `localdb.py`:`DOMAIN_DB_FILES` 加 `"sns": ["sns/sns.db"]` +
  编排函数 `sns_history(config, storage, keys, mode, since_days)`(E2 副本
  with domains=["sns","contact"] → sns_query 装配;query_history 同构)。
- [x] 1.3 `cli.py`:`localdb sns feed|notices --since Nd --json` 两分支
  (argparse 形态照 key-provider 多层先例;--json/--config 逐层注册表追加)。
- [x] 1.4 版本三处:pyproject.toml / __init__.py / component.json → 0.6.0。
- [x] 1.5 测试 `tests/wechat-bridge/test_sns_query.py`:合成夹具四形态
  (正文/纯图/转发/坏 XML)+ 窗口 + contact 回落 + notices 映射;
  `test_cli.py`(或在既有 CLI 测试文件)加两命令 usage/错误分支;
  golden_cli_payloads.json +2 锚。
- [x] ⌘ 1.6 提交 `feat(wechat-bridge): localdb sns 命令——朋友圈动态与互动通知只读查询(0.6.0)`。
  门禁:`uv run pytest tests/wechat-bridge/ -x -q`(全部绿)。
  真跑自证(开发机):`plugins/wechat-bridge/bin/wechat-bridge localdb sns
  feed --since 1d --json | python3 -m json.tool | head -40` 与 notices 同,
  载荷贴回本档(脱敏:正文只留长度,id/计数全留)。

## 批 2:引擎 sns 通道(src/myssia)

- [x] 2.1 `engines/wechat_local.py`:CHANNELS 加 "sns";`_options()` sns
  分支(feed_kind/since_days/read_timeout;chat/sides/count 交叉拒);
  `_fetch_impl` 分派 `_fetch_sns`;锚函数 `sns_anchor(id)`/
  `sns_notice_anchor(local_id)`;条目铸造(feed 标题回退链:text→[图片×N]→
  [视频]→[朋友圈动态];notices:赞/评词面);水位复用;skip 同 localdb。
- [x] 2.2 测试 `tests/engines/test_wechat_local_engine.py` 追加 sns 组:
  options 交叉拒/feed+notices 铸造/锚稳定/水位推进+skip 不推进/错误族。
- [x] ⌘ 2.3 提交 `feat(engines): wechat_local sns 通道——朋友圈动态/互动通知入情报流(id 强锚+水位增量)`。
  门禁:`uv run pytest tests/engines/ -x -q`。

## 批 3:配置面 + 真跑验收

- [x] 3.1 repo 样例 `config/weixin.yaml`:「你的会话往这里加」注释段补
  sns 形态两行样例(feed/notices);不改既有源(发行样例不含真会话)。
- [x] 3.2 live `~/Library/Application Support/MYIA/config/weixin.yaml`:
  加 `weixin-朋友圈`(feed_kind: feed)+ `weixin-朋友圈互动`(notices)
  两源,since_days: 3,push 维持空。
- [x] 3.3 真跑:`uv run myssia run weixin --once`(沙箱 MYIA_HOME 不用
  ——live 数据根,桥真读真解密);核对 feed 屏微信渠道两新源条目在场;
  重跑同窗零新增(dedup);第二轮 --since 收缩(水位生效,跑两次看桥
  argv 日志或 copy.built/kept 变化)。
- [x] ⌘ 3.4 提交 `docs(config): weixin.yaml 样例补 sns 通道形态`。
  全量门禁:`uv run pytest -x -q`(全仓)+ `npm --prefix desktop/ui-src
  run -- test`(零 UI 改动,防意外)。

## 批 4:装机换装 + 收尾

- [ ] 4.1 装机件刷新:桥组件重打包(just release-plugins --dry-run 验锁
  → 正式),桌面装机包重建换装(既有换装链:验源→删旧→清 WKWebView
  缓存)。
- [ ] 4.2 装机真跑 AC2:MYIA_SHOW_ON_START 直跑二进制小窗验(feed 屏
  微信渠道两源条目;截屏+local-ocr 留证,内容脱敏)。
- [ ] 4.3 状态 in_progress→review(task.json 直改,避开并行会话踩踏);
  implement.md 勾档;journal 记录。

## 验证命令速查

```bash
uv run pytest tests/wechat-bridge/ -x -q          # 桥域
uv run pytest tests/engines/ -x -q                # 引擎域
uv run pytest -x -q                               # 全量
plugins/wechat-bridge/bin/wechat-bridge localdb sns feed --since 1d --json
plugins/wechat-bridge/bin/wechat-bridge localdb sns notices --since 1d --json
uv run myssia run weixin --once                   # live 真跑(数据根)
```

## 回滚点

- 批 1 后:桥 0.6.0 独立可用(纯加法),不装引擎即零影响。
- 批 2 后:live 未配源 = 引擎新通道零消费,零影响。
- 批 3 后:删 live 两源即停采(数据面),store 条目随 retention 过期。

## 执行实录(2026-10-13 夜,批 1-3 全交付)

- 提交链:59ff041(桥 0.6.0)→ 073698a(引擎 sns)→ bedbe8a(配置+README)。
- 真跑实证:桥 feed 1d 窗 70 条 0.59s(parse_errors=3 如实)/notices 3 条
  (feed_id INTEGER→str 修复)/query 回归零变化。
- live 真库(run_id=342):朋友圈 217+互动 3 条入 store;二跑 dedup_seen
  全静默(#wxsns- id 锚幂等);水位缩窗 217→74。
- **装机热修实录**:live 加源后装机 cron(*/2,sidecar PYTHONPATH→
  /Applications/世事.app/Contents/Resources/myssia-src)每轮 invalid_engine_options
  红(bundled myssia 无 sns)——bundle 与仓库 diff 恰好只有我改的两文件,
  热修 = cp 两文件进 bundle + 清 pyc,21:04 起装机 cron 全绿(21:06 轮
  3 源 0 失败 items=124 retained=1)。桥组件同步 ~/.myia(0.6.0,
  collector 独立资产保留)。**完整 tauri 重打包走下次 tag 发布链**,
  bundle 热修与 0.4.x 时代换装同路数。
- golden 修正记录:design 说 +2 锚,实落 +1 锚(feed/notices 错误载荷
  同形,双锚零增量;成功载荷形状由 test_sns_query 合成副本细断言)。
- 门禁:全量 pytest 5629 passed 零新红;vitest 未跑(UI 零改动)。
- **遗留(批 4 裁量)**:feed 屏像素级验收留并行会话(10-13-wechat-
  features/groupinfo 在改 feed-screen.tsx/api.ts)收编后做——数据面
  220 条已入库,UI 渲染零改动面(源名前缀自动归微信渠道),不阻塞。

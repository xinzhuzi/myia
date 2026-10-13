# Implement:微信监控 UI(契约规格册对齐版;细节以 design §A-§F 为准)

> 执行序=先无冲突面(A-C 前端/Rust),桥面 D 排队(并行避让 design §6)。
> 每步验证就地跑;全量门禁收官统一。禁止 git commit(主会话收官)。
> 契约细节**不在本档重复**,逐步引用 design §A-§F 对应节。

## A 前端·设置卡(无并行冲突)

- [ ] A1 api 扩展(wechat-keyprovider-api.ts,~85→~180 行):`wechatKeyStatus()`+parse 守门(布尔严校模式照抄 parseKeyProviderState)+`KEY_ACQUIRE_EVENT_NAME`+`subscribeKeyAcquire(cb): UnlistenFn`+`startKeyAcquire(force)`/`cancelKeyAcquire()`——契约=design §B.3/§D.1,listen+UnlistenFn 照 pyenv-api.ts 范本。
- [ ] A2 密钥状态行(weixin-account-card.tsx 取钥器行**上方**插入,因果序=状态→行动→工具):Badge 三态(已就绪 N 库/已失效/未获取)+相对时间+按钮态联动(missing/stale=「获取密钥」;ready=「重新获取」;未配取钥器=置灰+引导)。testid `weixin-keystatus-*`。
- [ ] A3 三步面板(卡内,状态机 idle→confirm→running→result,§D.2 全规格):confirm 双文案+ready 变体覆盖语义行;running 四阶段步进条(phase 词表 §D.3,当前高亮已完成打勾)+detail mono 行+取消(「正在取消…」直到 cancelled 事件);result 成功/失败形+重试回 confirm。
- 验证:`npm --prefix desktop/ui-src run test -- weixin-account-card` 新增用例(`密钥状态行三态渲染`/`获取流全程 confirm 到 result`/`取消触发 cancel 并收 cancelled 事件`/`ready 态重新获取带确认文案`/`未配取钥器按钮置灰`)+ `npm --prefix desktop/ui-src run build`(tsc)。

## B 前端·feed 三级监控台(无并行冲突)

- [ ] B1 微信群列表右栏(feed-screen.tsx ~L1163 渠道行家族):`weixin-` 前缀源过滤+每源最新一条(cardDigest 既有函数复用)+CHANNEL_ROW_AVATAR_TONE.wx 官方绿 10% tint 既有档。testid `wx-monitor-*`。
- [ ] B2 密钥缺失态:源最近 run skip_reason=key_unavailable→灰行+「去获取密钥」(导航 /weixin 屏滚到密钥行);其余=源健康度域词(监控中/降级)。
- [ ] B3 「去配置监控群 →」右栏底按钮跳既有 YAML 编辑屏(深链预选 weixin.yaml;该屏无深链参数则跳屏+注释注记手选——grill 决议④一期零写面)。
- 验证:vitest 新用例(`微信群列表按源渲染`/`密钥缺失灰行与跳转`/`最新一条预览与相对时间`/`去配置跳转链路`)+ build。

## C Rust 壳(无并行冲突)

- [ ] C1 `wechat_key_status`(spawn 桥 key-status,载荷直转;§B.1)。
- [ ] C2 `wechat_key_acquire`+`wechat_key_acquire_cancel`(§B.2 全规格:单飞锁无参 cancel/逐行读转 event/壳帽 900s/取消=killpg 用户态树+落哨兵)+main.rs L902 generate_handler 列表注册。
- [ ] C3 cargo 单测:`三态载荷直转`/`progress 行到事件 seq 单调`/`单飞锁二次拒绝`/`取消落哨兵文件`/`超帽判 failed`。
- 验证:`cargo test wechat_keyprovider --manifest-path desktop/src-tauri/Cargo.toml` + `cargo check --locked`。

## D 桥侧(并行避让后)

- [ ] D1 探活桥三件(cli.py/localdb.py/docs):status+mtime 双探;活跃=挂 D 线先收官 A-C(观察员模式)。
- [ ] D2 `localdb key-status --json`(§A.1:三态/抽样 1-3 把页1 HMAC/mtime/恒 exit 0;复用 _verify_enc_key 族+auto_detect_db_dir)。
- [ ] D3 `localdb key-acquire --json [--force] [--timeout-hint N]`(§A.2:already_ready 短路/clamp(120,1800)/progress 转印 stdout/启动清残留哨兵/未配=exit 21 同族文案)。
- [ ] D4 协议文档 v1.1 节(timeout_hint 语义+哨兵约定+交互式取钥器指引,体例随既有 §5-§8)。
- 验证:`uv run --no-sync python -m pytest -q tests/wechat-bridge` 新用例(`key_status 三态`/`key_status 恒 exit0`/`key_acquire 短路 already_ready`/`force 走假 provider 正例`/`未配 exit21 文案`/`hint clamp 边界`/`progress 转印顺序`)。

## E 部署件+端到端

- [ ] E1 keyprovider-lldb.sh(§C 全序列:哨兵轮询 2s/取消 exit 42/临时件 600/root-用户态分段/NDJSON 阶段 progress)。
- [ ] E2 部署 `<数据根>/wechat-localdb/bin/`+chmod 700;设置卡「一键安装取钥器」(源在场检测=攻坚档 tools/ 路径)。
- [ ] E3 端到端:备份 keys.json→`--force` 发起→真重登窗口(**留主人裁决当轮做否**)→验 keys.json 全量验真后覆盖+feed 拉取恢复+哨兵自删;无真窗口的降级验收=假 provider 沙箱全链(MYIA_HOME=tmp)。
- [ ] E4 文案审计:`grep -rn "LLDB\|断点\|passphrase\|挂载" desktop/ui-src/src/screens/settings/weixin-account-card.tsx desktop/ui-src/src/screens/feed/feed-screen.tsx` 零命中(决议⑦)。
- [ ] E5 取消实测:发起 5s 后取消→ps 核验用户态零残留+哨兵在场→(真窗口场景)部署件 ≤10s 自杀+哨兵自删。

## F 收官

- [ ] F1 全量门禁:`uv run --no-sync python -m pytest -q --tb=short`+`npm --prefix desktop/ui-src run test`+`npm --prefix desktop/ui-src run build`+`uvx ruff@0.16.10 check .`+`cargo check --locked --manifest-path desktop/src-tauri/Cargo.toml`。
- [ ] F2 装机包刷新+像素级验证三屏(AC7):MYIA_SMOKE_GEOMETRY 冒烟+截屏+local-ocr(密钥状态行/获取流三步/监控台群列表)。
- [ ] F3 gitnexus detect-changes staged+分域提交(桥/壳/前端/文档/档;pathspec 不收编并行面)。
- [ ] F4 spec 更新:python spec 微信桥节补 v1.1+哨兵;frontend-ui 补三步面板/事件词表判例如需。

## 回滚点

前端 A/B 独立提交可单独 revert;C 面两命令新增零既有路径改动;D 面两命令不改 query/key-provider 既有语义;E 部署件删除即回终端取钥 SOP(攻坚档 tools/ 在案)。

# G10 代理池连通性测试按钮(doctor config_auto 免手填一键化)

## Goal

设置屏代理区「连通性测试」按钮免手填一键化:复用 sidecar doctor IPC 通道,**零新 IPC 方法、零新应答键**,空路径点「探测」= 自动发现 `<数据根>/pools.yaml` 并逐上游探测,结果人话回显(逐上游成功/失败/延迟,零行话)。

母任务计划定案(2026-10-05 傍晚收口后):本轮真实余量仅「免手填一键化」(按钮/输入框/逐池回显三件 40a666a 已在库);池 URL 结构写回 = 协议缺口在案,属远期代理池面板族不进本件。

## Requirements

1. **sidecar `doctor` 增可选布尔 `params.config_auto`**(缺省 false = 现行为逐字节不变):
   - `config` 显式 → 照旧手填赢(优先级之首不变);
   - `config` 缺省且 `config_auto=true` → 以 ServeContext.home(entry.py `_serve_context`,MYIA_HOME env > .app bundle 探测 > dev 回退)拼 `pools.yaml` 做存在性发现:
     - 命中 → argv 照常拼 `--config <路径>`;
     - 未命中(文件不存在 / dev 模式 home=None)→ 不带 `--config`(= 只看现状,应答 `proxy.config=null`)。
   - 发现逻辑全在 entry.py,cli.py `_resolve_pools` 零改动(CLI 层本无缺省路径概念,`config=None → (None, EXIT_OK)` 亲证 cli.py:2594-2604);
   - 零新应答键:自动命中的路径经 doctor 应答既有 `proxy.config` 天然回显;
   - `config_auto` 形状校验:非布尔 → `invalid_params`(path=params.config_auto,与 store.state.* value 布尔门同款)。
2. **前端 settings-screen.tsx**:
   - `handleProbe` 升两态:`probePath.trim()` 非空 → `{config:path}`(现状保留);空 → `{config_auto:true}`;
   - 路径输入框 placeholder 更新为「留空=自动探测 <数据根>/pools.yaml」;
   - 「探测」按钮原位不动(语义升级零迁移)。
3. **回显(doctor-verify.tsx)**:逐池 proxy-pool-row 三态 Badge 零改动;新增两行人话:
   - `proxyConfig` 非空 → 已加载配置路径一行(自动命中时用户可见 doctor 拣了哪个文件);
   - 空路径探测后 `proxyConfig===null` → 「未找到缺省 pools.yaml——可在上方填入全局配置路径后重探」提示行(自动探测未尝试时——挂载初始/保存后刷新——不出现,精确口径:屏侧跟踪最近一次探测是否 auto 态,doctor 应答无新键无法自证)。
4. **协议文档循纪律**:sidecar-protocol.md doctor 行(#4)补 config_auto 语义;注册表计数 62 不变(零新方法);版本注记:可选参数 + 旧壳新 UI 组合优雅降级(旧 sidecar 忽略未知键,doctor 照跑不带 config),循 plugin-market-batch 批二「协议版本未随批 bump」先例,PROTOCOL_VERSION 维持 10。
5. **协议对账例(质询补死,归属本流)**:tests/desktop/test_desktop_sidecar_protocol.py 增全量对账例——断 `data.allowed == sorted(_HANDLERS)` + 与注册表行数一致(动态断言,防并行流 _HANDLERS 增删后对账例失真;现库 :519-531 只断成员包含)。

## Acceptance Criteria

- [x] AC1 sidecar:config_auto 命中——tmp MYIA_HOME 沙箱置 pools.yaml,doctor {config_auto:true} → 应答 proxy.config = `<home>/pools.yaml` 且逐池探测行真跑(零外网:env 缺失凭据上游 → 解析失败行,不触网)。
  证据:`test_doctor_config_auto_discovers_home_pools_yaml`(tests/desktop/test_desktop_sidecar_protocol.py)绿——断 proxy.config==str(home/"pools.yaml")、pools 恰一行 ok=False「无法解析」、findings 含 proxy:main;实现 desktop/entry.py `_m_doctor`(config 缺省且 config_auto 且 ctx.home 非空 → `<home>/pools.yaml` 存在才拼 `--config`)。
- [x] AC2 sidecar:config_auto 未命中——home 模式零 pools.yaml → proxy.config=null、pools=[];显式 config 与 config_auto 并存 → 显式赢(手填路径原样回显);config_auto 非布尔 → invalid_params。
  证据:`test_doctor_config_auto_miss_and_dev_fallback`(home 零文件→null/[] + dev 回退 home=None 同款)、`test_doctor_config_explicit_wins_over_config_auto`(显式不存在路径原样回显+proxy.error)、`test_doctor_config_auto_non_bool_rejected`(invalid_params path=params.config_auto)三例绿。
- [x] AC3 前端:vitest 两态分流——空路径点探测发 `{config_auto:true}`、有路径发 `{config:path}`;auto 未命中提示行出现/初始挂载不出现;placeholder 文案更新。
  证据:settings.test.tsx 新两例绿——「G10 探测两态:留空发 config_auto,自动命中回显配置路径 + 逐池行」(seen[0]=={} 初始无键、点击后 config_auto===true、proxy-config-path/逐池行在、auto-miss 不冒)与「自动未命中 → 人话提示行;挂载初始不冒;填路径重探退场」(placeholder 含「自动探测」、proxy-auto-miss 文案两段、显式重探后退场);既有「探测走 doctor(--config=路径)」例不动仍绿。
- [x] AC4 协议:sidecar-protocol.md doctor 行补 config_auto 半句 + 版本注记;注册表 62 行不动;tests/desktop 全量对账例过(data.allowed == sorted(_HANDLERS) == 注册表行数)。
  证据:sidecar-protocol.md #4 行补 config_auto 语义半句 + 批注段 g10-proxy-probe 段(循 gates 先例不 bump,理由:零新方法零新应答键缺省 false 逐字节不变+旧壳忽略未知键降级);亲跑 `python -c` 读 _HANDLERS=62、PROTOCOL_VERSION=10;`test_method_registry_full_reconciliation` 绿(动态断 allowed==sorted(_HANDLERS)==注册表逐行方法名,两侧漂移即红,不硬编码行数)。
- [x] AC5 门禁:uv run --no-sync pytest tests/desktop/test_desktop_sidecar_protocol.py 全绿;vitest settings 相关文件全绿;ruff 零新红;detect-changes 亲跑;git commit --only 本流文件。
  证据(全部本机亲跑):`uv run --no-sync pytest tests/desktop/test_desktop_sidecar_protocol.py -q` → 145 passed;`uv run --no-sync pytest tests/desktop -q` → 224 passed;ui-src `npx vitest run` → 25 files/465 tests 全绿(含新两例);`npx tsc -b` 零错;`uv run --no-sync ruff check .` All checks passed(仅既存 e2e noqa 格式 warning,非本流);`gitnexus detect-changes -r shishi --scope unstaged` 亲跑:7 文件 14 符号,受影响流 7 条全在 SettingsScreen→doctor 预期面(_item_dict/_ITEM_STATE_MARKERS/handlePushSave 等为行号漂移归因噪声,本流 diff 未触及,读 diff 亲证);Rust 侧零改动零新 IPC(复用 doctor),cargo 不适用。

## 完成纪要(2026-10-05)

- 实现面:desktop/entry.py `_m_doctor`(+config_auto 布尔门/发现分支,缺省行为逐字节不变)、types.ts DoctorParams(+config_auto?)、settings-screen.tsx(handleProbe 两态+probeAutoMiss 跟踪+placeholder/hint 人话化+面板传参)、doctor-verify.tsx(代理区补「已加载配置」路径行与「未找到缺省 pools.yaml」提示行;逐池三态 Badge 零改动)。
- 超计划半步(有意,已在 Requirements 3 记录):提示行以屏侧 probeAutoMiss gating(doctor 应答无新键无法自证 auto 态,挂载初始/保存后刷新不冒「未找到」);auto 命中补「已加载配置:<路径>」行(计划「proxy.config 天然回显」的 UI 落点,否则用户看不到 doctor 拣了哪个文件)。
- 版本注记:PROTOCOL_VERSION 维持 10(循 plugin-market-batch gates 先例),旧壳+新 UI 组合=旧 _m_doctor 忽略 config_auto 照跑不带 config,前端提示行降级,不白屏。

## Notes

- 与远期「代理池管理面板」同族但本件只做测试按钮(池档决议)。
- 涉网纪律:本件实现与测试全程零外网(探测路径测试用 env 缺失凭据上游隔离,同 tests/engines/test_proxy_pool.py:766-783 手法)。
- gitnexus impact 亲跑:`_m_doctor` upstream 0 受影响(risk LOW,注册表 dict 字面量非调用面);`handleProbe` upstream 4(SettingsScreen→App,risk LOW)。

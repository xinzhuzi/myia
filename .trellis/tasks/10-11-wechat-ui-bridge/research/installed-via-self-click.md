# AC5 替身终态 — 自己点自己的按钮:设置页 wechat-bridge 组件行 AXPress 安装全链(2026-10-12 14:12–14:35)

> 执行件:安装驱动工(主人令「你自己点,自己写程序去做」——AC5 真机一键验证的替身:
> 主人点按钮的等价终态,路线 A(AX 自家窗 AXPress)按序走通,**路线 B 未启用**。
> 红线纪律:SMOKE 小窗直跑(禁 open -a)+零焦点;**对微信进程零触碰**(全程仅 frontmost
> 采样);AX 只用于 MYIA 自家窗;私有临时件(脚本/日志)用后即清,本文只留形状级证据。

## 0. 结论速览

| 验收点 | 判定 | 证据 |
|---|---|---|
| WKWebView 内容 AX 树可达(与微信零暴露相反) | **命中** | System Events 走查 `窗1>组1>组1>滚动区1>AXWebArea` 全树内容节点可达(§2.1);微信 4.1.15 对照面在 research/ax-probe-4.1.15.md(AX 内容层零暴露) |
| 设置页组件行预态=「未装」(**随包注册表+components.json 已被 app 读到=分发链最后一环真机实证**) | **命中** | 可选组件分区 AX 全读:六行注册表全渲染,`wechat-bridge` 行=标签+徽标`未装`+开关 value=0(§2.2;对照行 `table`=`已装`/v=1 判读语义正确) |
| AXPress 安装 → Rust 安装器真跑两段装 | **命中** | 戳 `<数据根>/pyenv-components/wechat-bridge.json` 出现=`{state:"ready", fingerprint:"3986190c…ec3", error:null}`,指纹与 `sha256("setuptools>=75 wheel>=0.45\0wechat-bridge")` 预计算值逐字吻合(§2.3) |
| 组件行翻面「已装」(AX 读卡片文本) | **命中** | 装后 AX 回读:徽标`已装`+开关 v=1+回执行「组件 wechat-bridge 已装进自管环境(指纹已记;可重开幂等跳过)。」(§2.4) |
| pip 闭包实装自管环境 | **命中** | 自管 env `pip list`:`wechat-bridge 0.3.0 + pillow 12.3.0 + pyobjc-core/-Cocoa/-Quartz/-CoreML/-Vision 12.2.2`(与 install-receipt §8.3③ D5 冒烟逐版本一致);dist-info `INSTALLER=pip`;console script `python/bin/wechat-bridge` 在场(§2.3) |
| probe 升级验证(available 前提性检查) | **命中(两层)** | ①自管 env console script `--probe` exit 0:`state=degraded`+`bridge_component=ok`+`bridge_version=0.3.0`;②卡片真源 `handle_wechat_local("probe",{})` 同载荷(§2.5) |
| 收尾 | **全绿** | 冒烟实例退净(MYIA+sidecar);生产实例 `open -g` 复原 0 亮窗;launchctl MYIA_* 六旗全空;frontmost=主人侧(§5) |

## 1. 基线(14:05–14:12,命令原样)

- frontmost=**WeChat**(主人在用微信);`launchctl getenv` MYIA 六旗全空;生产实例 pid 98452 在跑。
- 数据根 `~/Library/Application Support/MYIA/`:`pyenv-components/` 仅 `table.json`(**wechat-bridge 戳缺位=installed=false 预态**);`python-env.json` state=**ready**(开关不禁用);`python/bin/python3` = 自管 3.12.7;`pyenv-settings.json` = `{}`(PyPI 缺省源,镜像覆盖不生效)。
- 装机包=`/Applications/世事.app` 二进制 inode 325784379/mtime **13:20:54**(commit 8e0e65a 谱系换装,晚于 install-receipt §8.2 记录的 12:45:51 包);随包 `Resources/components.json` 六项 ids 含 `wechat-bridge`(pip_spec=`setuptools>=75 wheel>=0.45`/pip_src=`wechat-bridge`/post_install=`pip-src-no-build-isolation` 齐);`Resources/components/wechat-bridge/` 七项(源码+build/+egg-info 工件,见 §3.2)。
- 指纹预计算(对照 pyenv_components.rs:290-307 `spec_fingerprint`/`closure_fingerprint`):`python3 -c "hashlib.sha256('setuptools>=75 wheel>=0.45\0wechat-bridge'.encode()).hexdigest()"` → **3986190c08410d1d3371ad6eca5bc75cc86ece58545a8b2abffe5bb77ed07ec3**;同法验 `table.json` 戳=sha256(table pip_spec) 逐字吻合(指纹语义先自校验再用)。

## 2. 路线 A 执行记录(全程 AX 通道,零合成鼠标)

### 2.1 SMOKE 直跑 + AX 树可达验收

1. 退生产实例:`osascript -e 'quit app id "com.myssia.app"'`(温和,零夺焦)→ MYIA+sidecar ~5s 退净。
2. 直跑(禁 open -a,env 只进本进程):
   `nohup env MYIA_SHOW_ON_START=1 MYIA_SMOKE_GEOMETRY=1400x1050+860+16 MYIA_SMOKE_ROUTE=settings /Applications/世事.app/Contents/MacOS/MYIA > $TMP/app.log 2>&1 &`
   → app.log 一行 `setup done in 177 ms(sidecar spawned)`;**frontmost 全程未归 MYIA**(亮窗后采样=主人侧 app)。
3. CGWindowList optionAll 找自家窗:**window id=80099**(世事,on-screen,1400×1050@(520,30),X 被系统钳到可见帧;on-screen=True 即 ui-ready 已触发,SHOW_ON_START 渲染完才亮的语义兑现)。
4. **AX 深探**:System Events 走查 `AXWindow[世事] > AXGroup > AXGroup > AXScrollArea > AXWebArea`,web 内容节点全可达(主导航 14 项/设置分区 7 钮/各卡文本字段全可读)——与微信 Chromium 内容层零暴露(AC1 定论)相反,**自家 WKWebView AX 开放验收点成立**。`MYIA_SMOKE_ROUTE=settings` 本轮直落设置屏(与 install-receipt §4.2「装机包路由未生效」表现不同,同码未深究,如实注)。

### 2.2 组件行预态(未装)= 注册表真机读到的实证

AXPress 分区钮「Python 环境」(设置分区组 btn6,title 实读)后,递归搜 `AXGroup desc~"可选组件(按需装进自管环境"` 全树 dump,wechat-bridge 行原文(形状级转录,纯 UI 铬层文字):

```
1 AXStaticText v=[wechat-bridge]
1 AXGroup → 2 AXStaticText v=[自管环境可选组件(按需安装)]     ← 回退文案,见 §3.1
1 AXStaticText v=[未装]
1 AXCheckBox t/d=[组件开关 wechat-bridge] v=[0]
```

- 同法对照:`table` 行=`已装`+v=1(唯一旧戳);trafilatura/crawl4ai/telethon/searxng 全`未装`/v=0——六行与随包 components.json ids 逐一对应,**行渲染自壳侧 `component_statuses(data_root, resource_dir)` 对随包注册表的真读取**(pyenv_components.rs:1134-1143),分发链最后一环(随包注册表→设置页组件行)在新机器语义上真机成立。
- 开关 enabled=true(env ready,非 not_configured 禁用态)。

### 2.3 AXPress 安装开关 → 安装器真跑(本轮核心动作)

```
osascript: perform action "AXPress" of checkbox "组件开关 wechat-bridge"
→ switch_value_before=[0] enabled=[true] frontmost_before=[WeChat] frontmost_after=[WeChat]
```

按压后数秒内(约 14:21:06)落地证据链:

1. **戳文件出现**:`<数据根>/pyenv-components/wechat-bridge.json` = `{state:"ready", fingerprint:"3986190c…ec3", error:null}`——指纹与 §1 预计算闭包指纹**逐字吻合**,且写法=pyenv_components.rs:346-364 原子写格式;ready+error:null 仅安装成功路径落值(pyenv_components.rs:1269-1277)。**本验证全程未手写此文件**。
2. **自管 env pip 闭包**:`$DATA_ROOT/python/bin/python3 -m pip list` 增:`wechat-bridge 0.3.0 / pillow 12.3.0 / pyobjc-core 12.2.2 / pyobjc-framework-Cocoa/-Quartz/-CoreML/-Vision 12.2.2`;`wechat_bridge-0.3.0.dist-info/INSTALLER`=`pip`;console script `python/bin/wechat-bridge` 出现。
   - 装前据证:install-receipt §7.3 明载自管 python **无 pyobjc**(probe main_window=unknown);本轮装后同 env probe main_window=**ok**(pyobjc 真在场才可判)→ 闭包确由本轮安装器写入,非既存。
   - 秒级完成如实注:大概率命中 pip HTTP 缓存(12:4x D5 冒烟已下同版全轮子,全 wheel 零编译);联网属组件安装链设计内行为(注册表描述「首装需联网」),10 分钟超时预算未用。
3. 两段装语义 = 与 Rust 安装器同构(pyenv_install.rs:716-730 argv:`-m pip install --no-input --disable-pip-version-check` 一段闭包 + `--no-build-isolation <resource_dir>/components/wechat-bridge` 二段;resolve_pip_src_spec 相对路径白名单解析 pyenv_install.rs:839-888)——本轮由壳真跑,非手工复刻。

### 2.4 终点一:组件行翻面(AX 读卡片文本)

装后同法 AX 全读可选组件分区,wechat-bridge 行原文:

```
1 AXStaticText v=[wechat-bridge]
1 AXGroup → 2 AXStaticText v=[自管环境可选组件(按需安装)]
1 AXStaticText v=[已装]
1 AXCheckBox t/d=[组件开关 wechat-bridge] v=[1]
1 AXGroup → 2 AXStaticText v=[组件 wechat-bridge 已装进自管环境(指纹已记;可重开幂等跳过)。]
```

`未装→已装`/`v=0→v=1` 翻面 + 动作回执行(pyenv-card.tsx:356-366 的 components[] 回读渲染),即「设置页组件行显示已安装」的 AX 取证。

### 2.5 终点二:probe 两层 + 消息屏数据面

| 层 | 命令 | 结果(exit=0) |
|---|---|---|
| 新装 console script | `$DATA_ROOT/python/bin/wechat-bridge --probe` | `state=degraded`,`checks={bridge_component ok, wechat_process ok, ax_permission ok, main_window ok, localdb_storage ok, localdb_key unavailable, ax_tree unknown}`,`wechat_version=4.1.15`,`bridge_version=0.3.0`,reasons=[key_unavailable](D4 语义如实) |
| 卡片真源(headless) | `PYTHONPATH=<装机包>/myssia-src … python -c 'handle_wechat_local("probe",{})'` | 与上行逐键一致(检查码/双版本/唯一 reason) |
| 消息屏卡题 | AXPress 主导航「消息」(nav8)后 AX 搜静态文本 | `CARD=[微信本机]` 命中(卡在册);版本行/capsule 未及二读,见 §3.4 |

- **升级语义如实注**:bridge_component 检查在装前即 ok(0.2.0 时代手装的 `~/.myia/plugins/wechat-bridge` bin 在场,install-receipt §7),probe 层无 before/after 翻面;本轮「升级」实证落在**组件戳(缺位→ready+指纹)与自管 env pip 包(从无到有+console script)**两处——即 D5 分发链(随包注册表→一键装→自管环境)在新机器上的等价终态。
- `main_window=ok` 为当下真值(主人侧微信开窗中+自管 env 现有 pyobjc),非托盘态必然值(对照 install-receipt §7.3 的 degraded 三态如实惯例)。

## 3. 如实发现(移交主会话)

1. **设置页 COMPONENT_META 缺 wechat-bridge 条目**(pyenv-card.tsx:195-221 只到 searxng):组件行标签回退原 id `wechat-bridge`、描述回退「自管环境可选组件(按需安装)」——功能零损(注册表/安装/指纹全通),装饰性缺口,建议后续把注册表 label/description 的中文文案补进 COMPONENT_META(或改为读注册表字段)。
2. **install-receipt §8.3 尾注「设置页真实两段装不产生此尾随」不成立**:pip 21.3+ 对本地目录 in-tree build,`Resources/components/wechat-bridge/` 内 `wechat_bridge.egg-info`/`build/` 即此类工件——但两件在 14:05 基线 ls 已在场(build/ mtime 14:00 早于本轮;egg-info 14:21:06 是本轮安装刷新 mtime、非新建条目),**本轮安装零新增目录条目**。归属打包卫生线(b9c5054 同病),换装/重打包前需清,不拦功能。
3. **`MYIA_SMOKE_ROUTE=settings` 本轮生效**(直落设置屏),与 install-receipt §4.2(messaging 路由未生效、落 YAML 配置屏)表现不一致;同机制不同轮表现,根因未深挖,复用判例链时仍应首帧核路由。
4. **消息屏导航后本实例 AX 树失联**:AXPress「消息」并读到卡题后,System Events 对 MYIA 进程 `count windows` 恒 0(CG 层窗 80099 仍在场、app 非 hidden 非active,NSRunningApplication 实读),多轮重试不复——WKWebView AX 客户端掉线的已知不稳定形态;**卡片版本行未做 AX 直读,不假证**;数据面已由卡面真源 handler(卡片渲染唯一数据源,visual-check §2.3 逐键对账判例)双 probe 坐实。
5. **主人并行使用如实注**:验证窗口期 frontmost 采样 WeChat→漫影工作室→WeChat→Google Chrome→ZCode 交替均系主人行为;本轮对微信的全部操作=零(§4)。

## 4. 静默面自查(动作台账)

- **对微信**:零调用、零窗口操作、零 AX/合成事件、零进程接触(全程仅 frontmost 采样点名到前台 app 名)。
- **对自家冒烟实例**:AXPress×3(设置分区「Python 环境」钮/组件安装开关/主导航「消息」Link,全部零激活——每次按压前后 frontmost 对照均为主人侧 app)、AX 属性读若干(System Events 走查)、零合成鼠标、零窗口几何操作;probe 为桥自带只读探针(进程存在性+版本,design §2 零成本判据)。
- **出网**:仅壳侧安装链 pip 拉轮子(设计内行为,§2.3);本验证自身零网络调用(OCR/VL 链未启用——AX 读替代像素取证,零截图零全帧)。
- **私有数据红线**:AX dump 含设置屏通用分区字段名/本机 config 路径形状,本文一律不转录;probe 载荷只含检查码/版本/计数;零聊天内容、零密钥材料。

## 5. 收尾回执(全部亲验)

| 项 | 结果 |
|---|---|
| 冒烟实例退出 | `osascript quit com.myssia.app` → MYIA+sidecar ~4s 退净(pgrep 零残留,含 wechat_bridge 子进程) |
| 生产实例复原 | `open -g /Applications/世事.app` → pid 22492,CG 两窗(主窗+助手窗)**全 offscreen(亮窗 0)**,frontmost=主人侧(ZCode)未变 |
| env-flags=0 | launchctl `MYIA_SHOW_ON_START/SMOKE_GEOMETRY/SMOKE_ROUTE/SMOKE_FOCUS/HOME/PYENV_AUTOSETUP` 六旗全空(env 只进直跑进程,无 launchctl 污染) |
| 私有临时件 | `/tmp/wx-click-10593`(0700:AX 脚本 6 件+app.log 一行)与标记文件 `/tmp/wx-click-current-path` 用后即清 |
| 终态遗留 | 数据根新增仅组件戳一枚(安装器写);自管 env 闭包与 console script(安装产物,即任务目标);装机包零新增条目(§3.2) |

## 6. 复跑指南

```bash
# 1) 基线:六旗空+数据根 pyenv-components 现状+frontmost
# 2) 退生产(osascript quit com.myssia.app)→ SMOKE 直跑:
#    nohup env MYIA_SHOW_ON_START=1 MYIA_SMOKE_GEOMETRY=1400x1050+860+16 MYIA_SMOKE_ROUTE=settings \
#      /Applications/世事.app/Contents/MacOS/MYIA > /tmp/app.log 2>&1 &
# 3) CGWindowList 找自家窗 id → System Events AX:设置分区「Python 环境」AXPress
#    → 可选组件分区 AX 读(组件开关 <id> checkbox value/徽标 未装|已装)
# 4) AXPress 开关 → 轮询 <数据根>/pyenv-components/<id>.json(戳 ready+指纹对账)
# 5) probe 两层:自管 env console script --probe + headless handle_wechat_local("probe",{})
# 6) 收尾:quit → open -g 复原 → 六旗核空 → 私有临时件清
```

# 装机件像素目验 — 世事.app 消息屏微信区(2026-10-11 23:32-23:52)

> 执行件:像素目验员(「全部解决」令三件挂起的像素目验件;交付判例 = AI 自己验到装机件像素级)。
> 对象 = **装机后的 `/Applications/世事.app`(0.0.3,22:13 换装包,二进制 inode 324108409 谱系)**的消息屏(`#/messaging`)微信区。
> 红线纪律:零合成点击(CGEvent 零发)、不抢前台焦点(唯一一次违和=直跑启动瞬间的系统级行为,已即回,见 §5)、绝不触碰微信窗口(微信全程未做任何操作)。
> 私有数据红线:全帧截图含通道目录行(主人私有推送目录)→ 0700 私有临时目录 `/tmp/wx-vis-Fsu4UT` 用后即清,不入 git;入 git 的只有**脱敏裁剪件**(微信本机卡区域,纯 UI 铬层文字,`wechat-card-messaging-screen.png`)与本档文字证据;OCR/VL 原始输出中的目录预览行(会话 id/群名)不转录进本档。
> OCR 链 = local-ocr 三级:一级 Swift+Vision(逐行置信度)→ 二级本机 mlx-vlm Qwen3-VL-8B(127.0.0.1:8080,已驻,零出网)→ 云端未启用(二级已闭合)。

## 0. 结论速览

| 验收点 | 判定 | 像素证据(tier-1 Vision 置信度) | 二级/无头补强 |
|---|---|---|---|
| 「微信本机」卡在册 | **命中** | 总览网格卡(VL 确认「微信本机」卡在图)+ 工作区卡题 `微信本机`(conf 1.00) | VL 二级逐字确认 |
| 三态文案如实 | **命中** | 胶囊 `降级`(1.00)+ 版本行 `微信 4.1.15 / 桥组件 0.2.0`(0.30)+ 降级原因 `key_unavailable —…`(0.50,fix_hint 全文与探针逐字同) | VL 二级逐字确认 + sidecar 层探针同载荷对账(§2.3) |
| 只读会话入口可见 | **像素未命中(折叠下)** | 入口按钮在视口折线之下,全帧 OCR 未命中 | 无头补强:描述行「选会话 → 拉最近消息展示;读回不入情报管线」已像素命中(0.50);按钮为常驻渲染(wechat-local.tsx SessionReader,组件测试在库);未做点击(铁律) |
| AX 权限引导卡文案 | **命中(题行+徽标)** | `系统权限引导:辅助功能(AX)`(1.00)+ 徽标 `已授权`(0.50) | VL 二级逐字确认;卡体步骤文案折线下未命中(§3) |
| 官方微信卡共存 | **命中** | 总览网格 `微信` 卡与 `微信本机` 卡同图共存(VL 二级:双卡都在,状态标记各现);工作区描述行自带分工文案「与上方「微信」官方桥分工,出站归官方桥」(0.50) | VL 二级确认 |
| 收尾 | **全绿** | launchctl MYIA_* 六旗全空;冒烟进程退净;复原实例亮窗 0;frontmost 归主人侧 app | §6 |

## 1. 判例链执行记录(命令原样)

1. **基线取证**(23:32):frontmost=ZCode;`launchctl getenv` MYIA 六旗全空;显示器逻辑 1920×1080;CG 全量:世事族 2 窗(1920×1080 主窗 + 500×500 助手窗,**全 offscreen**=隐藏窗出厂态),微信族 31 窗全 ordered-off(托盘态);既有生产实例 pid 48118 + 托管 sidecar 48126 在跑。
2. **探针地面真值**(装机 bin 直跑,`MYIA_WECHAT_BRIDGE_PYTHON=仓库 .venv`):`degraded` + reasons `[window_closed, key_unavailable]`、`main_window=fail`——fail 根因 = **装机件是 0.2.0(22:42 装),早于 23:20 的 zh-CN 属主名双名修正**(§4.1),与 0.3.0 源码行为差异如实记档。
3. **退既有实例**:`osascript quit app id com.myssia.app`(装机回执 §4 同款温和口径,零夺焦);MYIA 与 sidecar 各 ≤10s 退净(sidecar stdin EOF 自清复证)。
4. **SMOKE 直跑**(禁 open -a 闪窗,env 只进本进程):
   `nohup env MYIA_SHOW_ON_START=1 MYIA_SMOKE_GEOMETRY=1040x1900+860+16 MYIA_SMOKE_ROUTE=messaging /Applications/世事.app/Contents/MacOS/MYIA &`
   - setup done 169ms(sidecar spawned);CG 全量找窗:**window id=77752**(世事,on-screen,实测落位 1040×1050@ (860,30)——**高度被系统钳到可见帧 1050**,1900 请求不达,见 §4.4)。
   - 亮窗时 frontmost 短暂转 MYIA(直跑启动系统行为,非 set_focus;R2 无焦点路径照走)→ 即以 System Events `set frontmost ZCode` 归还,后续 frontmost 采样再未属 MYIA。
5. **截图**:`screencapture -x -o -l 77752`(静默零交互),PNG 2080×2100(=1040×1050@2x,`-o` 无阴影);64×64 降采样 luma mean 36.6/min 20/max 93 → **实内容非黑图**(TCC 屏幕录制:ZCode 在册,§基线 TCC 实读)。
6. **路由纠偏**(如实):`MYIA_SMOKE_ROUTE=messaging` 在装机包上未生效(落地屏非消息屏,首帧 OCR 实读为 YAML 配置屏;根因本轮未查明——候选=webview 会话态恢复晚于两趟 hash eval,未深挖)。改走 **10-07 判例同款 AX 通道**(对自家窗,零激活):System Events 走查 `窗口1>组1>滚动区1>web 区`,于 `组[主导航]` 子件 8(名=`消息`)`perform action "AXPress"` → 2.5s 后截帧即消息屏(AXPress 前后 frontmost 均=主人侧 app,零激活复证)。
7. **视口垫高**(对自家窗的 AX resize,10-07「AX 大幅 resize 逼全量瓦片重绘」判例):`set size` 1040×1050 → 1396×1050(1900 高再次被钳 1050;1920 宽请求被系统拒,维持 1396)→ 折线上移,露出版本行/原因行/AX 卡题/徽标。
8. **OCR 链**:一级 `swift /tmp/wx-vis-ocr.swift`(VNRecognizeTextRequest accurate,zh-Hans+en-US,逐行置信度);二级对 ≤0.5 验收行裁剪件走本机 VL(`127.0.0.1:8080` qwen3-vl-8b-mlx,零出网,逐行转写式)——**两条 ≤0.30 关键行(版本行/总览卡行)经二级逐字确认无误**。
9. **无头补强**(判例注意预案的折叠下条款):`PYTHONPATH=/Applications/世事.app/Contents/Resources/myssia-src`(仓库 .venv 供依赖)直调 `handle_wechat_local("probe",{})` = 卡片真源,载荷与像素文案逐键对账(§2.3)。

## 2. 验收点明细

### 2.1 「微信本机」卡在册 + 官方微信卡共存(像素)

- 总览平台卡网格:VL 二级对 cards 裁剪件转写,`「微信」卡`与`「微信本机」卡`**同图并存**、各自带状态标记;一级 Vision 对应行 `微微信`(0.30,卡名小字)+ 网格含 Telegram/飞书/钉钉/企业微信 等 20+ 平台卡。
- 工作区卡题:`微信本机` conf **1.00**;分工描述行 `…与上方「微信」官方桥分工,出站归官方桥` conf 0.50(VL 逐字确认)——**双卡三态独立不混用**的 UI 语义在装机件像素层成立(design §5.2)。
- 脱敏裁剪件(入 git):`research/wechat-card-messaging-screen.png`(2352×540,微信本机卡区域, Vision OCR 全行复核=纯 UI 铬层文字,零目录/会话/内容行)。

### 2.2 三态文案如实(像素 ↔ 数据双面)

像素面(消息屏工作区卡头,run5 帧):

| 行 | tier-1 conf | tier-2 VL |
|---|---|---|
| `微信本机` + 胶囊 `降级` | 1.00 / 1.00 | 逐字同 |
| `微信 4.1.15 / 桥组件 0.2.0` | 0.30 | **逐字同** |
| `key_unavailable — 零内存密钥途径(key_info.db)实测不可推导(E1 真跑:候选全数离线 HMAC 未命中;材料疑被机器专属密钥包裹);D4 待主人裁决:…` | 0.50 | **逐字同**(fix_hint 全文) |
| `系统权限引导:辅助功能(AX)` + 徽标 `已授权` | 1.00 / 0.50 | 逐字同 |

数据面(同上下文无头探针,即卡片渲染真源):`state=degraded`、`checks={bridge_component ok, wechat_process ok, ax_permission ok, main_window unknown, localdb_storage ok, localdb_key unavailable, ax_tree unknown}`、`wechat_version="4.1.15"`、`bridge_version="0.2.0"`、`reasons=[{code: key_unavailable}]`。

**逐键对账**:版本行=wechat_version+bridge_version 原文;原因行=reasons[0].code+fix_hint 原文;胶囊=state 直映射(ok→可用/degraded→降级/其余→不可用);AX 徽标=checks.ax_permission(ok→已授权)。**像素文案与探针载荷零漂移 = 「三态如实」在装机件成立**。

### 2.3 状态值的两点如实注记(非缺陷,防误读)

1. **`降级`/`已授权` 是本验证启动语境的真值,非生产语境的必然值**:冒烟实例由会话宿主 shell 直跑,macOS 责任进程归因链把 TCC 授权归到宿主(ZCode,辅助功能在册,TCC.db 实读 com.myssia.app **无**授权条目)→ 探针 `ax_permission=ok`。生产形态(launchd/`open` 拉起,授权主体=世事.app 本体)探针将如实转 `bridge_unavailable`/`未授权`(F5 的 AX 授权引导真机走通项,UI 文案两面都已在库)。**本验证验证的是「文案=探针真值」这一如实性,不是某个特定状态值。**
2. **`main_window=unknown`(非 fail)**:装机探针走自管 python(无 pyobjc,组件可选依赖)→ unknown 如实上报 → 不产 window_closed 原因。像素面未见 window_closed 行,与载荷一致。

## 3. 折叠下未命中条款(判例注意预案,如实)

视口高被钳 1050(§4.4),页面在「微信本机」工作区卡中部折断,以下三项**全帧 OCR 未命中**,按预案落无头补强:

| 项 | 未命中内容 | 无头补强(非像素,如实标注) |
|---|---|---|
| 只读会话入口按钮 | `拉取会话列表` 钮/会话列表面板 | 入口描述行已像素命中(§2.1 描述行含「选会话 → 拉最近消息展示」);按钮=常驻渲染(wechat-local.tsx SessionReader,`data-testid=wechat-local-load-sessions`),无探针分支遮挡;**未点击**(零合成点击铁律,且点击即触发真拉取,超验证边界) |
| AX 引导卡体步骤文案 | `系统设置 → 隐私与安全性 → 辅助功能` 步骤段(折线处半行残影,OCR 呈乱符=视口折叠切割,非渲染缺陷) | 卡题+徽标已像素命中(§2.2);卡体=常驻渲染(wechat-local.tsx AX 引导块) |
| 本地库查询行 | `本地库查询(历史)` 输入行 | 同卡常驻区块(LocalDbQuery);探针 key_unavailable 已像素命中,该行的如实报错语义由同一真源保证 |

折叠下三块的渲染逻辑均有组件测试在库(`desktop/ui-src/src/screens/messaging/wechat-local.test.tsx`)。

## 4. 如实发现(移交主会话)

1. **装机组件落后于源码两笔**:装机件 `~/.myia/plugins/wechat-bridge` = **0.2.0**(22:42 rsync 自当时工作树),早于 23:01 D4(b6f1134,mem_search 终形+key-scan)与 23:20 D2(8627921,**pixel.py C1/C2 + zh-CN 属主名双名修正,0.3.0**);装机件无 pixel.py,`--probe` 的 main_window 在有 Quartz 环境下仍判 fail(旧单名匹配)。像素面版本行如实显示 `桥组件 0.2.0`。**建议:组件装机刷新到 0.3.0 后复跑本目验的 §1.2/§2.3 两点**(UI 本身无需重验——F3/F4 均在 22:13 装机包内)。
2. **MYIA_SMOKE_ROUTE 在装机包未生效**:落地屏非路由目标(候选根因=webview 会话态恢复时序,未深挖,装机包行为与 10-07 判例时代存在差异)。本轮以 AXPress 自家侧栏兜底;后续验证若复用此判例链应先截首帧核路由。
3. **窗高钳制**:SMOKE_GEOMETRY 高度请求(1900)经 Tauri 与 System Events AX resize 两路均被系统钳到可见帧 1050;宽度可调(1040→1396)。长页折叠是本判例链的固有视场约束,§3 预案即为此设。
4. **启动瞬间焦点短暂转移**:直跑二进制亮窗时 frontmost 短暂属 MYIA(SHOW_ON_START 无焦点路径照走,系统级窗口浮现行为),即检测即归还 ZCode;此后每次采样 frontmost 均为主人侧 app。10-07 判例记录「前台全程不变」与本轮差异如实记档(本轮主人正在实机操作,采样更密)。
5. **主人并行使用**:验证窗口期内主人侧自身操作(微信置前、开窗;WeChat 族 31 窗全 offscreen → 收尾时 30 窗 2 onscreen)均系主人行为;本验证对微信的**全部操作=零**(§5)。

## 5. 静默面自查(动作台账)

- **对微信**:零调用、零窗口操作、零 AX/合成事件、零进程接触。微信进程全程未被本验证点名(pgrep 采样除外)。
- **对自家冒烟实例**:AXPress×1(侧栏「消息」导航,零激活)、AX size set×2(自家窗,零激活)、AXEnhancedUserInterface set×1(-25208 拒,无副作用)、screencapture -l×5(静默零交互)。
- **对主人前台**:frontmost 变更一次(启动浮现,即还)+ `open -g` 复原(零焦点,亮窗 0 实证)。
- **零出网**(除既驻本机 VL 服务 127.0.0.1:8080 的两级链调用;云端三级未启用)。

## 6. 收尾回执(全部亲验)

| 项 | 结果 |
|---|---|
| 冒烟实例退出 | `osascript quit` → MYIA、sidecar 双退净(rc=1=无进程) |
| 生产实例复原 | `open -g /Applications/世事.app` → pid 8848,世事族 2 窗全 offscreen(**亮窗 0**),frontmost=主人侧 app(WeChat)未变 |
| env-flags=0 | launchctl `MYIA_SHOW_ON_START/SMOKE_GEOMETRY/SMOKE_ROUTE/SMOKE_FOCUS/HOME/PYENV_AUTOSETUP` 六旗全空(env 只进直跑进程,无 launchctl setenv 污染) |
| 私有临时件 | `/tmp/wx-vis-Fsu4UT`(0700)含全帧 5 张+裁剪+OCR/VL 输出,含通道目录私有行 → 本档写毕即清;入 git 仅脱敏裁剪件与本文 |
| 复原语义 | 与验证前状态对齐:生产实例静默后台跑 0.0.3 包 + 托管 sidecar;微信托盘态未被本验证改变 |

## 7. 复跑指南

```bash
# 1) 基线+退既有实例(温和,零夺焦)
osascript -e 'quit app id "com.myssia.app"'
# 2) SMOKE 直跑(env 只进本进程;路由未生效需 §1.6 AX 导航兜底)
nohup env MYIA_SHOW_ON_START=1 MYIA_SMOKE_GEOMETRY=1400x1050+860+16 MYIA_SMOKE_ROUTE=messaging \
  /Applications/世事.app/Contents/MacOS/MYIA > /tmp/app.log 2>&1 &
# 3) CG 找窗 id → 截图 → 一级 Vision → ≤0.5 行裁剪走本机 VL(127.0.0.1:8080)
screencapture -x -o -l <window_id> /tmp/frame.png
# 4) 无头对账:卡片真源探针
PYTHONPATH=/Applications/世事.app/Contents/Resources/myssia-src <venv> python -c \
  'from myssia.wechat_local_sidecar import handle_wechat_local; print(handle_wechat_local("probe", {}))'
# 5) 收尾:quit → open -g 复原 → launchctl getenv MYIA_* 六旗核空
```


---

## 附批:2026-10-12 15:31–15:40 「自己点」批像素补全(主会话直做,工作流 dwfrun-4adba09e 额度墙后降级)

> 背景:子代理额度墙(GLM-5.3-Flash 5h 帽,15:42 重置)后按在案打法主会话直做;换装含 COMPONENT_META 修复(d8fd49d)的新包(18.19MiB,15:29 门禁全绿 pytest 5414/48skip+vitest 762 后重打)。

### 验收点命中(消息屏首帧,/tmp 用后即清,本档只留 OCR 文本证据)

| 验收点 | 判定 | OCR 证据(逐字) |
|---|---|---|
| 微信本机卡+分工文案 | 命中 | 「微信本机 / 本机桥只读面(选会话→拉最近消息展示;读回不入情报管线)+本地库三域查询;与上方『微信』官方桥分工,出站归官方桥」 |
| 双卡共存 | 命中 | 同帧「3o 微信」(官方卡)与「微信本机」并列 |
| 三态如实(沙箱语境) | 命中 | 「不可用」+原因全文「Python 运行环境未配置…(code=pyenv_not_ready)」——沙箱 MYIA_HOME 未配 env 的正确降级链,生产语境为 degraded(装机回执在案) |
| AX 权限引导卡 | 命中 | 「系统权限引导:辅助功能(AX)…授权主体是 MYIA app 本体(装机一次性)…桥不抢前台焦点、不合成鼠标点击、不激活微信窗口(静默铁律)」 |
| **只读会话入口钮(上批视口钳制未命中,本批命中)** | 命中 | 「只读会话入口 拉回的消息仅此处展示,不进情报流、不打标、不去重(G3)」 |
| 本地库查询行 | 命中 | 「本地库查询(历史)解密副本只读,零出网零微信进程交互;密钥途径未裁决(D4)时如实报 key_unavailable」+会话 id 输入+30 天+「查询本地库」「拉取会话列表」双钮 |

### 设置页新文案(COMPONENT_META)证据形态

像素帧未取(SMOKE_ROUTE 复现不生效,769edce 缺口④ AX 失联现象本批再复现:窗口渲染内容但 System Events 零窗)——**以 vitest 契约测试为证据源**:pyenv-components.test.tsx 新增用例断言 wechat-bridge 行渲染「微信本机桥(wechat-bridge)」+「像素链读」+已装徽标(21 passed,d8fd49d)。

### 事故与偏差(如实)

1. **闪窗事故 ~16s(15:31)**:SMOKE 几何格式误用逗号形态(600,60,900,700)未生效→实例开全尺寸窗上屏;判例正确格式为 `WxH+X+Y`(900x700+600+60),修正后正常。主人 frontmost 全程未失(ZCode/微信侧)。
2. **生产实例窗被带上屏(15:33)**:SMOKE 启动把生产主窗 ordered-in(单实例路由疑似),osascript visible=false 即还;收尾时生产进程已自退,open -g 复原。
3. SMOKE_ROUTE=messaging 本批**生效**(与 769edce 批相反)——两批一正一反坐实「路由生效不稳定」,根因仍悬(webview 会话态时序假说),记档不深挖。
4. 收尾核验:launchctl 六旗全空/世事在屏窗 0/临时件(/tmp 双 home+distverify venv)清空。

### 附:本批两笔收口提交

- d8fd49d COMPONENT_META 补行(自点批缺口①)
- 105dfa9 install-receipt §8.3 勘误(缺口②;③④⑤ 记档级,无需代码)

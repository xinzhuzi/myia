# D2 像素链读通道 — 截窗三态实测 + C1/C2 端到端(2026-10-11)

> 执行件:像素工(10-11-wechat-ui-bridge Phase C1/C2,主人「全部解决」令 D2 认领)。
> **红线 3/4 纪律**:全程零激活调用、零合成点击、零前台抢夺(screencapture -l
> 对后台窗零交互;前后 frontmost 对照见 §6);截图/裁剪件含聊天内容 → 0700
> 私有临时目录用后即清;**本文零聊天内容、零会话名**,证据只留形状(计数/
> 坐标带/字符类形状/时长/码值)+ 一条脱敏样例(§2)。
> 实现件:`plugins/wechat-bridge/wechat_bridge/pixel.py`(C1/C2 落位,`ax.py`
> 委托,`cli.py` emit;单测 `tests/wechat-bridge/test_pixel.py` + 合成渲染器
> `tests/wechat-bridge/pixel_fixture.py`)。

## 0. 结论速览

| 项 | 定论 |
|---|---|
| 截窗三态(ask 判例) | **ordered-off(托盘/未 ordered-on)主窗实测可出完整合成帧**——三态判定落「出图」,非黑图非失败;`screencapture -x -o -l <id>` 出精确窗口内容 3840×2100(§1) |
| C1 会话列表(真跑) | 15 行(名字 15/预览 12/时间锚 8/未读徽标当帧 0 可数);Vision 0.45s + VL 修字 8 行,全程 11.9s(§2) |
| C2 消息区(真跑) | 最近 10 条(side 左 9/右 1,发送者命中 6,ts=居中时间标记);VL 修字 2 行,全程 7.9s;`chat.match=false` 如实(§3) |
| 合成 fixture(徽标/对组路径) | Vision 真跑:名字 **8/8**、未读 **5/8**(单数字徽标 Vision 漏读 3 例、`999+` 读成 `999`,误差如实);C2 消息 5/5 + 发送者 2/2(§4) |
| 静默取证 | frontmost 前后不变;零窗口操作(§6) |
| 门禁 | 组件 165p/7s;`MYIA_WECHAT_E2E=1` → **172p/0s**(真机链全过);全仓 5355p/47s;ruff 全绿(§7) |

## 1. 截窗三态判定(ask 判例:出图/黑图/失败)

前置:微信 4.1.15 运行中(pid 85172),CGWindowList 全量 233 窗、微信族 31 窗、
**onscreen=0**(ordered-off 残影态,与 A1 时间线一致);主窗
`window_id=48419`(1920×1050@layer0,属主名=**「微信」**,zh-CN 形态)。

| 命令 | 实测 |
|---|---|
| `screencapture -x -l 48419` | exit 0,PNG **3976×2236 RGBA**(=3840×2100 内容 + 68px@2x 阴影边);64×36 降采样 luma 均值 39.4、min 5、max 245、1235 种颜色 → **实内容非黑图** |
| `screencapture -x -o -l 48419` | exit 0,PNG **3840×2100**(`-o` 去阴影=精确窗口内容,坐标原点=内容左上,组件缺省用此形态) |

- **黑图判定**(组件内):64×36 降采样 luma 均值 <8 且极差 <10 → `screen_capture_black`(exit 1 过渡码;典型原因=宿主缺「屏幕录制」TCC 授权,fix_hint 指系统设置路径)。真窗 mean 37-40,远离黑图阈。
- **判例升级**:prd/ax-probe 曾预期「后台未激活窗可能不合成」——本机实测
  (macOS 26.4 + 微信 4.1.15)**ordered-off 窗完整合成**。附注:两轮真跑帧内容
  不同(居中时间标记一轮 23:03、一轮 23:08,与主人侧实时使用吻合)→ 窗口
  服务器对 ordered-off 窗仍持续更新帧;组件仍保守保留「最后渲染帧可能非实时」
  注记(`window.note`),不把观测当保证。
- **失败态**:screencapture 退出码非零/产物缺失 → `screen_capture_failed`;
  子进程超时 → §6 exit 30。三态判定落 `pixel.capture_window`,单测三态全覆盖
  (mock runner + 真 PNG;真机态走 `MYIA_WECHAT_E2E=1`)。

## 2. C1 真跑:sessions list(形状级)

```
python -m wechat_bridge sessions list --json        # exit 0,11.9s
capture: {state: ok, 3840×2100, mean_luma 37.5}
ocr: {engine: vision, elapsed_s: 0.446, n_lines: 65, low_conf_lines: 25}
vl:  {used: true, corrected_lines: 8, model: …/qwen3-vl-8b-mlx, downsampled: true}
parse: {rows: 15, time_anchors: 8, with_preview: 12, with_time: 8, with_unread: 0}
```

- 载荷 `sessions[]` 键 = `{id, name, unread, time, preview, conf}`(id=name,
  §6 契约三键 + 诊断附加;unread 像素链下可 null 如实)。
- **脱敏样例一条**(形状,零内容):`{name: C×5(5字, conf=1.00), unread: null,
  time: "23:08", preview: 13字}`。
- 时间锚命中形态:`HH:MM`×5、`星期一`、`M/D`×2(8/15 行;其余行时间被 Vision
  漏读 → 名字+预览**对组趟**兜底恢复,时间/未读如实 None)。
- VL 二级:25 低置信行中,门按**行 conf** 只送低置信会话名(+其预览)共 8 行
  修字,几何零改动;降采样 3840→2048(显式路径,LANCZOS)。
- 未读徽标:本帧无一处可数数字(主人侧刚读过)。徽标路径由合成 fixture 钉死
  (§4):数字/`999+` → int;单数字白字红圈徽标 Vision 漏读 3/6(`12`/`999+`
  两种可读,`3`/`1`/`2` 全漏)——**unread 命中率是像素链已知短板**,如实。

## 3. C2 真跑:messages read(形状级)

```
python -m wechat_bridge messages read <合成请求id> -k 10 --json    # exit 0,7.9s
chat: {requested_id: 6字, visible_title: 24字, match: false, note: 有}
ocr: {engine: vision, n_lines: 17(裁剪件), low_conf_lines: 3}
vl:  {used: true, corrected_lines: 2, downsampled: true}
parse: {blocks: 17, markers: 1, left: 15, right: 1, with_sender: 6, low_conf_lines: 3}
messages: 10 条 = {ts: "23:03"|null, sender: 4-10字|null, type: "text", text, side, conf}
```

- **静默硬边界兑现**:请求 id 为合成值 → `match=false` + note(「读到的是当前
  打开会话」),不静默张冠李戴;标题(24 字)自全窗锚定趟读出。
- 裁剪:聊天区 = 列表时间锚右缘 +0.01 → 1.0(数据驱动,无本机像素硬编码;
  无锚回落实测缺省 0.215)。
- 误差如实:`ocr.parse.caveat` 常驻载荷(发送者启发式/换行合并/媒体类读不出
  → 像素链不可判「类型+占位」,缺行即缺)。

## 4. 合成 fixture 验证(徽标/对组路径 + 离线回归锚)

渲染器 `tests/wechat-bridge/pixel_fixture.py`:3840×2100 深色主题、8 行会话
(名字/时间/预览/未读 None|1|3|12|99+|999+ 混合)+ 聊天区(标题/居中时间/左气
泡带发送者/右气泡),**全部文字为显式合成内容(「合成会话X」/「合成消息…」),
零私有数据,fixture PNG 已入 git**(`fixtures/synthetic_wechat_panel.png`)。

| 项 | Vision 真跑结果 |
|---|---|
| C1 名字 | **8/8**(两趟组装:时间锚 5 + 对组兜底 3;顺序=窗口自上而下) |
| C1 未读 | 5/8(`999+` 读成 `999` 计命中;`3`/`1`/`2` 单数字徽标全漏读) |
| C1 聊天区噪声 | 零污染(居中时间/气泡/发送者不成行) |
| C2 消息 | 5/5(裁剪趟;ts 标记 2、发送者 2/2、右气泡 2/2) |

单测面(`test_pixel.py`,29 例):两趟解析真值全对/limit 截断/空行、消息标记/
发送者/换行合并/K 截断/chat.match 归一化、VL 应答解析(保行数保序/不可解析保
初稿/服务缺位如实)、截窗三态(mock)/超时→exit 30、窗口定位(onscreen 优先/
英文名属主/零窗 None)、编排注入(载荷形状/私有目录用后即清/match 三态)、
CLI 接线(exit 0 契约载荷/窗闭 exit 12)、属主名对账回归。

## 5. 关键实测发现(反直觉三条,均有证据)

1. **VL 全量校对后再解析 = 失稳**:首轮实现按 local-ocr 技能惯例「低置信 →
   VL 校对全量行 → 再解析」,真跑 50.7s 得 rows=10/with_time=0(时间锚文本被
   VL 改写不再匹配 `HH:MM/昨天/周X` 形态,行配对连锁失稳)。**改定架构:解析
   以一级 Vision 原始几何为准,VL 解析后只对低置信行修字回填**(真跑 11.9s,
   行数/时间命中恢复正常)。local-ocr 技能的「校对模式」用于成品文本修正成
   立,用于「校对后回解析」不成立——几何敏感场景勿混用。
2. **CG 窗口属主名 zh-CN=「微信」**:`system_checks.wechat_main_window_open`
   原比对 `"WeChat"` 字面 → zh-CN 系统恒 False(B 段探针「主窗口 fail(托盘)」
   实为误判叠加)。已修:`WECHAT_OWNER_NAMES=("微信","WeChat")` 双名匹配,
   probe/像素层同源对账(单测钉死)。
3. **徽标与时间同右对齐、位于时间行下方**(行中垂直居中),非「时间右缘之外」
   ——徽标带按行右缘 `[-0.045, +0.008]` × y 偏移带 `[-0.005, 0.026]` 定位
   (合成 fixture 真值验证)。

## 6. 静默取证(AC4 口径)

- frontmost:CLI sessions list / messages read / --probe 前后均 `ZCode`(会话
  宿主),零变化;`screencapture -x` 静默(无快门声)、`-l` 窗口直取(不激活
  不枚举 AX 不合成事件)。
- 全程零合成点击、零 AX 动作 perform、零窗口开合;与 A1 探查同口径。
- 窗口列表对照:探查前后 CGWindowList 微信族均在册 ordered-off 态(31/33 窗
  级浮动属主人侧使用,非桥致)。

## 7. 测试与门禁(本会话亲跑)

| 门禁 | 命令 | 结果 |
|---|---|---|
| 组件单测 | `uv run --no-sync python -m pytest tests/wechat-bridge -q` | **165 passed / 7 skipped**(skip=门控真机) |
| 真机链 gated | `MYIA_WECHAT_E2E=1 …` 同上 | **172 passed / 0 skipped**(真截窗/真 Vision/真 VL 全过,28.1s) |
| 全仓回归 | `uv run --no-sync python -m pytest -q` | **5355 passed / 47 skipped / 0 failed**(144.3s) |
| ruff | `uvx ruff@0.16.10 check .` | All checks passed |
| golden | `MYIA_WECHAT_BRIDGE_REGEN_GOLDEN=1` 再生成 | 契约对账稳定(bridge_version 0.2.0→0.3.0 一行) |

## 8. 移交注记(主会话裁决/勾选项)

1. **勾选**:implement.md C1/C2 复选框归主会话(本档不代勾,执行增补已注)。
2. **§6 码表扩充候选**(design §6 封闭表,须先改 design):像素层过渡码
   `screen_capture_failed` / `screen_capture_black` / `ocr_unavailable`
   (exit 1 段,not_implemented 同款纪律,不谎报具名族)——建议主会话裁决
   是否转正为具名族(如 16 screen_capture_failed / 17 screen_permission_denied)。
3. **契约超集语义**:`unread: null`(徽标不可见时)、附加键
   window/capture/ocr/chat——probe 先例「additive, 消费端宽容」;`messages
   read` 的 `chat.match=false` 建议消费方(UI 卡)显式提示「当前打开会话与请求
   不符」。
4. **probe 窗口态语义修订已落**:`wechat_main_window_open` = CG 在册即真
   (ordered-off 可截);若主人侧期望 probe 仍区分 ordered-on/ordered-off,
   可在 checks 增列(现未加,保 golden 键集稳定)。
5. **并行会话共线注记**:`cli.py` 的 C1/C2 emit 接线与 D4 工的 key-scan 分支
   同文件并行开发,接线随其提交 b6f1134 先行落库;本提交为像素层其余全量
   (pathspec 限定自建/自改文件)。
6. **组件版本**:0.2.0 → 0.3.0(C1/C2 落地;`__init__`/`component.json`/
   golden 三处同步,stamp 测试钉死)。

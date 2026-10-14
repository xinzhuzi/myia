# 微信 send_text 三源合体升级设计(task 10-14-wechat-send-text)

设计员产出,2026-10-14;**三轮修订版**(第一轮质询 13 条 + 第二轮 9 条 + 第三轮真机
dry-run r2 实测三缺陷,处置记录见 §J,全部已并入正文,正文即修订后终态)。执行者照此
实现,零设计自由度;凡标「可翻案点」处为主人保留的裁决位(默认方案已选,翻案须改本档)。

输入材料(本文全部断言的出处):
- **桥勘察**(任务 ask 内嵌):现状 send 链逐行锚点(sendui.py/cli.py/ax.py/send_state.py/pixel.py/codes.py/system_checks.py/README.md + 装机启动器)。
- **靶场勘察**(任务 ask 内嵌):真机 2026-10-14 只读核查——微信 4.1.15(pid 91831)、AX 门开(ax_chat_test 可读「当前聊天: AI中转站-♾️ AI Token」+ 自写探针 122 节点)、两白名单目标 DB 解析实证(filehelper→文件传输助手;wxid_m90epbt5ojml22→alias jiangliushi666/nick 🐳)、装机桥 send_text --help 与 localdb query 冒烟通过。
- **蓝本三份**(`research/` 下,必读):
  - `research/wuziyong_wechatctl.swift`(下称 WZ;验证协议/CGEvent 源/清空轮询/防重)
  - `research/ref_search_click.sh`(下称 REF;tonyshield 分区过滤导航)
  - `research/FINDINGS.md`(下称 REV;AX 门 LLDB 配方/元素链)
- 桥源码与测试实读:sendui.py(555 行)/cli.py(523;send 分支 336-359、key-acquire hint clamp 152-164)/ax.py(129)/send_state.py(224;_write_unlocked 单键整写 125-134、rollback unlink 分支 174-184)/codes.py(112)/pixel.py(WindowInfo:126-148、OcrLine:151-160、SessionRow.to_payload:173-177、_chat_match:1161-1169)/localdb.py(query_history:1547-1556)/localdb_query.py(lookup_contact:363、_normalize_ts:192-200)/system_checks.py/probe.py/config.py/README.md(红线:63-68)/test_send_state.py(104-141 占位用例断言 float;rollback 断言 `not path.exists()` 120-128)/test_bridge_cli.py(55-113 既有 send 用例)。
- **第三轮真机证据(2026-10-14 03:2x,r2 dry-run,证据 /tmp/wxsend-e2e/ 与 /tmp/wxsend-e2e/r2/,装机桥 0.8.0)**:
  - 两目标 dry-run 均 exit 15「阶段=navigate:搜索结果面板无可定位行(分区过滤零候选)」(r2/01-filehelper-stdout.json、02-jl666-stdout.json 实读)。
  - 不存在联系人 → exit 1 send_target_not_found,零 UI 扰动(r2/03-nonexist-stdout.json 实读;DB 侧三形态 resolve 好消息)。
  - 主窗 AX 全树(axwalk2-out.txt 实读):具名元素 `current_chat_name_label`/`chat_input_field`/`chat_message_list`/`virtual_cell`/`tabbar_*`/`main_window_main_splitter_view` 全在 **AXIdentifier 列**(desc 列基本空)。
  - 搜索态窗序颠倒:搜索浮窗成 window 1、主窗退 window 3(主人 System Events 枚举实证 win1=368x370 匿名树/win3=微信 4 顶元素,浮窗 wid 96202;我侧未复跑枚举,以 ask 材料为准);doctor 在该形态数到 nodes=4 报 closed(doctor-after-p3-inproc.json 实读 ax_gate.nodes=4/input_field=missing——数的是浮窗)。
  - 好消息:doctor BFS 深度判据在正常态工作(门=open,nodes 76~123);搜索词 OCR 实证进框;浮窗内目标行俱在(「filehelper 文件传输助手」「微信号:jiangliushi666」在最常使用区顶部——截图证据模型侧不可视,以 ask 的 OCR 描述为准)。

---

## 0. 目标与不做什么

把 send_text 从「盲回车单链」升级为「DB 双验证 + 分区过滤导航(零盲回车)+ 验证五件套
+ AX 主链/CGEvent+OCR 降级 + localdb 回执终验」,CLI 补 `--dry-run` 与 `doctor`。

**不做**:自动 LLDB attach(doctor 只探针+给配方,重开是人工按 REV 配方执行);
不做发送按钮点击(发送动作保留唯一回车,见 §I 翻案点 4);不动 G6 硬间隔 ≥10s 语义
(send_state.py:46 不改值);不动读通道(pixel 静默铁律)。

---

## 1. 总架构:一次 send_text 的全序列(终态)

```
CLI(cli.py send_text 分支,替换 cli.py:336-359 的序列但保留分支骨架)
  1) 读 stdin 正文(不变,cli.py:338/249-259)
  2) localdb 链单次解析 ★(§J-19):storage = localdb.locate_db_storage();
     keys = localdb.resolve_keys(storage, config=config) —— 全程只解析这一次,
     注入下方两处消费点(取钥器交互/自愈链不重复挂住发送路径)
  3) DB 侧目标解析 ★新(sendtarget.resolve_target(config, chat_id, storage=, keys=))
     → SendTarget{username,alias,display_name,search_term}
     三形态入参皆可(§B-1);查无 → exit 1 code="send_target_not_found";多义名 →
     exit 1 code="send_target_ambiguous"(拒发,零 UI 扰动)
  4) ax.ensure_ui_preconditions(不变,ax.py:42-83)
  5) G6+防重合成占位 ★扩(send_state.reserve_send_dedup)——同一 flock 临界区,
     门序 = 指纹门在前、间隔门在后(幂等命中不该被间隔拦;WZ:237-247 同序):
       指纹命中 status=sent 且窗内   → exit 0 幂等载荷 {sent:false, deduped:true}(不占位)
       指纹命中 status=pending 且窗内 → exit 17 send_uncertain_dedup(uncertain-never-retry)
       间隔不足(<10s)              → exit 14(不变)
       其余 → 占时间戳(不变);指纹档只在 on_armed(回车 down 前)落 pending
     fingerprint = sha256(SendTarget.username + "\0" + body)(WZ:138-141 同构;键用
     解析后 username——同一人 alias/wxid/展示名三种叫法指纹相同,防重闭合)
  6) --dry-run 跳过 5(零发送零占位零防重检查,可无限重跑)
  7) ax.send_text(config, target, body, *, dry_run=False, on_armed=None,
     on_receipt_green=None, receipt_query=None)
     (on_armed=回车 down 前回调(CLI 传 mark_fingerprint_pending 闭包);
      on_receipt_green=回执全绿回调(mark_fingerprint_sent);receipt_query=注入的
      localdb 回执判定闭包,复用步骤 2 的 storage/keys——sendui 对 localdb 零
      import,依赖方向封闭,§A)
     ── sendui.send_text 内部(单尝试循环 MAX_ATTEMPTS=3 不变)──
     a. 激活+前台断言(不变,sendui.py:385-392)
     b. 通道判定 ★新:axui.probe_wechat_ax() = (AX 门全窗最大节点数>5) AND
        (chat_input_field 可读)——双判据(§D-1);channel = "ax" | "cgevent_ocr";
        跨尝试降级见 §D-1
     c. 导航前基线:OCR 一次标题带记 baseline_title(emoji indirect 证据链的比较基准,
        §D-3;仅降级链需要,AX 通道跳过)
     d. 导航 ★换(零盲回车;现 sendui.py:398-413 的 ↓+Return 整体删除):
        ax 通道:Cmd+F → 搜索词 AXValue 直写零剪贴板 → 轮询 AX 找
                session_item_<display_name> → AXPress(零坐标)
        cgevent_ocr 通道:Cmd+F → 剪贴板粘 search_term → _ocr_region_lines 截窗
                OCR 左栏(裁剪系坐标,§B-3)→ navfilter.select_result_row 分区过滤
                (排除搜一搜/功能分类分区)→ pane_to_window → row_box_to_screen →
                CGEvent 点击目标行(坐标换算链三段,§B-3/§B-5)
     e. 标题双验证(红线 2 第二验):
        ax 通道:axui.read_current_chat_name() 直读(emoji 精确;label 缺位不拦通道,
                走 OCR 兜底,§D-1)
        降级:OCR 标题带(现 _title_matches 保留);display_name 含 emoji 时
              OCR 核不出 → 间接证据链放行+如实标注(§D-3;链不可达 → exit 15 拒发
              是设计内行为)
     f. 发送前哨兵空断言 ★新(五件套件 2):composer 非空 → Cmd+A+Delete 清
        → 复探仍非空 → exit 15 拒发(composer_not_empty)
     g. 写入正文:
        ax 通道:axui.write_input_value(body) AXValue 直写
        降级链:pbcopy + Cmd+V(不变,sendui.py:227-235/420-423)
     h. 粘后回读(四路,新增精确路):
        剪贴板对账 → axui.read_input_value(原 osascript focused element 路由 axui
        取代)→ Cmd+A+Cmd+C 全量复制回读 ★新(长正文精确全量,KEY_C=0x08)
        → OCR 输入带(不变)
     i. dry_run=True → 此处收尾:Cmd+A+Delete 清草稿;降级链若处搜索态再 Esc
        (KEY_ESCAPE=0x35)退出 → 载荷 sent:false,dry_run:true(navigated/pasted/
        readback/nav_debug 如实)→ return(无回车、无 on_armed、零频控副作用)
     j. 发送三段(★异常隔离结构,§C-5:fail-closed 门 + armed 后吞异常):
        j0 **on_armed()**:回车 down 之前调用(= mark_fingerprint_pending;WZ:270-271
            先 pending 后发送同序)。**on_armed 失败 = fail-closed**:异常正常上抛
            (armed 仍 False → CLI rollback → 未回车,可安全重试)——指纹没落就
            绝不进入发送段,宁可不发也不开「无指纹却发出」的双发窗(§J-14)
        j1 发送前聚焦断言(两通道,防回车落搜索框,§D-2;**两通道都是断言不是动作**):
            ax 通道:axui.focus_input()(chat_input_field AXPress)→ 复读
            read_input_value()==body(聚焦未丢正文)→ focused_is_input 尽力断言
            (取 None 如实降为前两条,note 记录)
            降级链:click_at(COMPOSER_POINT) → **哨兵读一致性断言**:read_composer
            回 None(空)或 ==body(正文在框)才算聚焦成立;回异值=焦点不在
            composer → focus 失败(哨兵协议本身即聚焦断言,§J-17)
            聚焦断言失败 → 不上抛(armed 后):重试次数内→下一尝试;耗尽→
            **exit 15 error 载荷**(code=send_ax_focus_required,message 带
            stage=focus 与「pending 已落,120s 内同指纹重发将吃 exit 17」注记,
            §J-20——不破「exit 0 ⇒ sent:true」旧契约)
        j2 唯一一次 post_key(KEY_RETURN)(全函数唯一发送动作)
     k. 发送后验证(恒不抛,§C-5):
        1) 清空轮询 ★新(五件套件 3):哨兵读 composer(AX 通道 read_input_value
           直读零点击;降级链哨兵),12×80ms 内转空 = 发出强证据;超时 → uncertain
           note 如实
        2) localdb 回执终验 ★新(红线 4):调用注入的 receipt_query(username, body,
           since_epoch)——since_epoch = j0 时刻的 epoch 秒(wall_clock 注入点);
           判定=消息 text 空白不敏感对账命中 AND 消息 ts(已归一秒,localdb_query.
           _normalize_ts:192-200)> since_epoch - 2(防同正文历史消息假绿,§C-6);
           轮询退避 RECEIPT_POLL_SCHEDULE=(5.0, 10.0, 15.0) 累计 ~30s(保守覆盖
           E2 副本 mtime 重建耗时,§J-18);链失败 → None 如实 note;True →
           on_receipt_green()(= mark_fingerprint_sent)
        3) 消息区 OCR(现有 _post_send_verify 保留,降为辅助证据)
        全绿 → 指纹升 sent;否则指纹保持 pending(120s 窗内同指纹重发 exit 17 =
        uncertain-never-retry 闭环)
  8) finally:剪贴板复原(不变,sendui.py:536-543)+ 0700 工作目录即清
  9) 载荷(形状见 §E-3;exit 0 语义与消费方迁移注记见 §E-5)
```

AX 主链的中途失败(AXPress/AXValue 写失败)→ 整尝试失败重来(通道判定与降级规则
见 §D-1);**on_armed 调用点之后的一切异常在 sendui 内吞掉**(§C-5)。

---

## 2. §A 模块落点(问 1)

桥风格对齐:中文 docstring、错误码进 codes.py 封闭表、时间与外部调用模块级注入点
(monotonic/sleep/wall_clock/_run)、纯逻辑与平台原语分离(navfilter 零平台依赖 =
单测主战场)。

| 文件 | 动作 | 内容 |
|---|---|---|
| `wechat_bridge/codes.py` | 改 | +`SEND_UNCERTAIN_DEDUP = 17`("send_uncertain_dedup")进 `__all__` 与 `CODE_NAMES`(codes.py:18-35/59-73)。§6 封闭表修订注记写进本档 §E-4。 |
| `wechat_bridge/send_state.py` | 扩 | 防重指纹多槽态;**新原语 `reserve_send_dedup(now, fingerprint)`**;既有 `reserve_send`/`check_send_allowed`/`record_send`/`load_last_send_epoch` 公共行为零改动、`rollback_reserve` 增「有指纹档时移键不删文件」分支(无指纹场景行为不变,test_send_state.py:104-141 既有断言零改);**`_write_unlocked` 私有实现升级为读-改-写保指纹键**(§C-3/§J-16,缺失即 B rollback 抹 A pending 的实洞);`mark_fingerprint_pending/mark_fingerprint_sent`。 |
| `wechat_bridge/sendtarget.py` | **新** | DB 侧目标解析(三形态入参,§B-1;接受 CLI 注入的 storage/keys,§J-19)+ 搜索词选择 + 指纹。 |
| `wechat_bridge/navfilter.py` | **新** | 分区过滤选行纯逻辑 + 裁剪系→全窗→屏幕三段坐标换算(§B-3)。零平台调用、零 import 桥内其它模块(仅 stdlib)。 |
| `wechat_bridge/axui.py` | **新** | AX 读写原语(osascript System Events 封装;_run/SUBPROC_TIMEOUT_S 惯例抄 sendui.py:75-77/177-193)+ 双判据门探针 + focus_input(§B-2/§D-1)。**元素查找底座 = 遍历全部 windows 的 BFS + AXIdentifier 匹配 + missing value→None 规范化**(r2 三缺陷 A/B 的修正,§B-2-r2;二轮 §J-22 只修了 system_checks 计数,axui 底座遗漏在本轮补全)。 |
| `wechat_bridge/sendui.py` | 大改 | 导航段替换、哨兵、聚焦断言(两通道)、清空轮询、通道分层与跨尝试降级、dry_run、on_armed/回执注入、CGEvent 源隔离、`_ocr_region_lines` 新原语、载荷扩键。 |
| `wechat_bridge/pixel.py` | 微改 | `WindowInfo` 加 `x: float = 0.0` / `y: float = 0.0` 字段(pixel.py:126-133;find_main_window 从 kCGWindowBounds 已取的 X/Y 存入,pixel.py:238-249);`to_payload` 加 `"x"/"y"` 键。向后兼容(缺省 0)。 |
| `wechat_bridge/cli.py` | 改 | send_text 分支接线新序列(localdb 单次解析+注入;receipt_query 闭包);`send` parser 加 `--dry-run`;新顶层子命令 `doctor`(见 §E)。 |
| `wechat_bridge/ax.py` | 改 | `send_text(config, target, body, *, dry_run=False, on_armed=None, on_receipt_green=None, receipt_query=None)`;委托 sendui 同签名(docstring 契约同步:on_armed 边界条款)。 |
| `wechat_bridge/system_checks.py` | 扩 | `wechat_ax_node_count() -> int \| None`(**全部窗口最大 UI elements 数**,不绑 window 1——多窗时 z-order 首窗未必主窗,§J-22;osascript 遍历 windows 取 max;可注入)。 |
| `wechat_bridge/probe.py` | 扩 | `run_doctor()`:复用 `run_probe` 全量 + ax_gate 节(见 §E-2)。 |
| `tests/wechat-bridge/` | 新增/扩 | `test_send_target.py`、`test_navfilter.py`、`test_axui.py` 新;`test_send_state.py`(纯新增用例,既有零改)/`test_send_ui.py`/`test_bridge_cli.py`(既有 send 用例签名适配,§G)/`test_probe.py` 扩。 |

模块依赖方向(禁环):cli → {ax, sendtarget, localdb};ax → sendui;
sendui → {sendtarget, navfilter, axui, send_state, pixel};sendtarget → localdb/
localdb_query;navfilter → stdlib only;axui → codes/config。**sendui 不 import
localdb**(回执经 receipt_query Callable 注入——依赖方向与可测性双收)。

---

## 3. §B 导航设计(问 2):搜索词选择 + 分区过滤 + 点击/AXPress,绝不盲回车

### B-1 目标解析与搜索词选择(sendtarget)

**输入面声明(既有输入零破坏)**:`send_text <id>` 的 id 接受三形态——
①username 真源(wxid_…/filehelper/gh_…/@chatroom)、②alias、③**展示名/备注名**
(sessions list 契约的 id 本就是展示名,pixel.py:173-177 `"id": self.name`;
「文件传输助手」「🐳」直接可用)。三形态统一解析到 username 真源。

**关键分离**:`search_term`(进微信搜索框,要求 ASCII 可靠/键盘与 OCR 双友好)与
`row_match_terms`(OCR/AX 行匹配用,把 display_name 也算上——搜索结果行显示的是
display_name,不显示搜索词)。两者都从 SendTarget 派生。

```python
@dataclass(frozen=True)
class SendTarget:
    username: str        # DB 主键(wxid_xxx / filehelper / gh_xxx / @chatroom)
    alias: str | None    # DB alias 列(可空)
    display_name: str    # remark > nick_name > alias(localdb_query._contact_pick_names 同序)
    search_term: str     # 下列规则产物
```

`resolve_target(config, chat_id, *, storage=None, keys=None, data_root=None)
-> SendTarget | None`(CLI 第 3 步调用;storage/keys 由 CLI 步骤 2 单次解析注入,
缺省自解析供单测/复用——**取钥器/自愈交互全程至多一次**,§J-19;多义 → 抛
BridgeError(exit 1, code="send_target_ambiguous")):
1. localdb 链:注入则用之;缺省自跑 `locate_db_storage` + `resolve_keys` +
   `ensure_decrypted_copies`(与 `localdb query` 同链,cli.py:369-371 同款);该链
   任何 BridgeError(20/21/22 族)原样透传,消息注记阶段=「发送前目标解析」(链
   失败=拒发:红线 2 的 DB 侧验证是发送前置;fix_hint 指引 localdb key-acquire)。
2. `sqlite3` 打开 contact 副本(`localdb_query._open_copy` + 列名自适应 `_pick`
   惯例),**三路命中集统一唯一性判据**(§J-21:任何一路多行命中都送 ambiguous,
   绝不静默取首行=潜在错发):
   - 路 ①username 正查(SQL 精确等值;username 本就是唯一键,多行视同库异常 →
     ambiguous 如实);
   - 路 ②alias 反查(SQL 等值拉**全部**命中行;不取首行);
   - 路 ③展示名反查——**SQL 只做全量拉取、Python 侧比对**(compact() 是 Python
     函数进不了 sqlite WHERE;ASCII 名 sqlite 默认 BINARY collation 不折叠大小写,
     §J-21):`SELECT <id>,<alias>,<remark>,<nick_name> FROM contact` 全量(千行级)
     → Python 侧 `compact(remark)==compact(chat_id) or compact(nick_name)==
     compact(chat_id)`(去空白+casefold,展示名中文为主、大小写折叠只影响 ASCII 名)。
   - 判据:三路命中行合集去重(按 username)后 **恰 1 → 建 SendTarget;>1 →
     BridgeError(send_target_ambiguous,fix_hint=「命中多个联系人,请用 alias 或
     username(wxid)消歧」);0 → None**(不查 stranger 表:靶场实证两白名单均无
     stranger 行,contact 表是白名单目标的真源;如实边界,注释写明)。
3. display_name 取 remark>nick_name>alias(与 `_contact_pick_names`
   localdb_query.py:380/419-423 同序)。

`pick_search_term` 规则(确定性,靶场两目标即前两档):
1. `alias` 非空、纯 ASCII、长度 ≥3 → 用 alias(wxid_m90epbt5ojml22 → `jiangliushi666`);
2. elif `username` 纯 ASCII 且不以 `wxid_` 开头(filehelper、gh_ 公众号)→ 用 username
   (filehelper → `filehelper`);
3. else(有 alias 之外的 ASCII username 不可用、display_name 非 ASCII)→ 若 username 以
   `wxid_` 开头(ASCII)→ 用 username(微信搜索支持 wxid 命中;行匹配反正用
   display_name,搜索词只负责把目标带进结果面板);
4. else → 用 display_name(全 emoji 名走 §D-3 特殊路)。

`row_match_terms = [display_name, search_term, alias or "", username]`(去重去空;顺序即
优先级)。**r2 实证(§J-27)**:搜索结果行副文本「微信号:jiangliushi666」在场且
可 OCR——alias 项兜底从假设升级为实证,jl666 类 ASCII-alias 目标的降级链主路 =
副文本 text_match(unique-row 依赖下降)。

### B-2 AX 主链原语(axui)

元素事实源:REV「chat_input_field AXValue 写入/回读 + activate+回车(36)」与元素名
`current_chat_name_label` / `session_item_<名字>`(prd 三源表;/tmp/ax_chat_test 实测)。
靶场实证 AX 门现在开着(122 节点可读)。**元素可达性与 AXPress 聚焦行为未经桥内复验
——P9 预验先行(§J 条 12),不可达即降级,零阻塞**(§D-1)。

```python
def probe_wechat_ax() -> bool        # 双判据:wechat_ax_node_count()(全窗最大)> 5
                                     # AND read_input_value() is not None(输入区能力);
                                     # label 不进门(无会话打开态不误判,§J-13)
def write_search_value(term: str) -> bool   # Cmd+F 后 System Events:
                                     # set value of attribute "AXValue" of focused element
                                     # (REF:27-28 同款,零剪贴板)
def press_session_item(name: str) -> bool   # 轮询找 name 含 <display_name> 的
                                     # session_item_* 元素并 AXPress(零坐标点击)
def read_current_chat_name() -> str | None  # current_chat_name_label 直读(emoji 精确;
                                     # 缺位 → None,不拦通道——标题走 OCR 兜底)
def read_input_value() -> str | None        # chat_input_field AXValue 直读(精确全量)
def write_input_value(text: str) -> bool    # chat_input_field AXValue 直写(REV 实弹配方)
def focus_input() -> bool                   # chat_input_field AXPress(聚焦;行为未实证,
                                            # P9 预验项,§I-7)+ 复读 value 断言正文未丢
def focused_is_input() -> bool | None       # osascript 读 AXFocusedUIElement 是否输入区
                                            # (尽力;取不到 → None 如实)
```

全部经模块级 `_run`(osascript 子进程,SUBPROC_TIMEOUT_S=10 挂起 → exit 30,抄
sendui.py:177-193);`_run`/`monotonic`/`sleep` 是注入点(单测全 mock)。

#### B-2-r2 元素查找底座与取值规范化(第三轮真机修正,§J-23/24)

r2 实证的三条硬事实驱动本节(证据见档首「第三轮真机证据」):

1. **BFS 底座遍历全部 windows,不绑 `window 1`**(§J-23):搜索态下搜索浮窗是
   window 1、主窗退 window 3(System Events 枚举实证)——绑 z-order 首窗的元素查找
   在搜索态必然搜错窗 → probe 判据失败 → 恒降级。修正原语:

```python
def find_element_by_identifier(identifier: str, *,
                               value_contains: str | None = None,
                               timeout_s: float = 2.0) -> osascript 元素引用 | None:
    """遍历 process "WeChat" 的**全部 windows**,每窗内 BFS 按 AXIdentifier 匹配
    (可加 value_contains 复筛);返回首个命中(元素引用带窗信息)。osascript 单
    脚本内完成「枚举 windows → 逐窗 BFS」(repeat with w in windows),不在 Python
    侧逐窗 spawn。chat_input_field 在主窗、session_item_* 在搜索浮窗——全窗遍历
    对两者都成立,不依赖 window 顺序。超时/异常/无命中 → None。"""
```

2. **匹配属性 = AXIdentifier**(§J-24):真机全树实证具名元素
   (current_chat_name_label/chat_input_field/session_item_*/tabbar_*)的名称都在
   AXIdentifier,AXDescription 基本为空(仅 tabbar 有内容)——**AXDescription 不用于
   匹配**(r2 实现按 AXDescription 匹配导致全链 miss,教训入档)。
3. **取值规范化:AppleScript 的 `missing value` 字面量 → None**(§J-24):no-match
   时 osascript 返回字面串 `"missing value"`,read_* 系列一律把它与空串规范化为
   `None`(r2 实现把 `'missing value'` 当真值泄漏给上层判据,哨兵污染,修正)。
   `read_current_chat_name()` 缺位 → None 的既有契约由此才真正成立。

### B-3 分区过滤选行(navfilter,降级通道)与坐标换算链

REF 的内嵌 python(REF:43-101)抽出为纯函数 + 三处增强:①分区头集合补「功能分类」
等垃圾分区头;②unique-row 兜底(emoji 行 OCR 名乱/不匹配时);③**三段坐标换算链**
(OcrLine 坐标是**裁剪图**归一化 0-1,pixel.py:152-153——`_ocr_region_lines` 按框裁剪
后 OCR,行坐标必须先 pane→window 再 window→screen,直接当全窗用会系统性偏左上,
§J-3)。

```python
#: 本地结果分区头(REF:53 六项 + 朋友圈动态 + ★r2 实证的「最常使用」默认区)
LOCAL_HEADERS = frozenset({"最常使用", "群聊", "联系人", "聊天记录", "公众号", "服务号", "小程序", "朋友圈"})
#: 非本地/功能分类分区头(其下候选一律排除;★补 REF 缺的「功能分类」族)
JUNK_HEADERS = frozenset({"搜一搜", "功能", "功能分类", "文章", "智能工具", "朋友圈动态",
                          "表情", "视频号", "直播", "新闻", "购物", "小程序码"})
#: 搜索结果面板 OCR 区——**搜索浮窗内归一化**(r2 实证 4.1.15 搜索结果渲染在独立
#: 浮窗,不在主窗;§J-25):box 坐标相对浮窗内容,全浮窗宽、中部带;P9' 预验校准。
SEARCH_PANE_BOX = (0.0, 0.10, 1.0, 0.88)

@dataclass(frozen=True)
class RowPick:
    cx: float          # 行中心点击点(**SEARCH_PANE_BOX 裁剪图坐标系**,§J-3)
    cy: float
    rule: str          # "text_match" | "unique_row"
    term: str          # 命中的匹配词(unique_row = "")

def compact(text: str) -> str: ...          # 去全部空白+casefold(_squash 同语义再折叠)

def select_result_row(lines: list[OcrLine], terms: list[str]) -> RowPick | None:
    """分区过滤 + 评分选行(零平台调用;REF 算法 + 增强项)。

    **坐标契约:lines 的 x/y/w/h 一律为 SEARCH_PANE_BOX 裁剪图内归一化 0-1**
    (与 pixel.vision_ocr 的输出坐标系一致,pixel.py:152-153);返回的 RowPick 同系。
    **承载窗 = 搜索浮窗**(§J-25,r2 实证):OCR 的截窗对象是浮窗 WindowInfo,
    row_box_to_screen 的 window 参数 = 浮窗(浮窗自带 bounds x/y/w/h)——三段换算
    链几何不变,承载窗换浮窗。

    1. 分区头定位:
       y_local = max(y | compact(行文) ∈ LOCAL_HEADERS)(REF:58-59 最下本地头)
       y_junk  = min(y | compact(行文) ∈ JUNK_HEADERS)   ← ★补的排除锚
       limit   = y_junk if y_junk 在场 else y_local else None
    2. 候选 = **有文本**(OcrLine.text 去空白非空;OCR 吐出的行哪怕乱码也算——unique-row
       的可达前提,§J-9)、非分区头、y < limit - 0.003 的行(REF:83 的 -0.003 容差);
       limit is None(分区头全没 OCR 出来)→ 候选 = 全部非分区头有文本行。
    3. 文本评分:对每候选取最优 (term_rank, score),score: 全等=0 / 前缀=1 / 包含=2
       (REF:69-74);terms 按序即 rank。
    4. 并列取 y 最大、再 x 最小(sorted key=(score_tuple, -y, x) 取首,REF:80-97 同款)。
    5. ★unique_row 兜底:**无任何文本命中 且 候选恰 1 行 且 limit 在场** → 采纳该行,
       rule="unique_row"。语义边界如实(§J-9):兜底救的是「行在(OCR 吐出了该行
       的文本,哪怕乱码/与 terms 全不匹配)但名读不出」——emoji 名行被 OCR 读成乱码
       字符时可达;OCR **零文本行**(行完全没读出,候选 0)→ 返回 None 拒发,不猜。
    6. 无命中 → None(调用方 exit 15 拒,绝不盲回车)。
    """
    # 点击点 = 行文本本体中心:cx = line.x + line.w/2(避头像),cy = line.y + line.h/2

def pane_to_window(pane_box: tuple[float, float, float, float],
                   cx: float, cy: float) -> tuple[float, float]:
    """裁剪系 → 全窗归一化(第二段换算):wx = pane_box[0] + cx * pane_box[2],
    wy = pane_box[1] + cy * pane_box[3]。"""

def row_box_to_screen(window: WindowInfo, wx: float, wy: float) -> tuple[int, int]:
    """全窗归一化 → 屏幕绝对像素(第三段):round(window.x + wx * window.width),
    round(window.y + wy * window.height)(依赖 WindowInfo 新 x/y 字段,§A)。"""
```

### B-4 CGEvent 点击与事件源(sendui,降级通道)

WZ click 配方(WZ:33-41)落地 ctypes:

```python
#: kCGEventSourceStateCombinedSessionState(事件源隔离,★hardened:现状 source=None)
EVENT_SOURCE_COMBINED = 0
def _event_source() -> int: ...    # CGEventSourceCreate(EVENT_SOURCE_COMBINED) 模块级缓存;
                                   # c_void_p 句柄;失败回退 None 源并在 docstring 如实(不拦发送)
def click_at(x: int, y: int) -> None:
    """mouseMoved(60ms)→leftMouseDown(35ms)→leftMouseUp;事件带 source;
    post 到 kCGHIDEventTap(HID_EVENT_TAP 不变,sendui.py:101)。"""
```

`post_key` 同步改造:两事件(keyboardEventSource=src)均用 `_event_source()` 句柄
(WZ:25-31 配方;CGEventCreateKeyboardEvent 签名已就位 sendui.py:126-130,只换第一参)。

**点击范围收窄(红线纪律,写进模块 docstring)**:仅 ①搜索结果行(导航)、
②composer 聚焦点(降级链哨兵/清空/发送前聚焦,COMPOSER_POINT_NORM=(0.50, 0.83),
INPUT_STRIP_BOX 中心;P9 预验校准)、③无。不点发送按钮(发送=回车)、不点任何其他 UI。

### B-5 导航序列(sendui._navigate,替换 sendui.py:398-413;r2 修正版)

**双窗模型(§J-25,r2 实证)**:搜索态下微信有两个相关窗——主窗
(chat_input_field/current_chat_name_label 所在)与**搜索浮窗**(搜索结果渲染处,
wid 每次搜索新生成)。AX 主链经全窗遍历 BFS 自动覆盖两窗(§B-2-r2);降级链需显式
找浮窗:

```python
#: 搜索前快照 CGWindowList 属主窗 id 集合;Cmd+F+粘词后 diff 出**新出现**的
#: 微信属主窗 = 搜索浮窗 → WindowInfo(含 bounds x/y/w/h,坐标换算第三段用)。
def find_search_popup(before_ids: set[int]) -> WindowInfo | None:
    """浮窗判据 = 属主 ∈ {微信, WeChat} 且 window_id ∉ before_ids(搜索态新增);
    diff 不到(版本漂移无浮窗)→ None,降级链导航按零候选拒发如实(不回退主窗
    区域——r2 已证主窗无搜索内容)。"""
```

```
ax 通道:
  post_key(KEY_F, CMD) → sleep(SEARCH_SETTLE_S)
  axui.write_search_value(search_term)           # 零剪贴板
  轮询(SEARCH_RENDER_TIMEOUT_S=5s/0.5s):axui.press_session_item(display_name)
    ——press 底座 = find_element_by_identifier("session_item_…" 前缀匹配,全窗遍历,
    浮窗内命中;§J-23/25)成功即返回(press 内部找到并按下)
cgevent_ocr 通道:
  before_ids = 快照窗集合(CGWindowList,属主微信/WeChat)
  set_clipboard_text(search_term) → sleep(CLIPBOARD_SETTLE_S)
  post_key(KEY_F, CMD) → sleep(SEARCH_SETTLE_S)
  post_key(KEY_V, CMD) → sleep(SEARCH_RENDER_S=1.2s)
  轮询(SEARCH_RENDER_TIMEOUT_S=5s/0.6s):
    popup = find_search_popup(before_ids);None → 记 stage 失败详情,继续轮询至超时
    lines = _ocr_region_lines(popup, SEARCH_PANE_BOX, workdir, "search")  # ★截浮窗
    pick = navfilter.select_result_row(lines, row_match_terms)
    pick 非 None → click_at(*row_box_to_screen(popup,
      *navfilter.pane_to_window(SEARCH_PANE_BOX, pick.cx, pick.cy)))
      → sleep(CLICK_SETTLE_S=0.3) → 返回 pick
两通道随后都过标题双验证(§1 步骤 e,主窗坐标系不变);
**失败清理(§J-26,★r2 缺陷 D:导航失败不得留残局)**:任一环节超时/零候选 →
先 `_dismiss_search()`(post_key(KEY_ESCAPE)——关浮窗+清搜索态;ESC 后若词残留
搜索框由下次 Cmd+F 预填无害,r2 后复验)→ 再 stage_fail("navigate")→ exit 15
整尝试重试;盲回车键序(↓+Return)已删除,KEY_RETURN 全链唯一出现点=§1 步骤 j2。
dry-run 成功收尾与 armed 前其它失败路径同用 `_dismiss_search()` 清场(armed 后
不引入新交互)。
```

---

## 4. §C 验证五件套落法、G6 合成与异常隔离(问 3)

### C-1 五件套 → 落点对照

| # | 件(WZ 出处) | 落点 | 形态 |
|---|---|---|---|
| 1 | 标题校验(WZ:160-178) | 已在(sendui.py:408-413)+ 升级 | AX label 直读优先(axui.read_current_chat_name;缺位走 OCR 不拦通道),OCR 标题带(TITLE_BAND_BOX)兜底;emoji 处置见 §D-3 |
| 2 | composer 哨兵探测(WZ:190-197) | sendui.`read_composer_via_clipboard` ★新 | 见 C-2;**兼降级链聚焦断言**(§D-2/§J-17) |
| 3 | 发送后清空轮询(WZ:271-277) | sendui.`_wait_composer_cleared` ★新 | 12×80ms(WZ 同参数);AX 通道用 axui.read_input_value 直读(零点击),降级链每轮哨兵读 |
| 4 | SHA256 防重 120s + uncertain-never-retry(WZ:143-158/237-247) | send_state 扩展 ★新(多槽) | 见 C-3/C-4 |
| 5 | 旧剪贴板保存恢复(WZ:220-221) | 已在(sendui.py:507/536-543) | 保持;哨兵/搜索词对剪贴板的全部中间覆写都在 try 块内,finally 必复原 |

### C-2 哨兵探测协议(sendui.read_composer_via_clipboard)

WZ:190-197 原样移植(只读协议:Cmd+A 全选 + Cmd+C 复制不改输入框内容):

```python
def read_composer_via_clipboard(window: WindowInfo) -> str | None:
    """降级链读输入框内容;返回 None = 输入框空。
    click_at(composer 点) → sleep(0.06)
    post_key(KEY_A, CMD) → sleep(0.03)
    sentinel = f"__MYIA_PROBE_{uuid4().hex[:8]}__"
    set_clipboard_text(sentinel) → sleep(0.04)
    post_key(KEY_C, CMD) → sleep(0.06)        # KEY_C = 0x08(WZ:194 同键码)
    got = clipboard_text()
    return None if got == sentinel else got    # 哨兵未被动 = 输入框空(WZ:196 语义)
    # 哨兵读会把哨兵留在剪贴板 → finally 复原兜底;异常向上抛(exit 15/30 族;
    # 仅 §1 步骤 a-i 与 j0 可抛,armed 后 §C-5 隔离)
```

发送前空断言(§1 步骤 f):值非空 → Cmd+A+Delete 清(现 sendui.py:416-419 升级为
清后再探)→ 仍非空 → stage_fail("composer_not_empty")(WZ:250-252 同语义)。
**注意**:哨兵读发生在「正文粘贴之前」,与粘后回读互不污染(顺序:空断言→粘正文→回读)。

### C-3 状态文件形状与 G6 合成(send_state.py 扩展)

`send_state.json` 升级为两键(**向后兼容**:旧文件只有 last_send_epoch,缺
send_fingerprints 键 = 无指纹态,`_read_unlocked` 不变,新增指纹读写原语):

```json
{
  "last_send_epoch": 1730000000.0,
  "send_fingerprints": {
    "<sha256hex>": {"status": "pending|sent", "ts": 1730000000.5}
  }
}
```

**多槽指纹档(§J-10:单槽会被并发异指纹覆盖,uncertain 保护失效)**:
`send_fingerprints` 是 dict(键=指纹,值={status,ts});写入时顺手**清扫**:删过期
(ts 距 now > DEDUP_WINDOW_SECONDS)条目 + 容量上限 8 条(超限按 ts 淘汰最旧)。
A 的 pending 档不会被 B 的异指纹发送挤掉——120s 窗内 A 的同指纹重发仍被拒。

**既有写路径的指纹保全(§J-16,硬指令,缺失即实洞)**:
`_write_unlocked`(send_state.py:125-134 现状写死整份 `{"last_send_epoch": …}`,
任何一次占位/还原都会**整抹** send_fingerprints——B 异指纹失败 rollback 即抹 A 的
pending)。**改造为读-改-写**:临界区内先读现文件,保留 `send_fingerprints` 键原样,
只更新 `last_send_epoch` 再原子落盘(tmp+os.replace 不变)。这是私有函数的内部实现
升级,公共原语(reserve_send/record_send)外部可观测行为不变——既有断言零改依然
成立。`rollback_reserve` 同步增分支(公共行为在「无指纹档」场景与旧完全一致,
test_send_state.py:120-128 断言零改;**有指纹档**时:previous=None 的还原不再
unlink 整文件,改为移除 `last_send_epoch` 键、保留指纹档——unlink 会把 A 的
pending 一起删掉)。

**原语(既有公共行为零改动 + 新增)**:

```python
DEDUP_WINDOW_SECONDS = 120.0   # 模块常量硬编码(G6 同风格:无配置键)
FINGERPRINT_CAPACITY = 8       # 多槽容量上限(清扫用)

@dataclass(frozen=True)
class ReserveOutcome:
    previous: float | None          # 占位前时间戳(rollback 用;dedup 命中时未占位=None)
    dedup: str | None               # None=正常占位 | "sent_recently"=指纹命中且已发(幂等,未占位)

def reserve_send_dedup(self, now: float, fingerprint: str) -> ReserveOutcome:
    """发送路径专用:同一 flock 临界区内三步,**指纹门在前、间隔门在后**
    (幂等命中不占位不该被间隔拦;立即重复同指纹 → 幂等而非 exit 14,§J-5):
    1) 指纹门(只读,不预落):档内 fingerprint 命中且 now-ts < DEDUP_WINDOW:
       status=sent   → 返回 ReserveOutcome(None, "sent_recently")(未占位)
       status=pending → BridgeError(17,"上次同指纹发送状态不确定(pending)…绝不自动
                        重试",fix_hint=等 120s 或换正文;人工确认后再操作)
    2) 间隔门:previous 在且 now-previous < 10s → exit 14(判据不变)
    3) 占位:写 last_send_epoch=now(经读-改-写保指纹键);顺手清扫指纹档;
       指纹条目不写(只在 on_armed 落 pending)
    既有 reserve_send(now)->float|None 保留原样公共行为(诊断/兼容;docstring 注明
    发送路径走本原语)。
    """

def mark_fingerprint_pending(self, key: str, now: float) -> None:  # on_armed 调(回车 down 前)
    """写 dict[key]={pending, now}(只动自己的 key,不覆盖他档)+ 清扫。"""
def mark_fingerprint_sent(self, key: str, now: float) -> None:     # 回执全绿调
    """仅当档内 key 相同才 pending→sent 升级(不同=他进程的后发占了自己档,不覆盖,
    该次发送的防重窗以 pending 态继续有效——保守方向)。"""
```

**rollback 纪律(与防重的边界,写进 docstring)**:`rollback_reserve` 只动
`last_send_epoch`(且保指纹档,§J-16);未发出路径(on_armed 之前)才可能被调用;
on_armed 之后 sendui 恒不抛(§C-5),rollback 天然不触发。

并发封闭推演:进程 A on_armed 后 pending;进程 B 同指纹 reserve_send_dedup → 指纹门
见 pending → exit 17 拒;进程 B 异指纹 → 间隔门(≥10s)拦或放行(不同内容不同目标,
合法;A 的 pending 档因多槽+写路径保全而不受影响)。两门同一临界区,无 TOCTOU 缝。

### C-4 uncertain-never-retry 状态机(全链汇总;pending 时点=on_armed,回车 down 前)

| 时点 | 时间戳占位 | 指纹档 | 可重试? |
|---|---|---|---|
| reserve_send_dedup 过 | 落 now | 无 | 后续失败 rollback 还原时间戳,可重试 |
| **本尝试** on_armed 之前的失败(导航/空断言/回读/on_armed 自身失败=fail-closed,§C-5)重试耗尽 | rollback 还原 | 无 | ✓(≤3 次自动重试不变) |
| **on_armed 调用点**(回读确认后、回车 down 前) | 保留 | **pending** | ✗ 同指纹 120s 内 exit 17 |
| on_armed 后聚焦断言失败(未回车,§1-j1) | 保留(不 rollback) | pending | ✗ 同上(已知代价,§I-8) |
| **跨尝试残留(§J-22 补行,如实)**:尝试 N armed 后失败 → 尝试 N+1 在自身 on_armed 前失败上抛 → CLI rollback 时间戳——但尝试 N 的 pending **已落且不随 rollback 还原** → 同指纹重发 exit 17(保守:armed 过即视同 uncertain,与「本尝试未 armed 失败可重试」不矛盾——前者指纹在档) | 已还原 | **pending(N 落的)** | ✗ exit 17 |
| 回车后验证全绿(清空轮询+回执) | 保留 | **sent** | 同指纹 120s 内 → 幂等 exit 0 |
| 回车后任一验证不确定(轮询超时/回执未见/链挂) | 保留 | **pending** | ✗ exit 17;载荷如实(§E-3) |
| on_armed 与回车之间硬崩溃(进程死) | 保留(文件已落) | pending(文件已落) | ✗ 重启后同指纹 120s 内 exit 17(§J-10:回车后才落 pending 的崩溃窗口已闭合) |

**设计取舍(写明)**:pending 提前到回车前意味着「回车事件被系统丢弃(未发出)」的
尝试也会被锁 120s——宁可误锁,不开「已发出却无指纹」的双发窗(WZ:270-271 同序)。

### C-5 on_armed 的异常隔离(§J-14 定稿:fail-closed 门 + armed 后吞异常)

sendui.send_text 内部结构(骨架与文字以此为准,测试照此写):

```python
# 步骤 a-i(on_armed 之前):正常抛 BridgeError(exit 15/30 族)→ CLI 层
# except BridgeError → rollback_reserve(未发出,还原占位,可重试)——既有语义。
# j0 on_armed 是「进入发送段的门」,其失败 = fail-closed:
try:
    on_armed()                      # 落 pending;失败(OSError 等)→ 上抛
except Exception:
    raise  # armed 仍 False → CLI rollback → 未回车,可安全重试。
           # 指纹没落就绝不进入发送段——宁可不发,不开「无指纹却发出」双发窗(§J-14)。
armed = True
# —— 以下(armed=True)对外恒不抛 ——
try:
    ...聚焦断言(失败→计入重试/终败 exit 15 error,不上抛,§1-j1)...
    post_key(KEY_RETURN)              # j2 唯一发送
    ...清空轮询/回执(含 on_receipt_green、receipt_query 的调用)...
except Exception as exc:              # noqa: BLE001 —— armed 后兜底吞异常
    # 绝不上抛:此时已回车(或已 armed),上抛会诱发 CLI rollback → 放开 10s 内
    # 第二发(G6 双发红线,sendui.py:19-22 明文设防的场景)
    verdict = {"post_send_verified": False,
               "post_send_note": f"发出后内部异常({type(exc).__name__}),结果不确定"}
finally:
    ...剪贴板复原/工作目录清理(不变)...
```

边界语义(替代第一轮正文「on_armed 调用本身也在隔离段内」的错误表述,§J-14):
**on_armed 失败=fail-closed 上抛**(指纹未落→不发送→可重试);**armed 之后的**
on_receipt_green / receipt_query 失败=吞掉+`fingerprint_note`/`post_send_note` 如实
(指纹已 pending,防重保护在位,只是升级 sent 失败——如实披露)。on_armed 落盘的
原子性:mark_fingerprint_pending 走 tmp+os.replace,失败=未写或已写——已写后仍抛的
窗口下,重试路径会发现指纹已 pending → exit 17(保守方向,可接受,docstring 注明)。

### C-6 localdb 回执判定(receipt_query 注入;§J-6/8/18/19)

CLI 层构造闭包(sendui 零 localdb 依赖,§A 依赖图;**storage/keys 复用步骤 2 的
单次解析**,§J-19):

```python
# cli.py send_text 分支内(步骤 2 已解析 storage/keys,此处零重复解析):
def receipt_query(username: str, body: str, since_epoch: float) -> bool | None:
    """回执判定:query_history(username, since 1d) 的 messages 中存在
    (text 空白不敏感对账命中 body) AND (int(ts) > since_epoch - 2)。
    ts 已由 localdb_query._normalize_ts 归一为秒(localdb_query.py:192-200),
    since_epoch 为 epoch 秒;容差 2s 吸收时钟/落库延迟。
    localdb 链 BridgeError → None(如实,不算失败也不算成功)。"""
```

sendui 在 on_armed 时刻取 `since_epoch = wall_clock()`(新模块级注入点
`wall_clock: Callable[[], float] = time.time`,单测换假钟);k-2 段以
`receipt_query(target.username, body, since_epoch)` 轮询。**轮询预算(§J-18 定稿)**:
退避表 `RECEIPT_POLL_SCHEDULE = (5.0, 10.0, 15.0)`(首次调用后依次等 5/10/15s 再试,
累计 ~30s 窗 ≤4 次调用)——保守覆盖「微信写库延迟 + E2 副本 mtime 触发 sqlcipher
重建」的冷路径;热路径(副本新鲜)毫秒级返回。预算依据如实:冷重建耗时无零发实测
数据(不动微信文件 mtime 的前提下不可测),故取保守 30s;P9 预验⑥测热路径计时,
P10 真发的 localdb_receipt 若超窗 → 载荷如实 false + P10.6 人工双查补证(AC4 以
人工补证后判过,不假绿)。**判据防假绿**(§J-8):必须
`ts > since_epoch - 2`,否则当天同正文历史消息(「嘻嘻」类高频词)假绿。

---

## 5. §D 通道分层、切换判据与 emoji 处置(问 4)

### D-1 切换判据(§J-4/13/22:双判据 + 跨尝试降级 + 全窗节点数)

- **判定原语**:`axui.probe_wechat_ax()` = **(a)** `system_checks.wechat_ax_node_count()
  > 5`(AX 门开;REV「P3/P4」判据,靶场实证门开时 122 节点,r2 正常态 76~123 亦证
  判据工作;**该计数取全部窗口的最大 UI elements 数,不绑 `window 1`**——r2 实证
  搜索态浮窗是 window 1(4 顶元素)而主窗在 window 3,绑死会把门开误判成 closed,
  doctor-after-p3-inproc.json 实读 nodes=4 即此形态,§J-22/23) **AND (b)**
  `axui.read_input_value() is not None`(chat_input_field 能力面——主链依赖写/读
  输入区,光 label 可读不够;本仓自证 sendui.py:247-249:AX 门关时输入区零暴露,
  「label 可读、输入区不可写」的半开态按此判据直接走降级链)。read_input_value
  底座 = 全窗遍历 BFS(§B-2-r2)——r2 实证绑 window 1 时搜索态恒 miss → 恒降级,
  修正后判据才真可达。
  **label 不进门**(§J-13):「门开但当前无会话打开(label 缺位)」不误判——
  label 是读路增强,缺位时标题验证走 OCR 兜底。
  probe 即一次无障碍查询,副作用 = QNSView activateQtAccessibility 自然置位
  (REV:20-24,微信自身行为,非前台扰动)——docstring 如实注记。
- **判定时机与降级规则**:每次尝试(`_attempt_send`)开头判定一次,单尝试内通道
  固定(**中途不换道**:半 AX 半 CGEvent 混合态无法归因);**跨尝试允许降级**——
  本尝试失败且失败原语为 AX 能力缺失(write_search_value/press_session_item/
  write_input_value/focus_input 返回 False)→ 下一尝试 `forced_fallback=True` 直接
  cgevent_ocr,不再 probe。「label 可读、输入区不可写」形态:尝试 1 ax 失败 →
  尝试 2/3 降级链,**降级通道在该形态下可达,AC3 成立**(§J-4)。
- **AX 门失效处置**:doctor 报 ax_gate=closed + fix_hint 给 REV LLDB 配方(P1 定位
  自检 vptr == $S+0x9fe7e68 / P2 走函数 FUN_06c4ad50($qca,1) 写门 / P4 节点数复验);
  桥**不自动 attach**。门关不拦 send_text(自动走降级链),只在载荷 channel 如实。

### D-2 两通道职责对照(含发送前聚焦行;§J-1/17:两通道都是断言)

| 环节 | AX 主链 | CGEvent+OCR 降级链 |
|---|---|---|
| 搜索词写入 | AXValue 直写(REF:27-28) | 剪贴板+Cmd+V |
| 结果选择 | session_item_<名字> AXPress(零坐标) | 分区过滤 OCR + click_at |
| 标题验证 | current_chat_name_label 直读(精确;缺位走 OCR) | OCR 标题带 / 间接证据(§D-3) |
| 输入框读 | chat_input_field AXValue(精确全量) | 哨兵探测 / OCR 输入带 |
| 正文写入 | chat_input_field AXValue 直写 | pbcopy+Cmd+V |
| **发送前聚焦断言** | **focus_input()(AXPress)→ 复读 value==body → focused_is_input 尽力断言(取 None 如实降为前两条)** | **click_at(COMPOSER_POINT) → 哨兵读一致性断言:read_composer 回 None(空)或 ==body 才算聚焦成立;回异值(焦点落别处,Cmd+C 复制了别处内容)= focus 失败——哨兵协议本身即聚焦断言,与 AX 路对称,不是裸点击(§J-17)** |
| 发送 | 回车(post_key KEY_RETURN,同一原语) | 同左 |

聚焦断言失败 → §C-5 结构内处理(armed 后不上抛:计入重试;耗尽 → **exit 15 error
载荷**,§J-20)。**0.7.0 从未真机发送过**(README.md:55-56「真机冒烟=下一阶段」),
回车落点此前从未被验证——聚焦断言把这一盲点变成显式检查。**聚焦真伪的验证边界
如实(§J-17)**:dry-run 不回车,验不了「回车那一刻焦点在哪」的终局真伪;P9 预验
④验的是「点位聚焦有效性」(降级链 dry-run 中哨兵空断言/一致性断言通过=点击确实把
焦点带到了 composer;AX 路 focus_input 后 focused_is_input=True 为直证、None 如实),
终局以 P10.2 首次真发的 composer_cleared=true 为准——10.2 前置门槛:聚焦证据链完整
(dry-run 一致性断言过 + AX 直证或哨兵间接证),不完整先修再发,防 uncertain 烧
白名单额度。

### D-3 emoji display_name(🐳)处置方案

**AX 主链(首选,天然解决)**:`session_item_🐳` 元素名与 `current_chat_name_label`
文本都是 AX 层字符串,emoji 精确直读零 OCR——jiangliushi666/🐳 目标优先走 AX 主链,
标题验证 `ax_label` 路精确核 🐳。

**降级链(AX 不可达时)的如实可达性(§J-9/25 修订)**:
1. **导航级**:search_term=alias(ASCII)进搜索框;结果行文本是 🐳。可达路径按
   **浮窗内** OCR 实况二分(r2 已证主窗无搜索内容,盯主窗必零候选;浮窗修正后):
   - OCR 吐出了该行的**某种文本**(乱码字符/或副文本「微信号:jiangliushi666」——
     **r2 实证该副文本在场且可 OCR**,alias 项命中即 text_match,jiangliushi666
     类目标的主路是副文本 text_match 而非 unique-row)→ 分区过滤后若无 term 命中
     但候选恰 1 行 → unique-row 采纳(§B-3 步 5;兜底救「行在但名读不出」,
     不救「行完全没读出」);
   - 浮窗 OCR **零文本行**(行完全没被读出,候选 0)→ select_result_row 返回
     None → **exit 15 拒发(设计内行为,不是故障)**,message 注明「emoji 目标在
     降级链不可定位;先修 AX 门(doctor 看配方)后以 AX 主链发送」。
2. **标题核验级**:OCR 标题带读不出 🐳 → 间接证据链放行(前提:导航级已成立):
   (a)unique-row/text_match 采纳记录在案 +(b)点击后标题带 OCR ≠ baseline_title
   (导航前基线,§1 步骤 c;会话已切换)+(c)发送后清空轮询通过 +(d)localdb 回执
   终验见到正文落库。载荷 `title_verify: "indirect"` 如实标注。
3. **回执终验级**:receipt_query 按 username(wxid)查(§C-6)——**回执链不受 emoji
   影响**(DB 侧 wxid 是 ASCII),红线 4「回执以 localdb 落库为准」在 emoji 场景最硬。
4. 间接证据 (a)~(c) 任一不成立 → exit 15 拒发,如实 message 同上。

**如实边界**:emoji 目标的降级链可达性取决于 OCR 当次实况(P9 预验对 🐳 目标
dry-run 实测留痕);不可达即拒发,不猜不盲点。

---

## 6. §E CLI 契约(问 5)

### E-1 send_text(子命令名与位置参数不变)

```
wechat-bridge send_text <id> --file - [--dry-run] [--json] [--config PATH]
```

- `--dry-run`(store_true,缺省 False):全链走到「正文已粘贴 + 回读确认」,**不回车
  不 on_armed**;随后 Cmd+A+Delete 清草稿(降级链若处搜索态再 Esc,KEY_ESCAPE=0x35);
  跳过 reserve_send_dedup(不占时间戳、不查防重、不落指纹——零发送动作零频控副作用,
  可无限重跑)。载荷:
  `{"send": {"chat", "target": {...}, "channel", "sent": false, "dry_run": true,
  "navigated": true, "pasted": true, "readback", "title_verify", "nav_debug": {...},
  "attempts", "elapsed_ms"}}`。`nav_debug` 仅 dry-run 载(坐标与规则名,零内容,
  P9 预验校准依据):`{"pick_rule", "pick_cx", "pick_cy", "terms_hit"}`(裁剪系)。
- argv 红线不变:正文只走 stdin(cli.py:19-21)。

### E-2 doctor(新顶层子命令)

```
wechat-bridge doctor [--json] [--config PATH]
```

= `--probe` 超集 + send 链就绪度,**仍零前台扰动**(AX 读查询不激活不点击):

```json
{"doctor": {
  "probe": {<run_probe 载荷原样>},
  "ax_gate": {"nodes": 122, "state": "open|closed|unknown",
              "input_field": "ok|missing",
              "note": null|"进程外枚举 5 节点级 = Qt AX 门未开(REV 判据);nodes 为全窗最大 UI elements 数",
              "fix_hint": null|"AX 门重开配方(LLDB,人工执行):P1 vptr 自检 == slide+0x9fe7e68 → P2 FUN_06c4ad50($qca,1) 写门 → P4 复验节点数>5;完整配方 research/FINDINGS.md"},
  "cgevent_channel": {"post_key": "ok|unverified", "note": "辅助功能授权为发送前置,doctor 不合成事件,以首次 dry-run 实测为准"}
}}
```

- `ax_gate.nodes` = `system_checks.wechat_ax_node_count()`(osascript 遍历微信进程
  **全部 windows 取最大** `count of UI elements`;>5 = open,≤5 = closed,失败 =
  unknown/None;§J-22);`input_field` = axui.read_input_value() 探测结果。均可注入。
- exit 0 恒返回(doctor 是状态查询,不判错——key-status 判例,cli.py:468-472)。

### E-3 send_text 成功/幂等/错误载荷(终态形状;§J-20:stage=focus 走 error)

```json
// 正常发送成功
{"send": {"chat": "<原样入参>", "target": {"username": "...", "display_name": "..."},
          "channel": "ax|cgevent_ocr", "sent": true, "attempts": 1,
          "readback": "ax_value|clipboard_copy|ocr_strip",
          "title_verify": "ax_label|ocr|indirect",
          "composer_cleared": true, "localdb_receipt": true,
          "post_send_verified": true, "post_send_note": null,
          "fingerprint_note": null, "deduped": false, "elapsed_ms": 42000}}
// 发出后不确定(回车已发生;恒不抛错,§C-5)
{"send": {..., "sent": true, "composer_cleared": false,
          "post_send_verified": false, "post_send_note": "...uncertain...", ...}}
// 聚焦断言终败(on_armed 后未回车)→ **exit 15 error 载荷**(不破 exit 0⇒sent:true
// 旧契约,消费方零迁移;message 注明 pending 已落)
{"error": {"code": "send_ax_focus_required", "message": "发送前聚焦断言未过(未回车;指纹已 pending,120s 内同指纹重发将 exit 17)", ...}}
// 防重幂等命中(指纹 sent,120s 内;含立即重复——指纹门先于间隔门)
{"send": {"chat": "...", "target": {...}, "sent": false, "deduped": true,
          "dedup_status": "sent_recently", "elapsed_ms": 30}}
// uncertain(指纹 pending 拒发)
{"error": {"code": "send_uncertain_dedup", "message": "上次同指纹发送状态不确定(pending,120s 窗内):绝不自动重试", "fix_hint": "等待窗口过期或更换正文;人工确认上次发送结果后再操作", ...}}
// 目标查无 / 多义
{"error": {"code": "send_target_not_found", "message": "DB 侧未解析到目标(chat_id=…,username/alias/展示名三路均无)", "fix_hint": "确认 id;用 localdb query 先验目标存在"}}
{"error": {"code": "send_target_ambiguous", "message": "命中多个联系人(chat_id=…)", "fix_hint": "改用 alias 或 username(wxid)消歧"}}
```

`readback` 枚举增 `"clipboard_copy"`(Cmd+A+Cmd+C 全量回读路);`title_verify` 枚举
如上;载荷永不载正文(红线 6 不变)。

### E-5 exit 0 语义与消费方迁移注记(§J-20)

旧契约「exit 0 ⇒ sent:true」在新版有两处扩展形态,均为 additive 且带显式分支键:
- `sent:false + deduped:true`(幂等命中:重复请求被成功去重,零新发);
- `sent:false + dry_run:true`(演练请求,零发送)。
**未升级的消费方把 exit 0 当 sent:true 会误判上述两形态**——迁移注记落点:P8 的
README 能力边界节 + MYIA 侧 push 层(weixin_local)升级提醒一句「按 deduped/dry_run
分支」;除此之外 exit 0 恒 sent:true(聚焦终败=exit 15 error,不在 exit 0 内)。

### E-4 错误码表增量(§6 封闭表修订)

| 码 | 名 | 语义 | 新/既有 |
|---|---|---|---|
| 0 | exit_ok | 成功(含 deduped 幂等/dry-run;见 §E-5 迁移注记) | 既有 |
| 14 | send_rate_limited | G6 间隔不足(可等后重试) | 既有 |
| **17** | **send_uncertain_dedup** | **指纹 pending 命中:上次发送状态不确定,绝不自动重试** | **新增** |
| 15 | send_ax_focus_required | 断言族(navigate/composer_not_empty/readback/locate/**focus 终败**;on_armed 前可自动重试) | 既有 |
| 1 | send_target_not_found / send_target_ambiguous | DB 侧目标解析失败/多义(exit 1 + 具名 code,像素层 screen_capture_failed 先例,codes.py:112 docstring 同款不进具名族) | 新增(code 不加码值) |
| 30 | timeout | 子进程挂起 | 既有 |

---

## 7. §F 红线内建对照(prd 红线逐条 → 落点)

| 红线 | 落点 |
|---|---|
| 1 白名单双发 | 代码不硬编码白名单(测试纪律);真机矩阵纪律在 implement.md P10(仅 filehelper/jiangliushi666,正文「嘻嘻」,≤2 真发,**防重/间隔矩阵全用零发或条件执行路径**,间隔 ≥10s 由 G6 强制) |
| 2 发送前 DB+标题双验证 | §1 步骤 3(resolve_target 三形态,exit 1 拒于任何 UI 扰动前)+ 步骤 e(AX label 主/OCR 兜底/indirect 如实) |
| 3 uncertain-never-retry | §C-4 状态机(pending=on_armed 时点;跨尝试残留行入表)+ §C-3 多槽+写路径保全 + exit 17 |
| 4 localdb 回执终验 | §C-6 receipt_query(时间戳判据防假绿;30s 退避预算;超窗→人工双查补证不假绿);post_send_verified 以 localdb 为准,清空轮询/OCR 为过程证据 |
| 5 grill 三关 | implement.md P11 |
| 6 剪贴板必恢复 | finally 复原不变(sendui.py:536-543);哨兵/搜索词覆写全在 try 内 |
| (导航零盲回车) | §B-5:↓+Return 键序删除;KEY_RETURN 唯一点=发送(j2);回车前聚焦断言(§D-2 两通道对称)保回车落点;无候选行 exit 15 拒 |

---

## 8. §G 测试计划(问 6 前半:全 mock 零真机)

命令:`uv run --no-sync python -m pytest tests/wechat-bridge -q`。基线 302 passed /
7 skipped(prd「现状」节)。**对账口径(§J-11/22-2 定稿)**:适配的既有用例**仍全绿
仍计入通过数**——对账式 = `通过数 = 302 + 新增数,全绿`;test_send_state.py 既有
用例零改(send_state 既有公共行为不变保证);test_bridge_cli.py 既有 send 用例
(④/④b 族,test_bridge_cli.py:73-113)需签名适配(桩换新签名 + 补 resolve_target
mock),逐条列名、行为断言不放松。

| 文件 | 用例(全 mock) |
|---|---|
| test_send_target.py(新) | 三形态解析:username 正查(filehelper)/alias 反查(jiangliushi666)/**展示名全量拉取+Python compact 比对**(「文件传输助手」「🐳」;大小写折叠用例);remark 优先序;查无 → None;**alias 反查多行 → send_target_ambiguous(不静默取首行)**;storage/keys 注入路径(不重复解析);localdb 链失败透传(20/21/22);pick_search_term 四档;fingerprint 稳定性(三入参同目标同 key) |
| test_navfilter.py(新) | 分区头过滤(junk 头/local 头/junk 优先);评分/并列取 y 最大;unique-row 三态(乱码单行采纳/零候选 None/候选≥2 不触发);分区头集合含「功能分类/搜一搜」;坐标换算链三段端到端(裁剪系 fixtures → pane_to_window → row_box_to_screen,WindowInfo x/y=100,200 断屏幕坐标,§J-3) |
| test_axui.py(新) | probe 双判据(门开+输入区可读才 True;门开无输入区 → False;label 缺位不影响);focus_input/focused_is_input 脚本形状;读写脚本 osascript argv 形状(mock _run);read None 路径;超时 → exit 30 |
| test_send_state.py(扩,既有零改) | 多槽指纹:sent 幂等(含 <10s 立即重复 → 幂等而非 14)/pending→17/过期放行/清扫;并发交错(A pending 后 B 异指纹 sent,A 重发仍拒);**写路径保全:B 占位后 rollback,A 的指纹档仍在(锁 §J-16 实洞)**;rollback 无指纹场景旧行为(删文件,既有断言即此)/有指纹场景移键保留指纹;pending→sent 升级;mark_sent 异 key 不覆盖;旧格式文件兼容 |
| test_send_ui.py(扩) | FakeHarness 扩 clicks/ax 读写/composer 态/clear 态/wall_clock:①AX 主链全绿;②降级链全绿(键序:无 KEY_DOWN_ARROW);③盲回车禁止(KEY_RETURN 仅发送点一次);④哨兵空断言链;⑤清空轮询超时 → uncertain(不抛错/指纹 pending);⑥dry-run(无回车无 on_armed/KEY_ESCAPE 在/载荷 nav_debug);⑦title_verify 三枚举;⑧emoji(乱码单行→unique-row→indirect;零候选 → exit 15);⑨CGEvent 源;⑩**on_armed fail-closed:抛 OSError → 上抛包装 exit 15 族、无回车、CLI rollback、指纹未落;armed 后 on_receipt_green 抛 → 吞掉+fingerprint_note 如实**(§J-14);⑪聚焦断言两通道(AX:focus_input False → exit 15 error+stage 注记+无回车;降级:composer 点击后哨兵读异值 → focus 失败,回 None/==body → 过,§J-17);⑫回执:since_epoch=on_armed 时刻;**RECEIPT_POLL_SCHEDULE=(5,10,15) 轮询形态**(假钟推进,§J-18) |
| test_bridge_cli.py(扩+适配) | 适配:既有 send 用例桩换新签名+resolve_target mock(逐条列名);新:--dry-run 契约(零频控副作用:dry-run 后立即可真发不被 14 拦);指纹幂等 exit 0(含立即重复);exit 17;not_found/ambiguous exit 1 code;**storage/keys 单次解析断言(monkeypatch 计数 resolve_keys 调用次数 ==1,§J-19)**;doctor 载荷(ax_gate 三态+input_field);receipt_query 闭包假绿反例(ts≤since-2 → False);**stage=focus 终败 → exit 15 error 载荷**(§J-20) |
| test_probe.py(扩) | run_doctor 复用 probe 全量 + ax_gate 注入(mock wechat_ax_node_count——**含多窗最大数语义断言**) |

Mock 纪律:平台原语(子进程/ctypes/时钟)全注入,CI 无微信全绿——桥既有
test_send_ui.py FakeHarness 模式(42-100)直接扩展。

---

## 9. §H 装机热修(问 6 后半)

装机活体 `~/.myia/plugins/wechat-bridge/`(bin 启动器 53 行 bash 通常不动;包从
`~/.myia/plugins/wechat-bridge/wechat_bridge/` 直加,勘察确认 cp 更新 mtime 击穿
`__pycache__`):

```bash
SRC=/Users/zhengbingjin/Project/Github/MYIA/plugins/wechat-bridge/wechat_bridge
DST=~/.myia/plugins/wechat-bridge/wechat_bridge
cp "$SRC"/{codes,send_state,sendtarget,navfilter,axui,sendui,ax,pixel,system_checks,probe}.py "$DST"/
# 改动面核对(逐文件 diff -q 应仅本任务改动);冒烟(零发送)见 implement.md P9
```

README.md 同步:红线 1 的 send_text 例外句补「+ 合成鼠标点击(仅导航行与 composer
聚焦,PRD 2026-10-14)」;§6 码表补 17;能力边界节补三源合体条目(含门序/多槽指纹/
聚焦断言/异常隔离要点 + **§E-5 消费方迁移注记**)。

---

## 10. §I 可翻案点(默认方案已选;翻案须改本档)

| # | 决策 | 默认 | 翻案备选 |
|---|---|---|---|
| 1 | **合成鼠标点击解禁**:README.md:65 现文「合成鼠标仍禁」与 PRD AC1「分区过滤选行→点击」冲突。默认按 **PRD(2026-10-14,晚于 README 0.7.0)为准 = 翻案成立**,点击范围收窄到 §B-4 三类,README 红线同步修订 | 点击导航 | 键盘导航(↓ 逐行+AX 焦点判行):4.1.15 AX 焦点不可靠且慢,不推荐;若主人不认翻案则 AC1 改键盘路,本档 §B-3/4 重写 |
| 2 | exit 17 新码族 | 新增(uncertain 需与 14「可等后重试」语义分开编程) | exit 14 + code 区分(不加码值;MYIA 侧需看 code 字符串分叉) |
| 3 | LLDB 重开自动化 | 不自动(doctor 只探+配方;attach 属调试器附加,人工执行) | doctor 一键重开(须主人再批调试器自动化) |
| 4 | 发送动作 | 保留回车(post_key KEY_RETURN,唯一发送点,回车前聚焦断言保落点) | WZ 的 send 按钮点击(sendPoint;多一处坐标依赖,不取) |
| 5 | AX 元素名可信度 | **已定案(r2)**:真机实证元素名在 AXIdentifier 且 BFS 命中(axwalk2-out.txt 全树:chat_input_field/current_chat_name_label/chat_message_list);「漂移改前缀匹配」备选**撤销**(无漂移证据;session_item_* 前缀匹配本来就进 §B-5) | ~~P9 预验~~ 已闭 |
| 6 | dry-run 跳过防重检查 | 跳过(零频控副作用;r2 两轮 dry-run 零占位已实践) | dry-run 也吃防重检查(不取) |
| 7 | **未实证项清算(第三轮,§J-27)**:①搜索命中形态 **已实证**(搜索词进框,OCR 证);②SEARCH_PANE_BOX 主窗几何 **已证伪并修正**(浮窗,§J-25);③session_item_🐳 元素名 **仍悬置**(r2 走了降级链,AX 通道因缺陷 A 未跑通;修通后 P9' dry-run 验);④AXPress 聚焦行为 **仍悬置**(未回车,P10.2 终判);⑤COMPOSER_POINT_NORM **仍悬置**(哨兵未及跑);⑥回执热路径 **仍悬置**(未真发) | 修 A+B+C 后重跑 P9' 预验清单③④⑤,再进 P10 | 悬置项任一倒 → 按对应节回改常量/判据 |
| 8 | pending 落点=on_armed(回车 down 前,WZ 同序)+ on_armed fail-closed(§J-14) | 宁误锁 120s 不开双发窗;聚焦断言失败(未回车但已 pending)也如实吃 17;on_armed 落盘失败=不发送可重试 | 回车后才落 pending(崩溃窗口:回车 up→mark 前进程死 → 指纹空 → 双发洞;不取) |
| 9 | 回执轮询预算 30s 退避 | 保守覆盖冷重建(无零发实测数据,如实);超窗→人工双查补证 | 若 P9/P10 实测热路径+冷重建都快,可收窄 schedule(改常量即可) |

---

## 11. 规模预告(P 系列 = implement.md 的阶段骨架)

| 阶段 | 内容 | 预估 |
|---|---|---|
| P1 | codes+send_state 防重扩展(含 _write_unlocked 读-改-写)+单测 | 2h |
| P2 | sendtarget+单测 | 1.5h |
| P3 | navfilter+pixel x/y+单测 | 2h |
| P4 | axui+system_checks/probe doctor 探针(全窗节点数)+单测 | 2h |
| P5 | sendui 大改+单测(最大件) | 4.5h |
| P6 | cli 接线(--dry-run/doctor/单次解析注入)+单测 | 1.5h |
| P7 | 全量回归基线对账 | 0.5h |
| P8 | README/文档修订(含 §E-5 迁移注记) | 0.5h |
| P9 | 装机热修+假设预验与校准(doctor 双判据/双目标 dry-run/nav_debug/哨兵一致性/热路径计时)+ 冒烟 | 1h |
| P9' | **r2 修正轮(§J-23~26 落码后)**:cp 热修 → 双目标 dry-run 复跑(验 A/B/C:AX 通道可达+浮窗 OCR 有候选+失败清场)+ 悬置项③④⑤(session_item_🐳/AXPress 聚焦/COMPOSER_POINT) | 1h |
| P10 | 真机矩阵(AC4;防重/间隔全用零发或条件执行路径) | 1h(含 ≥10s 间隔等待) |
| P11 | grill 三关+AC7 提交 | 1h |

合计约 19h(含 r2 修正轮 P9')。测试先行顺序:P1→P6 每阶段单测同批落,不留尾部补测。

---

## 12. §J 质询处置记录(2026-10-14,两轮共 22 条;正文已全部并入)

### 第一轮(13 条)

| # | 质询要点 | 处置 | 落点 |
|---|---|---|---|
| 1 | AX 主链无 composer 聚焦,唯一回车落点盲(0.7.0 从未真机发送,README.md:55-56) | **采纳**:§D-2 加「发送前聚焦」行;§1 步骤 j1;聚焦失败=armed 后 exit 15(二轮条 20 定稿为 error 载荷);AXPress 未实证 → §I-7 P9 预验 | §1-j1、§D-2、§I-7 |
| 2 | on_sent_key 裸调可诱发 rollback 双发(G6 红线) | **采纳**:改 on_armed(回车 down 前)+ §C-5 隔离结构;rollback 边界=on_armed 前(二轮条 14 精化为 fail-closed 门) | §1-j0、§C-5 |
| 3 | 坐标换算链断裂(OcrLine 是裁剪系 pixel.py:152-153;_ocr_region 只回文本) | **采纳**:坐标契约写死裁剪系;pane_to_window 三段换算;_ocr_region_lines 新原语;端到端单测 | §B-3、§B-5、§G |
| 4 | probe 单元素判据,半开态锁死 ax 通道,降级不可达(AC3 落空) | **采纳**:probe 双判据 + 跨尝试降级(forced_fallback) | §D-1 |
| 5 | 10.4 立即重复与门序矛盾 | **采纳**:门序反转——指纹门在前、间隔门在后 | §1-5、§C-3 |
| 6 | 回执管线断裂(sendui→localdb 禁环;storage/keys 无来源) | **采纳**:receipt_query 闭包 CLI 构造注入;sendui 零 localdb import(二轮条 19 精化:单次解析复用) | §A、§C-6 |
| 7 | resolve_target 砍掉展示名输入面(pixel.py:173-177 实读核实) | **采纳**:三形态入参 + 展示名反查(二轮条 21 精化:全量拉取+Python 比对) | §B-1 |
| 8 | 回执不校验时间戳 → 同正文历史消息假绿 | **采纳**:ts > since_epoch−2(_normalize_ts 归一秒实读核实);假绿反例单测 | §C-6、§G |
| 9 | unique-row 与候选定义矛盾 | **采纳**:语义修正——救「行在名读不出」不救「行完全没读出」;零候选 → exit 15 拒发为设计内行为 | §B-3-5、§D-3、§G |
| 10 | uncertain 不封闭:回车后才落 pending;单槽被异指纹覆盖 | **采纳**:pending 提前至 on_armed(WZ:270-271 同序);多槽 dict+清扫 | §C-3、§C-4、§I-8 |
| 11 | 「既有单测零改动」不实(test_send_state.py:108/117;test_bridge_cli.py:73-113——均实读核实) | **采纳**:send_state 既有公共行为零改(reserve_send_dedup 拆新);test_bridge_cli 既有 send 如实「签名适配」列名(二轮条 22-2 修正对账式) | §A、§C-3、§G |
| 12 | 关键行为假设全压 P10 交付前夜 | **采纳**:P9 升级为「热修+假设预验与校准」,任一倒 → 回改再进 P10 | §I-7、§11 |
| 13 | KEY_ESCAPE 缺;probe 误判「门开无会话」 | **采纳**:KEY_ESCAPE=0x35 入常量;label 退出 probe 判据 | §B-5、§E-1、§D-1 |

### 第二轮(9 条)

| # | 质询要点 | 处置 | 落点 |
|---|---|---|---|
| 14 | §C-5 骨架(on_armed 抛 → armed=False → raise,fail-closed)与正文/用例⑩「吞掉+继续回车」(fail-open)矛盾——指纹缺失下发出=重开双发窗 | **采纳,fail-closed 为准**:骨架定稿——on_armed 是「进入发送段的门」,失败正常上抛(未回车/CLI rollback/可重试);armed 之后才吞异常;第一轮正文错误表述已删;用例⑩改「on_armed 抛 → 上抛 exit 15 族+无回车+rollback;armed 后 on_receipt_green 抛 → 吞+fingerprint_note」 | §C-5、§1-j0、§G |
| 15 | P10.4b 异指纹「嘻嘻2」有意外真发第 3 条路径(10.4a 幂等不占位+回执轮询+人工核对耗时 → 距上次 reserve >10s → 间隔门放行真发) | **采纳**:10.4b 改**条件执行**——前置读 send_state.json 的 last_send_epoch,now−last <8s 才真跑(期望 exit 14);≥8s 一律跳过真跑,间隔门拦截语义由单测覆盖(test_send_state 既有用例即验),矩阵如实注记「零发验证」;杜绝第 3 条真发 | implement 10.4b |
| 16 | 两键状态文件与「既有原语零改动」未闭合:_write_unlocked 单键整写(send_state.py:125-134 实读核实)会整抹 send_fingerprints(B rollback 抹 A pending);rollback unlink 分支(send_state.py:179)同抹;两承诺字面冲突 | **采纳,下硬指令**:_write_unlocked 改读-改-写保指纹键(私有实现升级,公共可观测行为不变——既有断言零改依然成立);rollback 增「有指纹档→移除 last_send_epoch 键保留指纹档」分支(无指纹场景旧行为不变,test_send_state.py:120-128 断言零改);新增用例「B 占位+rollback 后 A 指纹档仍在」锁死;承诺精确化为「既有公共可观测行为零改动」 | §A、§C-3、§G、implement 1.2 |
| 17 | 降级链「聚焦」只是动作不是断言(与 AX 路三重断言不对称);P9 预验④名为验聚焦实则只验 AXValue 读写链(dry-run 不回车永远验不了聚焦终局) | **采纳**:降级链聚焦=**哨兵读一致性断言**(click composer → read_composer 回 None 或 ==body 才算聚焦;回异值=焦点落别处=focus 失败)——哨兵协议本身即断言,两通道对称;P9 预验④改写为「点位聚焦有效性」(dry-run 哨兵一致性通过=点击带焦点到 composer 的间接证;AX 直证=focused_is_input True);终局真伪以 P10.2 首发composer_cleared 终判,10.2 前置「聚焦证据链完整」门槛防 uncertain 烧额度 | §D-2、§C-2、implement P9-④/P10 |
| 18 | 回执轮询 2s×3 预算对冷重建未论证,超窗=真成功报 uncertain(指纹 pending+120s 拒续发),P10.2 localdb_receipt:true 有翻车风险 | **采纳**:轮询改退避表 RECEIPT_POLL_SCHEDULE=(5,10,15)s 累计 ~30s(保守覆盖,依据如实:冷重建无零发实测数据);P9 预验⑥测热路径计时;P10.2 期望改「localdb_receipt:true,或超窗 false+10.6 人工双查补证后判过」——不假绿 | §C-6、§I-9、implement P9-⑥/P10.2 |
| 19 | resolve_keys 跑两次(resolve_target 一次+receipt 闭包一次;取钥器 timeout-hint 可 clamp 至 1800s,cli.py:152-164;自愈链重复挂住发送路径) | **采纳**:CLI 步骤 2 单次解析 storage/keys,注入 resolve_target(新参 storage=/keys=,缺省自解析供单测)与 receipt 闭包共用;单测断言 resolve_keys 调用次数==1 | §1-2/3、§B-1、§C-6、§G |
| 20 | 「stage=focus 终败=exit 0+sent:false」打破旧契约 exit 0⇒sent:true,未给 MYIA 侧迁移注记 | **采纳**:stage=focus 终败改 **exit 15 error 载荷**(code=send_ax_focus_required,message 注明 pending 已落;消费方零迁移);exit 0 的两处 sent:false 扩展形态(deduped/dry_run)入新增 §E-5 迁移注记,落 P8 README+MYIA push 层提醒 | §E-3、§E-5、§1-j1 |
| 21 | 展示名反查是伪 SQL(compact() 进不了 WHERE;ASCII 名 BINARY collation 不折叠即不命中);alias 反查多行命中未定义(静默取首行=错发风险) | **采纳**:展示名反查改**SQL 全量拉取+Python compact 比对**(去空白+casefold);三路命中集统一唯一性判据——恰 1 建档、>1 一律 send_target_ambiguous(含 alias 多行,绝不取首行)、0 → None;单测补大小写折叠与 alias 多行用例 | §B-1、§G |
| 22 | C-4 缺「跨尝试」行(尝试1 pending 残留 vs 表第 2 行字面矛盾);P7 对账公式算术不对(适配用例仍计入通过数,减项不该存在);node count 绑 window 1 多窗误判 | **采纳**:C-4 补「跨尝试残留」行(armed 过即视同 uncertain,如实);P7 对账式改「通过数=302+新增数,全绿;适配用例列名但不减数」;wechat_ax_node_count 改**全窗最大 UI elements 数**(不绑 window 1),doctor 载荷 note 注明 | §C-4、§G、§D-1、§E-2、implement 7.1/4.2 |

### 第三轮(真机 dry-run r2,5 条;证据见档首「第三轮真机证据」)

| # | 缺陷/事项 | 处置 | 落点 |
|---|---|---|---|
| 23 | **A:axui BFS 底座绑 window 1**——搜索态浮窗是 window 1、主窗退 window 3(System Events 枚举实证,win1=368x370 匿名树/win3=微信 4 顶元素,浮窗 wid 96202)→ AX 原语搜错窗 → probe 恒败 → 恒降级;doctor 同形态数到 nodes=4 误报 closed(doctor-after-p3-inproc.json 实读 ax_gate.nodes=4/input_field=missing)。二轮 §J-22 只修了 system_checks 计数的 window 1 绑定,**axui 元素查找的同款绑定漏网**——本轮补全并如实记二轮修正范围不彻底 | **采纳**:`find_element_by_identifier` 底座 = osascript 单脚本内「枚举全部 windows → 逐窗 BFS」(AXIdentifier 匹配),不依赖 window 顺序;chat_input_field(主窗)与 session_item_*(浮窗)同原语可达 | §B-2-r2、§D-1、§A axui 行 |
| 24 | **B:匹配属性 AXDescription 不命中**(真机具名元素名全在 AXIdentifier,desc 基本空——axwalk2-out.txt 全树实读:current_chat_name_label/chat_input_field/chat_message_list/virtual_cell/tabbar_* 均在 identifier 列);附带 read_current_chat_name no-match 返回字面 `'missing value'` 的哨兵泄漏 | **采纳**:匹配改 AXIdentifier(AXDescription 不用于匹配);read_* 系列统一把 AppleScript 字面 `missing value`/空串规范化为 None——「缺位 → None」契约由此真正落地 | §B-2-r2 |
| 25 | **C:降级链 OCR 盯主窗 SEARCH_PANE_BOX 必零候选**——4.1.15 搜索结果渲染在独立浮窗(r2 截图+OCR 实证浮窗内「filehelper 文件传输助手」「微信号:jiangliushi666」在最常使用区顶部;两目标 JSON 实读均「分区过滤零候选」) | **采纳**:OCR 承载窗改搜索浮窗——`find_search_popup(before_ids)`(CGWindowList 搜索前后 diff 新增微信属主窗,winid.py 同源判据);SEARCH_PANE_BOX 语义改浮窗内归一化 (0.0,0.10,1.0,0.88);三段坐标链几何不变、window 参数换浮窗;diff 不到浮窗 → 如实零候选拒发(不回退主窗);LOCAL_HEADERS 补「最常使用」(r2 实证默认区);AX 主链同享修正(浮窗内 session_item 经全窗 BFS AXPress) | §B-3、§B-5、§D-3 |
| 26 | **D:导航失败无清理**——词留搜索框、浮窗不关(r2 残局实证) | **采纳**:armed 前一切导航失败/超时路径先 `_dismiss_search()`(post_key(KEY_ESCAPE) 关浮窗+清搜索态)再 stage_fail;dry-run 成功收尾同用;armed 后不引入新交互;顺带:navigate 失败的 fix_hint 文案按目标实况给(非 emoji 目标不报「emoji 目标…」提示——r2 两 JSON 文案误导实录) | §B-5、§E-1 |
| 27 | **r2 好消息与悬置项清算**:①doctor BFS 深度判据正常态工作(门=open,nodes 76~123);②搜索词进框(OCR 实证,Cmd+F+Cmd+V 序列有效);③DB 侧三形态 resolve+不存在联系人 exit 1 send_target_not_found 零 UI 扰动全绿(r2/03 JSON 实读);④副文本「微信号:jiangliushi666」实证在场可读——§B-1 alias 兜底假设**升级为实证**,jl666 类目标降级链主路=text_match(副文本),unique-row 依赖下降;⑤§I-5 元素名定案、§I-7 悬置项逐条清算(搜索命中形态/主窗几何已闭,session_item_🐳/AXPress 聚焦/COMPOSER_POINT/回执热路径仍悬置,修 A+B+C 后 P9' 重验) | 好消息入档;悬置项转 P9'(§11) | 档首证据节、§B-1、§D-3、§I-5/7 |

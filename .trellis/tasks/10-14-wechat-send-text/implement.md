# implement.md — send_text 三源合体执行清单(task 10-14-wechat-send-text)

执行者照勾选推进;每步含验证命令。设计依据 = 同目录 `design.md`(下称 D;**2026-10-14
三轮修订版**:两轮质询 §J-1~22 + 第三轮真机 r2 三缺陷 §J-23~27,断言锚到 D 的 §)。
仓库根 = `/Users/zhengbingjin/Project/Github/MYIA`(下称 `$REPO`)。
基线:`uv run --no-sync python -m pytest tests/wechat-bridge -q` = **302 passed /
7 skipped**(prd「现状」节;P7 对账口径见 7.1)。

纪律:①每阶段完跑该阶段验证命令再勾;②全部单测零真机(mock 纪律 D§G);③真机
步骤(P9/P10)严守白名单红线:仅 filehelper 与 jiangliushi666,正文「嘻嘻」,全程
真发 ≤2 条——**防重/间隔矩阵一律用零发或条件执行路径**(10.4);④正文永不进
argv/日志/报告(红线 6);⑤**on_armed = fail-closed 门,armed 后对外恒不抛**
(D§C-5 硬结构,违者返工)。

---

## P1 码表 + 防重状态扩展(≈2h)

- [ ] 1.1 `plugins/wechat-bridge/wechat_bridge/codes.py`:`__all__` 与 `CODE_NAMES`
      (codes.py:18-35/59-73)加 `SEND_UNCERTAIN_DEDUP = 17`("send_uncertain_dedup");
      docstring 注记「§6 修订 2026-10-14:17 = 指纹 pending 命中,uncertain-never-retry
      (design.md §E-4)」。
- [ ] 1.2 `send_state.py`(**既有公共可观测行为零改动**——reserve_send/
      check_send_allowed/record_send/load_last_send_epoch 的签名与行为不动,
      test_send_state.py:104-141 既有断言零改,D§J-11/16):
  - [ ] 1.2.1 模块常量 `DEDUP_WINDOW_SECONDS = 120.0`、`FINGERPRINT_CAPACITY = 8`
        (硬编码,G6 风格无配置键)。
  - [ ] 1.2.2 `@dataclass(frozen=True) ReserveOutcome{previous: float|None,
        dedup: str|None}`(D§C-3)。
  - [ ] 1.2.3 **`_write_unlocked` 私有实现升级为读-改-写**(D§J-16 硬指令;现状
        send_state.py:125-134 写死整份 `{"last_send_epoch": …}` 会**整抹**
        `send_fingerprints`——B 异指纹失败 rollback 即抹 A 的 pending,实洞):临界区
        内先读现文件,保留 `send_fingerprints` 键原样,只更新 `last_send_epoch` 再
        tmp+os.replace 原子落盘。私有函数内部升级,公共原语外部行为不变。
  - [ ] 1.2.4 `rollback_reserve` 增分支(D§J-16):**无指纹档**(现文件无
        send_fingerprints 或空 dict)→ 旧行为完全不变(previous=None → unlink 文件,
        test_send_state.py:120-128 断言零改;有 previous → 写回旧值);**有指纹档** →
        previous=None 时不再 unlink,改为移除 `last_send_epoch` 键、保留指纹档
        (unlink 会把 A 的 pending 一起删);docstring 写明两分支。
  - [ ] 1.2.5 **新原语 `reserve_send_dedup(self, now, fingerprint) ->
        ReserveOutcome`**(发送路径专用):同一 flock 临界区三步,**门序=指纹门在前、
        间隔门在后**(D§C-3/§J-5:指纹 sent 命中且窗内 → ReserveOutcome(None,
        "sent_recently") 不占位——立即重复同指纹得幂等而非 exit 14;指纹 pending
        命中且窗内 → BridgeError(17,fix_hint=「等待 120s 或换正文;人工确认后再
        操作」);然后间隔门(判据不变)→ 占时间戳(经 1.2.3 读-改-写)+ 顺手清扫
        指纹档)。既有 `reserve_send` docstring 注「发送路径走 reserve_send_dedup」。
  - [ ] 1.2.6 **多槽指纹**:`mark_fingerprint_pending(key, now)`(on_armed 调,回车
        down 前;只写自己的 key 不覆盖他档)/ `mark_fingerprint_sent(key, now)`
        (仅同 key 才 pending→sent 升级);两者各自动写 + 清扫(删过期 >120s 条目、
        容量 >8 按 ts 淘汰最旧;D§C-3/§J-10)。
  - [ ] 1.2.7 状态文件两键:`{"last_send_epoch": float, "send_fingerprints":
        {"<sha256hex>": {"status": "pending|sent", "ts": float}}}`;`_read_unlocked`
        不动;旧格式文件(仅 last_send_epoch)可读兼容。
  - [ ] 1.2.8 模块 docstring:门序论证 + 多槽并发论证 + **写路径保全论证** +
        rollback 两分支纪律(D§C-3/§C-4 表照抄)。
- [ ] 1.3 `tests/wechat-bridge/test_send_state.py` **纯新增**用例(既有零改):
      sent 幂等(**含 <10s 立即重复 → 幂等而非 exit 14**)/pending→17/>120s 过期
      放行/两门同临界区/清扫(过期+容量 8)/并发交错(A pending 后 B 异指纹
      sent,A 同指纹重发仍被拒)/**写路径保全:B 占位后 rollback,A 的指纹档仍在
      (锁 §J-16 实洞)**/**rollback 两分支:无指纹场景旧行为(既有断言即此)/
      有指纹场景移键保留指纹档**/pending→sent 升级/mark_sent 异 key 不覆盖/
      旧格式文件兼容/既有 reserve_send 回归(零改即过)。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_send_state.py -q
# 期望:既有用例原样通过 + 新增全绿(既有破=实现走样,回改实现不改测试)
```

---

## P2 DB 侧目标解析 + 搜索词选择(≈1.5h)

- [ ] 2.1 新建 `plugins/wechat-bridge/wechat_bridge/sendtarget.py`(依赖方向 D§A:
      sendtarget → localdb/localdb_query):
  - [ ] 2.1.1 `SendTarget` frozen dataclass{username, alias, display_name, search_term}
        (D§B-1)。
  - [ ] 2.1.2 `resolve_target(config, chat_id, *, storage=None, keys=None,
        data_root=None) -> SendTarget | None`——**三形态入参 + storage/keys 注入**
        (D§B-1/§J-7/19:sessions list 的 id 本就是展示名,pixel.py:173-177;storage/
        keys 由 CLI 单次解析注入,缺省自解析供单测):localdb 链(注入则用;缺省
        locate→resolve→ensure 同 cli.py:369-371;BridgeError 20/21/22 原样透传,
        message 注记「发送前目标解析」;链失败=拒发)→ contact 副本 sqlite
        **三路命中集统一唯一性判据**(D§J-21:多行命中一律 ambiguous,绝不静默
        取首行=错发风险):①username 正查(SQL 等值,多行视同库异常→ambiguous);
        ②alias 反查(SQL 等值拉**全部**命中行);③展示名反查——**SQL 只做全量拉取
        `SELECT <id>,<alias>,<remark>,<nick_name> FROM contact`(千行级),Python
        侧 compact 比对**(去空白+casefold;compact() 进不了 sqlite WHERE、ASCII 名
        BINARY collation 不折叠大小写——伪 SQL 不可执行,D§J-21);判据:三路命中
        合集去重(按 username)**恰 1 → SendTarget;>1 → BridgeError(exit 1,
        code="send_target_ambiguous",fix_hint=「命中多个联系人,请用 alias 或
        username(wxid)消歧」);0 → None**(不查 stranger 表,注释如实,靶场实证)。
        列名自适应用 localdb_query._columns/_pick;display_name 取
        remark>nick_name>alias。
  - [ ] 2.1.3 `pick_search_term(username, alias, display_name) -> str`:四档规则
        (D§B-1;alias 纯 ASCII ≥3 → 非 wxid_ 纯 ASCII username → wxid_ username →
        display_name)。
  - [ ] 2.1.4 `row_match_terms(target) -> list[str]`:[display_name, search_term,
        alias, username] 去空去重。
  - [ ] 2.1.5 `fingerprint(target, body) -> str`:sha256(username + "\\0" + body) hex
        (WZ:138-141 同构;三形态入参同目标同 key)。
- [ ] 2.2 `tests/wechat-bridge/test_send_target.py`(D§G 行):三形态正查(filehelper)
      /alias 反查(jiangliushi666)/**展示名全量拉取+Python 比对**(「文件传输
      助手」「🐳」;**大小写折叠用例**「FileHelper」→命中)/remark 优先序/查无
      None/**alias 反查多行 → send_target_ambiguous**/**storage/keys 注入路径
      (注入时不自解析)**/localdb 链失败透传(20/21/22)/四档搜索词/指纹稳定性
      (三入参同目标同 key)。sqlite 用 tmp_path 建假 contact 库(localdb 链整体
      monkeypatch 注入副本目录)。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_send_target.py -q
```

---

## P3 分区过滤纯逻辑 + 窗口坐标(≈2h)

- [ ] 3.1 `pixel.py`:`WindowInfo` 加 `x: float = 0.0`、`y: float = 0.0`
      (pixel.py:126-133);`find_main_window` 把 kCGWindowBounds 的 X/Y 存入
      (pixel.py:238-249);`to_payload` 加 `"x"/"y"`(pixel.py:135-148)。
- [ ] 3.2 新建 `navfilter.py`(stdlib only,D§B-3 逐条):
  - [ ] `LOCAL_HEADERS` / `JUNK_HEADERS`(D§B-3;**LOCAL 含 r2 实证的「最常使用」
        默认区**,§J-25;JUNK 含「功能/功能分类/搜一搜/文章/智能工具/朋友圈动态/
        表情/视频号/直播/新闻/购物/小程序码」)。
  - [ ] `SEARCH_PANE_BOX = (0.0, 0.10, 1.0, 0.88)`——**搜索浮窗内归一化**(r2 实证
        搜索结果在独立浮窗不在主窗,§J-25;P9' 预验校准)。
  - [ ] `compact(text)`(去全部空白+casefold)。
  - [ ] `RowPick{cx, cy, rule, term}`(**坐标契约 = SEARCH_PANE_BOX 裁剪图归一化**,
        OcrLine 同系,pixel.py:152-153;docstring 写死,D§J-3)。
  - [ ] `select_result_row(lines, terms) -> RowPick | None`:D§B-3 算法六步(y_junk
        优先;评分 (term_rank, 0|1|2);并列 y 最大再 x 最小;unique-row 兜底=无命中
        +候选恰 1+limit 在场——救「行在名读不出」不救「行完全没读出」(0 候选 →
        None 拒发),D§J-9;点击点=文本本体中心)。
  - [ ] `pane_to_window(pane_box, cx, cy)`(第二段换算)。
  - [ ] `row_box_to_screen(window, wx, wy)`(第三段换算,依赖 WindowInfo x/y)。
- [ ] 3.3 `tests/wechat-bridge/test_navfilter.py`(D§G 行全用例;fixtures 用裁剪系
      坐标):分区头过滤/评分/并列/**unique-row 三态:乱码单行采纳、零候选 None、
      候选≥2 不触发**/分区头集合含「功能分类/搜一搜」/**坐标换算链三段端到端**
      (裁剪系 fixture → pane_to_window → row_box_to_screen,WindowInfo(x=100,y=200,
      w=800,h=600) 断屏幕像素,D§J-3)。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_navfilter.py tests/wechat-bridge/test_pixel.py -q
```

---

## P4 AX 原语 + doctor 探针(≈2h)

- [ ] 4.1 新建 `axui.py`(中文 docstring;`_run`/`monotonic`/`sleep` 模块级注入点,
      SUBPROC_TIMEOUT_S=10 → exit 30,抄 sendui.py:75-77/177-193):
  - [ ] **`find_element_by_identifier(identifier, *, value_contains=None, timeout_s=2.0)
        -> 元素引用 | None`——底座 = osascript 单脚本内「枚举全部 windows → 逐窗
        BFS」+ AXIdentifier 匹配**(D§B-2-r2/§J-23/24,r2 三缺陷 A+B 的修正:
        搜索态浮窗是 window 1、主窗退 window 3,绑 window 1 必搜错窗;AXDescription
        真机基本为空不匹配;**read_* 系列把 AppleScript 字面 `missing value`/空串
        规范化为 None**,堵 `'missing value'` 哨兵泄漏)。chat_input_field(主窗)与
        session_item_*(浮窗)同原语可达。
  - [ ] `probe_wechat_ax() -> bool`——双判据(D§D-1/§J-4/13/23):
        `wechat_ax_node_count() > 5` AND `read_input_value() is not None`
        (底座 = find_element_by_identifier,全窗遍历);**label 不进门**;docstring
        注记副作用=AX 查询自然触发 activateQtAccessibility(REV:20-24)。
  - [ ] `write_search_value(term) -> bool`(Cmd+F 后 AXValue 直写焦点元素,
        REF:27-28)。
  - [ ] `press_session_item(name) -> bool`(轮询 `find_element_by_identifier`
        ("session_item_" 前缀/名含目标,全窗遍历命中浮窗内元素)→ AXPress,
        D§J-23/25)。
  - [ ] `read_current_chat_name() -> str | None`(label 直读;缺位/missing value →
        None 不拦通道,§J-24)。
  - [ ] `read_input_value() -> str | None` / `write_input_value(text) -> bool`。
  - [ ] `focus_input() -> bool`(chat_input_field AXPress + 复读 value 断言正文未丢;
        行为未实证 → P9 预验项,D§J-1/§I-7)。
  - [ ] `focused_is_input() -> bool | None`(osascript 读 AXFocusedUIElement;取不到
        → None 如实)。
- [ ] 4.2 `system_checks.py` 加 `wechat_ax_node_count() -> int | None`——**全部窗口
      最大 UI elements 数,不绑 window 1**(D§J-22:多窗时 z-order 首窗未必主窗,
      绑死会把门开误判 closed 白走降级链;osascript 单脚本 `repeat with w in
      windows` 取 max);失败 → None;可注入。
- [ ] 4.3 `probe.py` 加 `run_doctor(...) -> dict`(复用 run_probe 载荷 + ax_gate 节
      {nodes/state/input_field/note/fix_hint},note 注明 nodes=全窗最大数;fix_hint
      给 REV LLDB 配方摘要,D§E-2 形状)。
- [ ] 4.4 `tests/wechat-bridge/test_axui.py` + `test_probe.py` 扩(probe 双判据用例:
      门开+无输入区 → False;label 缺位不影响;doctor 载荷三态含 input_field;
      **多窗最大数语义断言**——mock 返回多窗脚本形状)。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_axui.py tests/wechat-bridge/test_probe.py -q
```

---

## P5 sendui 大改(最大件,≈4.5h)

改动全在 `plugins/wechat-bridge/wechat_bridge/sendui.py`(现 555 行;模块 docstring
同步改:三源出处/五件套/通道分层/聚焦断言两通道对称/fail-closed 门与 armed 段隔离/
点击范围收窄纪律)。

- [ ] 5.1 CGEvent hardened:`_event_source()`(CGEventSourceCreate(0) 缓存句柄,失败
      回退 None 如实)+ `click_at(x, y)`(moved 60ms/down 35ms/up,事件带 source,
      WZ:33-41)+ `post_key` 两事件换 source(WZ:25-31)。常量
      `EVENT_SOURCE_COMBINED = 0`、`KEY_C = 0x08`、`KEY_ESCAPE = 0x35`(D§J-13)、
      `COMPOSER_POINT_NORM = (0.50, 0.83)`。
- [ ] 5.2 删盲回车键序:sendui.py:405-407 的 `KEY_DOWN_ARROW`+`KEY_RETURN` 序列删除;
      `KEY_DOWN_ARROW` 常量退役。
- [ ] 5.3 新常量:SEARCH_RENDER_TIMEOUT_S=5.0 / SEARCH_POLL_S=0.5 / SEARCH_RENDER_S=1.2
      / CLICK_SETTLE_S=0.3 / SENTINEL_GAP_S=0.06 / CLEAR_POLL_TIMES=12 /
      CLEAR_POLL_GAP_S=0.08 / **`RECEIPT_POLL_SCHEDULE = (5.0, 10.0, 15.0)`**(回执
      退避累计 ~30s,D§J-18);新注入点 **`wall_clock: Callable[[], float] =
      time.time`**(回执 since_epoch,D§C-6)。
- [ ] 5.4 `read_composer_via_clipboard(window) -> str | None`(D§C-2 协议逐行)。
- [ ] 5.5 **新原语 `_ocr_region_lines(window, box, workdir, tag) -> list[OcrLine]`**
      (坐标=裁剪图归一化,D§J-3;旧 `_ocr_region` 拼接文本保留);**新原语
      `find_search_popup(before_ids) -> WindowInfo | None`**(D§B-5/§J-25:r2 实证
      搜索结果在独立浮窗——CGWindowList 搜索前后 diff 出新增微信属主窗 = 浮窗,
      winid.py 同源判据;diff 不到 → None 如实零候选拒发,不回退主窗);**失败清理
      `_dismiss_search()`**(D§J-26:post_key(KEY_ESCAPE) 关浮窗+清搜索态,armed 前
      一切导航失败/超时路径与 dry-run 收尾先清场再 stage_fail/返回;armed 后不引入
      新交互);`_navigate(target, window, channel, workdir)`(D§B-5 两通道序列):
      降级链 OCR 路 = `find_search_popup(before_ids)` → `_ocr_region_lines(popup,
      SEARCH_PANE_BOX)` → `select_result_row` → `pane_to_window` →
      `row_box_to_screen(popup,…)` → `click_at`(**坐标链承载窗=浮窗**,三段几何
      不变);AX 路 = write_search_value + press_session_item(find_element 全窗底座);
      无候选 → `_dismiss_search()` → stage_fail("navigate")(fix_hint 按目标实况,
      非 emoji 目标不报 emoji 提示,§J-26)。
- [ ] 5.6 `_attempt_send` 改造(签名加 target/channel/forced_fallback/dry_run;
      D§1 序列 b-i):通道判定 axui.probe(**跨尝试降级**:本尝试失败原语为 AX
      能力缺失 → 下一尝试 forced_fallback 直走 cgevent_ocr,D§D-1)→ 降级链导航前
      OCR 标题带记 baseline_title(emoji indirect 基准)→ 导航 → 标题双验证(AX:
      read_current_chat_name 精确,label 缺位走 OCR;降级:_title_matches,emoji 走
      indirect 证据链,**零候选 → exit 15 拒发=设计内行为**,D§J-9)→ 哨兵空断言
      (非空→清→复探→仍非空 stage_fail("composer_not_empty"))→ 写入(AX 直写;
      降级剪贴板+Cmd+V)→ 回读四路(剪贴板对账 → axui.read_input_value →
      Cmd+A+Cmd+C 全量("clipboard_copy")→ OCR 输入带)。
- [ ] 5.7 `send_text` 主口改造(签名 `(config, target, body, *, dry_run=False,
      on_armed=None, on_receipt_green=None, receipt_query=None)`;**D§C-5 骨架
      逐行落地**):
  - [ ] **fail-closed 门**:`try: on_armed() except Exception: raise`——失败=未回车/
        指纹未落/CLI rollback/可重试(D§J-14,**绝不吞**);成功后 `armed=True`,
        armed 段整体 try/except Exception 吞异常(note 如实;含 on_receipt_green/
        receipt_query 调用失败 → `fingerprint_note`/`post_send_note`)。
  - [ ] dry_run 分支:回读确认后 Cmd+A+Delete 清草稿 → 降级链处搜索态再
        post_key(KEY_ESCAPE) → 载荷 sent:false/dry_run:true/nav_debug:{pick_rule,
        pick_cx, pick_cy, terms_hit} → return(无回车无 on_armed零频控副作用)。
  - [ ] 发送段:`since_epoch = wall_clock()` → **on_armed()** → **发送前聚焦断言
        两通道对称**(D§D-2/§J-17:AX 路 focus_input+复读 value==body+
        focused_is_input 尽力断言;**降级链 click_at(COMPOSER_POINT)→ 哨兵读一致
        性断言:read_composer 回 None(空)或 ==body 才算聚焦成立,回异值=焦点落
        别处=focus 失败**——哨兵协议本身即断言,不是裸点击)→ 失败:重试次数内
        下一尝试/耗尽 → **exit 15 error 载荷**(code=send_ax_focus_required,
        message 注明「未回车;指纹已 pending,120s 内同指纹重发将 exit 17」,
        D§J-20,不破 exit 0⇒sent:true)→ 唯一一次 post_key(KEY_RETURN) →
        `_wait_composer_cleared`(AX 直读;降级哨兵,12×80ms)→ 回执轮询
        `receipt_query(target.username, body, since_epoch)`(**按
        RECEIPT_POLL_SCHEDULE=(5,10,15)s 退避,累计 ~30s**,D§J-18;True →
        on_receipt_green())→ 既有 `_post_send_verify` 辅助 → 载荷新键(D§E-3:
        target/channel/title_verify/composer_cleared/localdb_receipt/
        fingerprint_note/deduped)。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_send_ui.py -q
```

- [ ] 5.8 `tests/wechat-bridge/test_send_ui.py` 扩(FakeHarness 加 clicks/ax 读写/
      composer 态/clear 态/wall_clock 假钟;D§G test_send_ui 行 ①~⑫;键序断言:
      KEY_RETURN 仅发送点一次/失败路径无 KEY_RETURN/无 KEY_DOWN_ARROW/dry-run 有
      KEY_ESCAPE;**⑩ on_armed fail-closed:抛 OSError → 上抛 exit 15 族+无回车+
      CLI rollback+指纹未落;armed 后 on_receipt_green 抛 → 吞+fingerprint_note
      如实**(D§J-14);**⑪ 聚焦两通道:AX focus_input False → exit 15 error+
      stage 注记+无回车;降级 composer 点击后哨兵读异值 → focus 失败、回 None/
      ==body → 过**(D§J-17);**⑫ 回执轮询按 (5,10,15) 退避形态**(假钟推进断言
      调用时序,D§J-18))。

---

## P6 CLI 接线(≈1.5h)

- [ ] 6.1 `ax.py`:`send_text(config, target, body, *, dry_run=False, on_armed=None,
      on_receipt_green=None, receipt_query=None)`,docstring 补 on_armed 边界条款
      (D§C-4);委托 sendui 同签名。
- [ ] 6.2 `cli.py`:
  - [ ] 6.2.1 send parser 加 `--dry-run`(store_true,default=False;help=「走到粘贴
        回读不回车;零频控副作用可重跑」)。
  - [ ] 6.2.2 `send_text` 分支重写(cli.py:336-359 骨架保留):stdin → **步骤 2:
        `storage = localdb.locate_db_storage()`;`keys = localdb.resolve_keys(
        storage, config=config)` 单次解析**(D§J-19:取钥器交互/自愈链全程至多一次)
        → `sendtarget.resolve_target(config, chat_id, storage=storage, keys=keys)`
        (None → BridgeError(1, code="send_target_not_found");ambiguous 透传)→
        `key = sendtarget.fingerprint(target, body)` → dry_run=True 跳过频控直入 →
        否则 `outcome = rate_state.reserve_send_dedup(now=now, fingerprint=key)`
        (记 previous):outcome.dedup=="sent_recently" → 幂等载荷 exit 0(D§E-3;
        **指纹门先于间隔门**,D§J-5);BridgeError 17 上抛(未占位)→
        **receipt_query 闭包(复用上述 storage/keys,零重复解析)**:判定 =
        query_history(username, 1d) messages 中 text 空白不敏感对账命中 body
        **AND int(ts) > since_epoch - 2**(ts 归一秒,localdb_query.py:192-200;
        localdb 链 BridgeError → None,D§C-6/§J-8)→ `ax.send_text(config, target,
        body, dry_run=args.dry_run, on_armed=lambda: rate_state.
        mark_fingerprint_pending(key, now=_now()), on_receipt_green=lambda:
        rate_state.mark_fingerprint_sent(key, now=_now()), receipt_query=
        receipt_query)`——rollback 不走回调:既有 `except BridgeError:
        rollback_reserve(now, previous); raise` 语义原样保留(仅 on_armed 前路径
        可及)。
  - [ ] 6.2.3 新顶层子命令 `doctor`(handler = `_emit(probe.run_doctor(config=
        config, bridge_version=...))` return 0,状态查询不判错)。
- [ ] 6.3 `tests/wechat-bridge/test_bridge_cli.py` **扩+既有适配**(D§G):
  - [ ] 既有 send 用例(④/④b 族,test_bridge_cli.py:73-113)机械适配:桩签名换新
        形态 + monkeypatch `sendtarget.resolve_target` 返回固定 SendTarget——逐条
        列名记入提交说明(适配≠放松);
  - [ ] 新用例:--dry-run 契约(零频控副作用:dry-run 后立即可真发不被 14 拦)/
        指纹幂等 exit 0(含 <10s 立即重复)/exit 17/not_found 与 ambiguous 的
        exit 1 code/**单次解析断言(monkeypatch 计数 localdb.resolve_keys 调用
        次数 ==1,D§J-19)**/doctor 载荷形状/receipt_query 闭包假绿反例
        (ts≤since-2 → False;新消息 → True)/**stage=focus 终败 → exit 15
        error 载荷**(D§J-20)/G6 接线既有用例不回退。

验证:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge/test_bridge_cli.py tests/wechat-bridge/test_ax_gate.py -q
```

---

## P7 全量回归 + 基线对账(≈0.5h)

- [ ] 7.1 全量绿;**对账口径(D§J-22 定稿:适配的既有用例仍全绿仍计入通过数——
      减项不存在)**:`通过数 = 302 + 新增数,全绿`;test_send_state.py 既有用例
      零改(若破=实现走样,回改实现不改测试);6.3 列名的适配用例 git diff 逐条
      目检(仅签名/mock 面,断言语义不变):

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge -q
git -C "$REPO" diff tests/wechat-bridge/test_bridge_cli.py | head -80   # 适配面目检
```

- [ ] 7.2 GitNexus 影响面核查(提交前门,AGENTS.md 纪律):

```bash
cd "$REPO" && gitnexus detect-changes -r shishi --scope staged   # staging 后跑
```

---

## P8 文档修订(≈0.5h)

- [ ] 8.1 `plugins/wechat-bridge/README.md`:红线 1 send_text 例外句补「+ 合成鼠标
      点击(仅导航行与 composer 聚焦;PRD 2026-10-14 翻案,design.md §I-1)」;
      码表/运行形态节补 `--dry-run` 与 `doctor`;能力边界节补三源合体条目(门序/
      多槽指纹/聚焦断言/fail-closed 门要点)+ **§E-5 消费方迁移注记**(exit 0 两处
      sent:false 扩展形态:deduped/dry_run,MYIA push 层按分支键判,D§J-20)。
- [ ] 8.2 sendui/send_state 等模块 docstring 与 design.md 对齐(落完代码回头核对)。

验证:`git -C "$REPO" diff --stat` 目检改动面 = 本清单文件集合。

---

## P9 装机热修 + **假设预验与校准**(≈1h;零真发;D§J-12/17/18)

- [ ] 9.1 cp 改动件到装机活体(D§H;先 `diff -q` 逐文件核对仅本任务改动):

```bash
SRC="$REPO/plugins/wechat-bridge/wechat_bridge"
DST="$HOME/.myia/plugins/wechat-bridge/wechat_bridge"
for f in codes.py send_state.py sendtarget.py navfilter.py axui.py sendui.py ax.py cli.py pixel.py system_checks.py probe.py; do
  diff -q "$SRC/$f" "$DST/$f" || cp -v "$SRC/$f" "$DST/$f"
done
```

- [ ] 9.2 **冒烟 + 假设预验清单**(每项留痕任务档;任一倒 → 回改设计常量/通道判据,
      改完重跑,再进 P10——发现时点必须在交付前夜之前):

```bash
B="$HOME/.myia/plugins/wechat-bridge/bin/wechat-bridge"
"$B" --probe                                            # exit 0,三态载荷
"$B" doctor                                             # 预验①:ax_gate.nodes>5(全窗最大数)
                                                        #   且 input_field=ok(双判据实测)
"$B" send_text --help                                   # usage 含 --dry-run
echo 嘻嘻 | "$B" send_text filehelper --file - --dry-run # 预验②:search_term 命中形态+
                                                        #   导航点击落点(nav_debug.pick_*)
echo 嘻嘻 | "$B" send_text jiangliushi666 --file - --dry-run  # 预验③:alias 搜索+🐳 行
                                                        #   OCR 实况三态如实记录
```

  - [ ] 预验④(**聚焦有效性,改写版**,D§J-17:dry-run 不回车验不了终局,只验
        「点位/AXPress 把焦点带到 composer」):降级链 dry-run 中**哨兵空断言/
        聚焦一致性断言通过** = COMPOSER_POINT 点击与哨兵协议聚焦有效的间接证据;
        AX 路 focus_input 后 focused_is_input=True 为直证(None 如实);两证据记入
        **P10.2 前置门槛:聚焦证据链完整(哨兵一致性过 + AX 直证或间接证)才准
        首次真发**,防 uncertain 烧白名单额度。
  - [ ] 预验⑤:几何校准——nav_debug 的 pick 坐标换算后点击命中目标行(未中 → 调
        SEARCH_PANE_BOX/行框参数重跑 dry-run,稳定命中 ≥2 次);COMPOSER_POINT_NORM
        同法(哨兵探测成功=点中)。
  - [ ] 预验⑥(**回执热路径计时**,D§J-18):`time "$B" localdb query filehelper
        --since 1d`(副本新鲜路径的耗时应远小于 30s 预算;冷重建不可零发实测,
        预算保守 30s 维持,如实注记)。
- [ ] 9.3 dry-run 后核频控无副作用:`send_state.json` 无新 last_send_epoch 变动/
      无指纹档。

---

## P9' r2 修正轮(≈1h;零真发;§J-23~27 落码后的复验)

前置:P4/5.5 按 r2 修正落码(全窗 BFS/AXIdentifier/missing value→None/浮窗 OCR/
失败清理),单测同步更新后全绿。

- [ ] 9'.1 热修 cp(同 9.1 命令面)+ 全量单测绿:

```bash
cd "$REPO" && uv run --no-sync python -m pytest tests/wechat-bridge -q
```

- [ ] 9'.2 **双目标 dry-run 复跑**(验 A/B/C 三缺陷闭合,留痕 r3 目录):
      ①filehelper dry-run:期望不再「分区过滤零候选」——AX 通道可达(channel=ax,
      probe 全窗底座)或降级链浮窗 OCR 有候选(载荷 nav_debug.pick_rule 非 None);
      ②jl666 dry-run:同上 + 副文本「微信号:jiangliushi666」text_match 路径;
      ③失败路径清场核(若造一次失败):微信回到无搜索态(词清/浮窗关,目检+截图)。
- [ ] 9'.3 悬置项(§I-7 清单):session_item_🐳 元素名(AX 路 dry-run 实测)/
      AXPress 聚焦(focus_input 后 focused_is_input 直证尽力)/COMPOSER_POINT_NORM
      (降级路哨兵一致性);留痕,倒则按对应节回改常量再进 P10。

---

## P10 真机测试矩阵(AC4;≈1h;红线:≤2 真发,仅两白名单,正文「嘻嘻」)

前置:P9 预验①-⑥ 全过(聚焦证据链完整门槛);每次真发前目视微信前台态正常。

- [ ] 10.1 dry-run 导航 ×2——P9.2 已覆盖,核载荷 channel/title_verify 留痕(🐳 目标
      降级链零候选 → exit 15 拒发是**设计内行为**,留痕后走 AX 主线路径)。
- [ ] 10.2 真发 #1:`echo 嘻嘻 | "$B" send_text filehelper --file -` → exit 0,
      sent:true,**composer_cleared:true(回车落点终局真伪以此为准,D§J-17)**,
      localdb_receipt:true(**或超窗 false → 10.6 人工双查补证后判过,不假绿**,
      D§J-18);微信 UI 人工目检文件传输助手收到「嘻嘻」。
- [ ] 10.3 间隔等待 ≥10s(G6 强制;exit 14 属正常,等 retry_after 后重试)。
      真发 #2:`echo 嘻嘻 | "$B" send_text jiangliushi666 --file -`(两真发指纹
      不同,防重不拦;间隔门独立生效)→ 同 10.2 核对(🐳 目标 channel/title_verify
      按 P9 实况;回执按 wxid 查不受 emoji 影响)。
- [ ] 10.4 防重/间隔矩阵(**零发与条件执行版**,D§J-15:杜绝意外第 3 条真发):
  - [ ] a. 同指纹立即重复(10.3 同命令连跑)→ **exit 0 幂等载荷** sent:false/
        deduped:true(指纹门先于间隔门);零新发核验:send_state.json 时间戳未变 +
        微信无新消息;
  - [ ] b. 异指纹间隔门(期望 exit 14)——**条件执行**:先读
        `~/Library/Application Support/MYIA/wechat-localdb/send_state.json` 的
        last_send_epoch,`now − last < 8s` 才真跑 `echo 嘻嘻2 | "$B" send_text
        filehelper --file -`(期望 exit 14 零新发);**≥8s 一律跳过真跑**(10.4a
        幂等不占位+回执轮询+人工核对耗时极易把间隔耗过,真跑=意外真发第 3 条,
        红线击穿),间隔门拦截语义由单测覆盖(test_send_state 既有用例即验
        exit 14),矩阵如实注记「零发验证+单测覆盖」;
  - [ ] c. pending→exit 17 路不人为制造(不主动制造不确定发送;单测覆盖,如实注记)。
- [ ] 10.5 不存在联系人干净拒发:`echo 嘻嘻 | "$B" send_text no_such_zzz123 --file -`
      → exit 1 code=send_target_not_found,微信零扰动(全程无激活);多义名
      (send_target_ambiguous)无白名单内同名数据则单测覆盖,如实注记。
- [ ] 10.6 localdb 回执双查(红线 4 留痕):对两目标各跑
      `"$B" localdb query <username> --since 1d` 核「嘻嘻」在消息列表且时间戳为
      刚刚(与 10.2/10.3 载荷 localdb_receipt 互证;10.2/10.3 超窗 false 时以此
      补证判过)。
- [ ] 10.7 剪贴板恢复核:真发前 `echo before_test | pbcopy`,命令后 `pbpaste`
      应回 `before_test`。

---

## P11 grill 三关 + 提交(AC5/AC6/AC7;≈1h)

- [ ] 11.1 grill 设计关:对照 prd AC1-AC3 逐条在 design.md(两轮质询修订版)找
      落点;§J 22 条处置逐条复核已并入;缺口补或如实注记。
- [ ] 11.2 grill diff 关:全量 diff 自查(点击范围收窄/盲回车删除/回车唯一性/
      on_armed fail-closed/armed 段隔离/rollback 两分支与指纹保全/门序/多槽/
      三段坐标换算/载荷不载正文)。
- [ ] 11.3 grill 测试关:P7 基线对账(通过数=302+新增)+ P9 预验留痕 + P10 矩阵
      证据归档(载荷 JSON 存 `.trellis/tasks/10-14-wechat-send-text/` 下,文件名带
      目标与时间;不含正文之外的聊天内容——「嘻嘻」是测试正文可留)。
- [ ] 11.4 提交入库(桥源码+测试+任务档):
      `git add plugins/wechat-bridge tests/wechat-bridge .trellis/tasks/10-14-wechat-send-text`
      → `gitnexus detect-changes -r shishi --scope staged` 过 → commit(消息模板照
      仓库惯例 `feat(bridge): send_text 三源合体 …`)。

---

## 完成定义(AC 对账)

| AC | 勾选位 |
|---|---|
| AC1 导航零盲回车 | 5.2/5.5 + test_navfilter + 9.2 预验②③⑤ |
| AC2 五件套 | P1/P5(5.4/5.7)+ test_send_state/test_send_ui |
| AC3 AX 主链+降级+doctor | P4/P5(5.6 双判据+跨尝试降级)+ 9.2 doctor + 10.1 |
| AC4 真机矩阵 | P10 全(10.4 零发与条件执行版) |
| AC5 基线不回退+装机冒烟 | 7.1(通过数=302+新增)+ 9.2 |
| AC6 grill 三关 | 11.1-11.3(含 §J 22 条处置复核) |
| AC7 提交 | 11.4 |

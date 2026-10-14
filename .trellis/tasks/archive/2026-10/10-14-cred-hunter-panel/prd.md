# PRD — 凭证猎手面板(V1 只读:key/高危列表屏)

> 任务:10-14-cred-hunter-panel · 状态:in_progress(交付完成待归档;AC 八条全勾,证据见 check.jsonl)· 优先级:P2 · 规范键:E
> 池源:`10-03-v12-backlog/prd.md:95`(「凭证猎手面板(key/余额/高危列表,对标 aipocket;只展示与管理,不含导出——与 G11 红线区分)」,远期形态三项之一)
> V1 形态令(主人,2026-10-14):**先只读面板后交互,先窄后宽**——本任务只交付只读面板;交互(验证触发/余额持久化/状态流转)全部推 V2。

## Goal

给桌面端一个「凭证猎手」屏:把 credhunter 插件已落地的本地密钥库(`credhunter-keystore.json`,猎→存→验通路的数据面)以**掩码-only 的只读表格**呈现——全部密钥列表 + 高危过滤视图 + 证据展开,零新增网络行为、零凭据暴露面扩大。

对标 aipocket 的 AllKeysPage(全部密钥)/HighValuePage(高价值 Key)两屏的**布局与行为思想**;许可红线下的取舍见 §2。

## 1. 背景与现状(不重做清单)

引擎侧全部已交付(10-03-aipocket-fusion,已归档),本任务**纯 UI + 一枚只读协议方法**,不碰引擎:

| 既有交付 | 证据 |
|---|---|
| credhunter 插件三能力(credhunt/credcheck/exposure) | `plugins/myssia-credhunter/plugin.yaml` provides 节 |
| 本地密钥库:指纹→全文,`$MYIA_HOME/credhunter-keystore.json`,600 权限,原子写;结构 version=1,records{fingerprint: {apikey, provider, first_seen, last_seen, hit_count, sources(≤20), last_check, check_state}} | `plugins/myssia-credhunter/credhunter/keystore.py:94-99`(结构)、`:78-86`(路径解析:MYIA_HOME env > cwd) |
| credcheck 读库验证回填:只回填 check_state/last_check(余额探测结果只进返回 payload,**不持久**) | `plugins/myssia-credhunter/adapter.py:531`(`run_credcheck_keystore`)、`keystore.py:153-169`(`update_check`) |
| Q9 掩码函数(前 8 后 4;长度 9-12 只前 8+省略号;≤8 只前 2+省略号)与指纹(sha256 前 16 hex) | `plugins/myssia-credhunter/credhunter/findings.py:54-66` |
| credcheck 三态词表:final_verified / rejected(401/403 判死)/ transient(429/5xx) | `plugins/myssia-credhunter/credhunter/credcheck.py:14-16`;行为规格 `archive/2026-10/10-03-aipocket-fusion/research/behavior-specs/credcheck.md` |
| 桌面 job 通道先例(run.start/status/cancel,V2 复用) | `desktop/entry.py:7126-7128` |
| secrets 契约「值永不可读」(本屏同向纪律) | `desktop/entry.py:1975-1976`、`desktop/ui-src/src/lib/api/types.ts:695-698` |
| 屏挂载三件套先例(App 路由/侧栏/命令面板) | `desktop/ui-src/src/App.tsx:65`(bot-credentials 例)、`components/layout/sidebar.tsx:68`、`components/layout/command-palette.tsx:50`;屏族现 12 目录(`ls desktop/ui-src/src/screens/`) |
| 列宽 headless 引擎已在依赖,零新增包 | `desktop/ui-src/package.json:22`(`@tanstack/react-table ^8.21.3`) |
| MYIA_HOME 注入链:壳 spawn sidecar 注入 env(`desktop/src-tauri/src/main.rs:319-320`)→ `_self_command` 子进程继承(`desktop/entry.py:3470`)→ sidecar 与 CLI 子进程同数据根,**keystore 路径两侧天然一致** | 如左引 |
| 本机真实数据(冒烟素材):仓库根密钥库 1 条 xai 记录,hit_count=1763,check_state=None(未验证是真实常态) | 2026-10-14 实查 `credhunter-keystore.json`(425 bytes,version=1) |

## 2. 硬约束(不可协商)

1. **AGPL 双雷**:对标对象 aipocket 与生态参照 new-api 均为 AGPL-3.0(MYIA=MIT,无再授权通道;判例 `archive/2026-10/10-03-aipocket-fusion/prd.md:20`)。只借**行为与布局思想**(列模型/过滤工具条/徽章分层/列宽持久化),零代码、零上游标识符、零上游文案;状态徽章文案按 MYIA 自家三态词表用人话重造。GitHub API 许可徽章显 NOASSERTION 是假象,以 LICENSE 文件为准——凡引许可证处禁止按「无许可」放松红线。
2. **G11 三不借(红线,永久不做,不止 V1)**:
   - **导出**:任何形式的密钥/记录导出(json/csv/剪贴板打包)不做——census 拍板 `archive/2026-10/10-04-fe-gap-census/research/matrix.md:86`(「G11 凭据导出|关闭(红线不做)」);
   - **全文 reveal / 复制**:违背 Q9 与 secrets 契约「值永不可读」(`desktop/entry.py:1975-1976`),不做;
   - **拿猎得键实测对话**(上游 chat-test 形态)= 滥用发现凭据,插件授权定位明拒(`plugins/myssia-credhunter/README.md` 授权定位节「不滥用任何发现的凭据」),不做。
3. **掩码-only 出协议**:sidecar 应答只含服务端算好的 `masked_apikey`,全文 `apikey` 字段在 handler 投影时丢弃;协议流、日志、UI、localStorage 零全文密钥(测试断言)。掩码规则逐字镜像 `findings.py:54-66`(含短键退化)。
4. **零网络**:V1 唯一新协议方法是纯文件读;不做任何探测触发(余额/验证触发属 V2,须走 job 通道——串行限速 RPM≤30/间隔 2s 决不能同步等)。
5. **UI 并入既有屏族版式**:新增 screens 目录 + 侧栏/命令面板条目,不新造画布;文案全人话零生造词;命名直白扁平。

## 3. Requirements(V1 只读,零歧义规格)

### 3.1 协议:新方法 `credhunter.keys.list`(纯加法)

- **注册**:`desktop/entry.py` 新增 `_m_credhunter_keys_list` 并入 `_HANDLERS`(`:7115`);纯加法不 bump `PROTOCOL_VERSION`(判例:六域接线批 `entry.py:7179-7180` 注)。同步 `.trellis/spec/desktop/sidecar-protocol.md` 方法注册表(本批开工实值 95 行,+1 → 96 对账;PRD 初稿「93 行」为写作时点值,proxy-pool-panel 批先行合入后漂移)。
- **参数**:`{}`(空参)。
- **行为**:读密钥库文件(纯读,零网络),路径解析**镜像** `keystore.default_keystore_path`(`keystore.py:78-86`:MYIA_HOME env > cwd;entry.py 不 import 插件代码——插件动态加载,内联这两行规则并在 handler docstring 互指 keystore.py;测试经 MYIA_HOME env 逐例注入,同 `_serve_context` 惯例 `entry.py:633`)。
- **应答形状**(冻结):

```json
{
  "path": "<库文件绝对路径>",
  "exists": true,
  "version": 1,
  "count": 1,
  "records": [
    {
      "fingerprint": "sha256-xxxxxxxxxxxxxxxx",
      "masked_apikey": "前8…后4",
      "provider": "xai",
      "first_seen": "ISO", "last_seen": "ISO",
      "hit_count": 1763,
      "sources": ["https://github.com/o/r/blob/…"],
      "last_check": null,
      "check_state": null
    }
  ]
}
```

  - `records` 按 `last_seen` 新→旧排序;`sources` 原样透传(库内已去重上限 20);**无 `apikey` 键**。
  - 库文件不存在:`` `{"path": …, "exists": false, "version": null, "count": 0, "records": []}` `` ——合法未建库态,不报错不建文件(handler 纯读,绝不触发 Keystore 构造建档)。
  - 库损坏/版本不符/不可读:结构化错透传 keystore 错误族 code(`keystore_invalid` / `keystore_unreadable`,`keystore.py:60-75` 同名),进 `ProtocolError`。
- **前端类型**:`desktop/ui-src/src/lib/api/types.ts` 加 `CredhunterKeysListResult` / `CredhunterKeyRecord` + `SidecarProtocol` 映射行(`types.ts:1375-1429`)。

### 3.2 屏:新增 `screens/credhunter/`(挂载三件套)

- **路由**:`App.tsx` 加 `<Route path="credhunter" …>`;**侧栏** `sidebar.tsx` 条目「凭证猎手」;**命令面板** `command-palette.tsx` 条目(label「凭证猎手」,keywords:`credhunter 凭证 密钥 高危 leaked keys`)。
- **文件**:`credhunter-screen.tsx`(本体)+ `api.ts`(屏私有薄封装:方法调用、高危判据常量、状态词表映射;先例 `screens/feed/api.ts`)+ `credhunter-screen.test.tsx`。
- **版式**:并入屏族既有 Card/Badge/Button 组件族(`@/components/ui/*`,参照 `bot-credentials-screen.tsx:19-23` 引法),头部视图切换 + 表格主体。

### 3.3 视图与列模型(对标 AllKeysPage/HighValuePage 的 MYIA 化)

**视图切换(单屏两视图,Segment/Tabs,不做第二路由)**:

1. **全部密钥**(缺省):全量 records。
2. **高危**:过滤 `check_state === "final_verified"`(已验证存活 = 泄漏且有效,最高活险;rejected 已判死、transient 未定不入选)。判据常量 `HIGH_RISK_STATES` 集中在 `api.ts` 一处,V2 调整(余额阈值/hit_count 组合)只动这里。

**六列**(列名直白,列宽可拖拽,`@tanstack/react-table` headless 引擎,持久化 localStorage key `credhunter.key-table-columns.v1`):

| 列 | 数据源 | 说明 |
|---|---|---|
| 密钥 | masked_apikey | 副行/tooltip 显 fingerprint;**无任何复制/查看动作** |
| 供应商 | provider | 文本徽章(品牌配色属打磨,V1 不做) |
| 验证状态 | check_state | 徽章四态,词表见下 |
| 命中 | hit_count | 副行显 first_seen/last_seen |
| 证据 | sources.length | 行展开处列 URL 明细 |
| 最近检查 | last_check | null 显「未验证」 |

**状态徽章词表**(MYIA 自家三态 + 未验证,文案人话,变体分层思想来自上游但词面自造):

| check_state | 文案 | 徽章变体 |
|---|---|---|
| final_verified | 已验证存活 | success |
| rejected | 已判死 | danger |
| transient | 暂不可判 | warning |
| null | 未验证 | muted |

**工具条**:掩码域子串搜索(masked_apikey+provider 匹配)、供应商过滤 chips(当前记录聚合计数)、排序切换(hit_count 高→低缺省 / last_seen 新→旧)。**无余额列、无余额排序**——数据面不存在持久余额(见 §5 缺口),不做假列。

**行展开**:sources URL 全列表(≤20)+ fingerprint + first_seen/last_check 完整时刻。

**空态**(三态都要,文案人话):
- 库未建(exists=false):「凭证猎手还没有密钥库——猎手(credhunt)尚未运行或尚无命中。可在品类 YAML 启用 engine: credhunter 源后跑一轮采集」;
- 库在但高危视图空:「没有已验证存活的泄漏凭证」;
- 过滤无命中:常规「无匹配结果」。

### 3.4 测试

- **entry.py 单测**(`_m_credhunter_keys_list`):①exists=false 空态应答形状;②正常投影——**断言应答 JSON 序列化文本不含库内全文 apikey**、掩码前 8 后 4、last_seen 排序、sources 透传;③版本不符 → `keystore_invalid`;④短键(≤8 / 9-12)掩码退化逐字镜像 `findings.py:54-66`。
- **屏测试**:fixture 渲染六列、视图切换过滤高危、provider chips 过滤、搜索、exists=false 空态文案、列宽写读 localStorage(mock)。

## 4. Acceptance Criteria

- [x] `credhunter.keys.list` 注册进 `_HANDLERS`,空参调用返回 §3.1 冻结形状;应答任何路径下无全文 apikey(单测断言序列化全文不含)
- [x] exists=false 空态 + keystore_invalid/keystore_unreadable 结构化错三路径全测
- [x] 屏挂载三件套齐:路由 /credhunter、侧栏「凭证猎手」、命令面板条目
- [x] 六列表格 + 视图切换(全部/高危,判据 final_verified)+ 搜索 + provider chips + 排序 + 行展开证据,全部有测试
- [x] 状态徽章四态词表渲染正确(final_verified/rejected/transient/null)
- [x] 列宽拖拽持久化 localStorage(`credhunter.key-table-columns.v1`),刷新还原
- [x] `types.ts` SidecarProtocol 映射 + `.trellis/spec/desktop/sidecar-protocol.md` 注册表 +1 对账一致
- [x] 全程零新增网络调用、零新增 npm 依赖、零协议版本 bump

## 5. V2 及以后(本任务不做,拆后续任务)

| 项 | 依赖/说明 |
|---|---|
| 验证/余额探测触发 | 新 `credhunter.check.start/status/cancel` 三方法,镜像 run.* job 协议(`entry.py:7126-7128` 形态);串行限速(RPM≤30/间隔 2s)必须异步 job |
| 余额列 | 前置 = keystore 结构升级 v2 增 balance/tier 字段并回填(现为 v1 固定,`keystore.py:51`;探测结果只进 payload,`adapter.py:531`);升版须拍 version≠1 的兼容决策 |
| 人工状态流转 | check_state 人工复核闭环(对上游 transition 形态,词表按 MYIA 自家) |
| 高危判据增强 | 余额阈值/hit_count 组合(产品决策,V1 缺省已定且只动 `api.ts` 常量) |
| 蜜罐/suspicious 维度 | 远期参照,无数据面 |
| 导出/reveal/chat-test | **永久不做**(§2 G11 三不借) |

## 6. 拷问预答

- **Q 为何只读?** 余额批查是串行限速长任务,同步必超时,job 通道是独立后端工作量;且 keystore v1 无余额持久层,交互版绑不开数据升级。先窄后宽是主人 V1 形态令。
- **Q 对标 aipocket 却无余额列?** MYIA 数据面无持久余额(`adapter.py:531` 回填仅 check_state/last_check);做恒「未探测」假列违反如实纪律,余额列随 V2 keystore v2 一起落。
- **Q 高危判据凭什么?** 泄漏凭证最高活险 = 验证存活;判据单点常量可调,余额维度是 V2 产品决策。
- **Q 全文密钥会不会经面板泄漏?** 读与掩码都在服务端,协议流只有掩码;secrets 契约「值永不可读」同向;库本机 600。测试有「序列化不含全文」断言。
- **Q AGPL?** 只借行为/布局思想,零码零标识符零文案;判例在案(aipocket-fusion 已全名清除上游标识符)。

## Notes

- 设计/执行阶段如需行为规格佐证,读 `archive/2026-10/10-03-aipocket-fusion/research/behavior-specs/credcheck.md`(三态语义权威);上游 repo(james-6-23/aipocket)仅作 GitHub 文件级只读参照,本地副本已删。

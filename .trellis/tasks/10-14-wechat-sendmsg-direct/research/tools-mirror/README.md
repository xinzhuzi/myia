# tools/ — Phase 0 工具整备(v2.1,grill R2 六条落实后,门 1 绿)

固化来源:`/tmp/blscan.py`、`/tmp/refscan3.py`(→ 本目录,CLI 化+模块化,/tmp 不可信判例);
`cap.py` = 上级目录 v1(并行会话遗产,原样保留)的堆扫升级版;`fstarts.py`/`attribute.py` 新增。
全部离线干跑自验通过(`test_offline.py`,23/23,零微信零发送零 attach)。

## grill R2 修订摘要(v2 → v2.1)

1. **区间源:活体枚举优先**(S10 勘误):本机 lldb-1703 有零参 `SBProcess.GetMemoryRegions()`
   (attach 态亲证 39/60 可读数据区;launch 停 main 态返回空=按不可用回退),vmmap 快照降为
   回退源(快照滞后=hit 时新增堆区漏扫)。
2. **判据分级防烧窗**:HIT_PROBES=「嘻嘻」(utf8/utf16)=唯一烧窗判据;AUX_PROBES=「filehelper」
   只记 weak 取证件(每窗一份),窗不烧、断点保持使能——防堆内陈旧 filehelper 串烧掉主人
   唯一手发窗(S1 同型)。
3. **窗口 TTL**:arm(timeout_s=30) 默认 30s 噪声界;过期后首个命中=关窗+禁断点+零扫堆
   (防全堆扫反复冻结微信)。
4. 扫描去重(块尾重叠区同 label 同地址只计一次);attribute.py 函数表边界 None=rc=3 干净退出;
   fstarts 起点数勘误为 387,126(load() 去重后,干跑在案)。

## 清单

| 脚本 | 作用 | 干跑证据 |
|---|---|---|
| `cap.py` | LLDB 断点捕获枪 v2.1:窗口开关(默认关)+TTL → 线程名过滤(coroutine/mars::stn)→ 帧捕获(异常保帧)→ 区间源(活体枚举优先/vmmap 回退)→ 堆扫(ReadMemory 4MB 分块+探针级重叠+去重+双探针分级)→ primary 命中=写 hit+自关窗+自禁断点+自继续;仅 aux=weak 不烧窗 | A1-A12 |
| `fstarts.py` | 薄片 LC_FUNCTION_STARTS 反查:VA→所属函数(start,end)。387,126 起点(去重后;符号表已剥光,这是唯一函数边界源) | C0/C1 |
| `blscan.py` | BL 直调扫描:`--callers-of 0xVA`(可多次)/`--all-index` 全量索引 | B1/B2:与 /tmp 版产物逐点等价(0x5e1d050=27743;0x490fb20=0 不翻案) |
| `refscan3.py` | 页级 ADRP 取址扫描(S3 铁律:只页级) | B3/B4:五默认页等价;xkey 校准页 826≠0 |
| `attribute.py` | 归因链:hit 文件 → lr−slide=VA → 薄片反查调用者 → blscan 上游 → BT 帧附带映射;slide 缺失/VA 越界/函数表边界=rc≠0 干净退出绝不猜 | C1-C4 |
| `test_offline.py` | 全离线干跑(假 lldb 对象+真薄片+真样例 vmmap+活体枚举假形态);日志→ `../dryrun/phase0-dryrun.log` | 23 PASS |
| `samples/vmmap.sample.txt` | 10-14 真机 vmmap 快照拷贝(回退源解析器奇偶用例;A1:124 区间/241MB) | A1 |

## Phase 1 使用(design Step1-2 run-sheet 对接)

1. **真机冒烟(升格为首步,not-run 声明在案)**:on_hit 回调全路径在真 attach 态(真
   SBFrame/SBError/微信进程 ReadMemory)从未执行过——首次实战前必须:attach → 禁用态布防
   (`command script import cap.py` + `breakpoint command add -F cap.on_hit` + `breakpoint disable`)
   → 立即 `bp SetEnabled(False)` + `detach`,验证 attach 链路通且零异常。
2. **落位**:hit/weak/日志→`<勘察>/hits/`;回退区间表→`<勘察>/hits/vmmap.txt`(仅当活体枚举
   不可用时才需要;run-sheet ③ 照做留作保险)。
3. **布防(禁用态)**:`breakpoint set -a S+0x5e1d050`、`S+0x5e1d680`,disable,挂 `cap.on_hit`。
4. **窗口使能**:主人说「发」→ 3s 内会话内 `script import cap; cap.arm()`(默认 TTL 30s)→ 断点 enable。
5. **触发**:主人手发「嘻嘻」到文件传输助手(标准形态,零预算);hit 落 `hits/hit_*.txt`
   (primary=嘻嘻 命中即自禁断点自关窗);`weak_*.txt`=陈旧串可能,窗未烧继续等。
6. **收枪**:回调已自禁断点自关窗;会话侧再 `bp SetEnabled(False)` + `detach`(双保险纪律)。
7. **离线归因**:`python3 attribute.py --hit hits/hit_*.txt --slide 0x<S>`
   (slide 取法:`image list -o -f | rg wechat.dylib`)→ `attribution/attr_*.{json,txt}`;
   对 caller/upstream 函数入口跑 DecompileTargets 全函数反编译。
8. **阴性对照(建议步)**:arm 后不发送,观察首个协程命中是否触发 weak/miss——filehelper
   堆内驻留形态取证,辅助判读 weak 含义。

## 已知边界(干跑实测)

- 活体枚举失败/返回空(launch 停 main 态亲测形态)→ 回退 vmmap 快照;快照滞后=hit 时新增
  堆区不扫(hit 文件 `regions_source` 字段标明实际来源)。
- vmmap 快照与活进程不一致的区间 → ReadMemory 失败按块跳过并计数(`failed: N`),不中断(A4)。
- 探针横跨 4MB 块边界由重叠回退兜住;重叠区双命中去重(A5a/A5b)。
- 仅 aux(filehelper)命中=陈旧串可能:weak 取证件(每窗一份),窗保持开等 primary(A11);
  双探皆无=窗口错失或过滤过狠:miss 记账,重开窗口再来,勿换弱先验常量(A6)。
- 窗口 TTL 过期:关窗+禁断点+零扫堆(A12);重开须重新 `arm()+enable`。
- 任何异常/两区间源皆无:关窗+禁断点+异常取证件(含已捕获帧)落盘(A7/A8,uncertain-never-retry)。

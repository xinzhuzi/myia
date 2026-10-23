# 当前版本业务字段映射核验（进行中）

> 账号安全停止约束优先：本文件中历史观察窗口计划已失效，全部既有授权已消费。后续仅离线分析，不恢复微信操作或要求用户测试；见 `account-safety-stop-20261016.md`。

## 独立于历史协议的定位方法

仅从现有源码 `plugins/wechat-bridge/wechat_bridge/localdb_query.py:17` 已确证的实际列名出发，扫描冻结ARM64薄片的精确NUL字面量，然后查询留存Ghidra工程的xref；不读取真实数据库/聊天正文/密钥，不调用微信。

`message_content` 仅出现于 `0x98539cf`，唯一参数xref是 `0x4cc2828`，所属函数 `0x4cc245c`；`real_sender_id` 唯一xref和 `local_type` 的一条xref也落该函数。见 `text-contract-pass115/callback-seeds.tsv`。

## 当前已得到的静态绑定证据

`text-contract-pass116/native-fn-4cc245c.c/.asm`：此函数为一个binding注册成员名、offset和各自类型访问器，调用同一 `0x56f9b9c`。注册表由 `0x4cbaf80` 的guard/call_once初始化，存于 `0xa4ad950`。pass118保留了注册函数，确认offset作为键、字段名和成员访问器共同写入注册项，另将访问器送入字段构造。

| 注册名（原始字面量） | 成员offset | 与发送生产者的关系 |
| --- | --- | --- |
| local_id | 0xf4 | 当前发送wire未使用 |
| server_id | 0xf8 | 发送生产者将响应条目+0x28写至该offset |
| local_type | 0x108 | 还须证明与发送条目field3读取record+0xc的关系 |
| sort_seq | 0x100 | 当前发送wire未使用 |
| real_sender_id | 0x110 | 当前发送wire未使用 |
| create_time | 0x114 | 两个已留存生产者均将record+0x114写入条目field4 |
| source | 0x160 | 两个生产者将非空record+0x160写入条目field6 |
| message_content | 0x130 | 两个生产者将record+0x130写入条目field2 |
| compress_content | 0x148 | 当前发送wire未使用 |

这提供了正文/时间/source/server_id的同offset证据；仍须核验成员访问器如何应用offset，以及该binding与发送record属于同一类型的直接关联，才能把业务输入映射写成可执行合同。不能仅凭offset相同就放行。

## 已排除的误读

- `0x4bb6cd4` 只检查传入string是否包含原始字面量 `_weclaw`，并不提供收件人字段名证明（pass114）。
- `0x4a2eed8` 读record+0x108再尾调 `0x6a3d4`，而后者直接返回1（pass118）；不得将这个调用臆解为消息type转换。
- `0x4cbe440` 通过 `0x4d310bc` 等helper把参数变成string；当前仍未据此确定客户端标识的输入语义。
- `create_time` 在精确字符串扫描的位置可能是另一更长字符串的后缀，裸偏移无xref不构成负向结论；绑定函数中已直接出现完整列名，不再围绕该后缀扩大扫描。

## 下一步

核验binding访问器及record类型的关联；收件人record+0x30、条目field3的record+0xc及客户端标识生成仍开放。调度/排空及真发送授权边界不变。

## 成员访问器后续核验

pass119虚表 `0x9eb0770` 的精确槽值在pass121逐项导出：写入 `0x4cc2e80` 使用 `record + *(accessor+8)`，读取 `0x4cc2e90` 使用同样的相加规则。它们证明绑定offset是对象内成员字节offset，当前仍需绑定与发送record同类型的直接关联。pass120有两处未从精确槽值取出的地址录入，虽然工具找到了所属函数，**此批不作为语义依据**；pass121以明确槽值重新导出。

pass122的 `0x4cc16e4` 使用同一binding逐个查询offset并构造字段列表；其调用者pass123 `0x3022764` 具有数据库结果循环，调用 `0x3025388` 构造记录；仅定点读了该循环，未把大型导出的其他分支纳入结论。

pass124 `0x3025388`：结果行构造先复制冻结模板 `0x88a1320`（0x278字节），调用 `0xac6038`，随后遍历binding字段并通过各访问器vslot+0x28将列值写入同一record。pass126构造器为其写入虚表 `0x9eb04f0`。

pass125 `0x4cbf804` 将record+0x108的64位值复制到record+0xc；pass126 `0x4cbc3ac` 又可把+0xc复制回+0x108。后者还经record+0x220虚表调用更新派生数据。此证据建立local_type持久字段与+0xc缓存的关系；条目field3读取的是该缓存低32位，仍需同类型关联和文本输入取值的独立验证。

pass130发现发送生产者用于日志的 `0x4cbe440 -> 0x4d310bc` 也读取同一record的+0xf4(local_id)、+0x114(create_time)、+0x100(sort_seq)，并从+0x260复制string。它先调用 `0x4cbd624(record)` 返回另一个string，下一步核验该getter。pass130的 `0x4cbb054` 构造器写同一虚表 `0x9eb04f0` 并在尾部调用 `0x4cbc3ac`。

`text-contract-byte-verification-v7.json` 覆盖至pass130：208份导出（含重复）33382指令/133528字节均匹配；consumer另487条匹配。数据虚表slot/业务语义不是指令字节验证的替代物。

pass131 `0x4cbd624`：普通记录根据 `0x4cbd748(record)` 返回record+0x30或+0x18；类型10000还会和账号vslot+0x28返回string比较。它提供会话选择逻辑的明确下一跳，但当前不能仅凭比较方式断定发送方向。pass130的接收记录构造器直接从输入嵌套wrapper +0x18赋值record+0x30，输入+8赋值record+0x18；需后续核验输入protobuf的真实类型和来源。

截至本切片，业务映射尚不写入产品JSON；后续优先目标为0x4cbd748、binding类型关联及客户端标识时间/账号来源。该研究未触及活进程。

## pass132：方向比较与类型赋值的精确边界

`text-contract-pass132/native-fn-4cbd748.c/.asm`：type缓存低32位不等于10000且record+0x18字符串非空时，取得`0x4669774`返回的账号对象，调用其vslot+0x28，并按string长度与逐字节内容比较；返回相等结果。结合pass131，只能确认`0x4cbd624`据此在record+0x30与+0x18之间选择，尚不能把两个字符串直接定名为发件人/收件人。账号该虚槽的返回语义和生产者同类型关联仍需继续核验。

`text-contract-pass132/native-fn-4cbbd20.c/.asm`：末段先将第二参数低32位写入record+0xc，再从+0xc读64位写入+0x108；因此不能把该setter表述为第二参数完整64位直接赋给local_type。随后更新派生对象并确保+0x230的共享对象存在；本批不证明文本消息的具体类型取值。

`text-contract-byte-verification-v9.json`覆盖至pass132：211份函数导出（含重复）、33891条指令、135564字节与冻结薄片一致，完整consumer另487条一致。未附加、未调用微信、未发送、未修改产品JSON；离线测试结果仍引用既有`newsendmsg-integrated-verification.json`，本批没有重跑或扩大测试结论。

后续顺序：补业务输入与同类型证据→核验调度线程、超时和取消排空→完成限时实验及清理资格→明确收件人/正文并取得新的单次授权→真实发送与独立送达核验→产品接线和两入口安装。两次既有只读授权均已消费，不能用于这条实验链。

## pass133～141与下一次证据获取方式

账号vslot+0x28精确指向`0x4670680`（pass81/pass133），继续经账号vslot+0x68的`0x466a2fc`取得account+0x68/+0x70的shared对象，再调用该对象vslot+0x18；当前尚未证明该子对象实际类型及返回string的业务名称。不得把这一间接getter直接写成账号标识读取配方。

pass138的`0x4cbcb04`构造器写入同一record虚表`0x9eb04f0`，从输入+0xf0/+0x108赋record+0x18/+0x30，从输入+0x18赋正文+0x130，输入+0x10赋时间+0x114，输入+0x34经`0x4cbbd20`赋type；输入类型及到发送生产者的完整关联仍开放。另导出的`0x4c89510`明确设type=0x31，属于其他分支，不能用于证明文本type。

pass136/137定位`0x30bda14`位于虚表`0x9de7f68`，pass139的两个共享工厂均将该虚表写入所建对象，基础构造器`0x3065454`保留两个弱引用（pass140）。这些是工厂/注册链证据，不是完整record输入的证明。pass140大函数`0x30e3fb0`只定点读取注册`0x30eccc4`的片段，不对其余分支作结论。

为了直接核验普通文本发送的字段与运行线程，本轮准备了`newsendmsg-factory-window-plan.md`及单次只读观察器；用户确认测试为文件传输助手/“今天真是个好日子”，尚未授予新附加窗口。读取器的布局来源为`0x465da58`重复表/+0x10 count、`0x465d024`条目字段，以及pass141两个精确构造器`0x465bd88`/`0x4f33c00`的虚表。pass141后者与pass72重复，仅用于定点复核；不算独立语义证据。

`text-contract-byte-verification-v11.json`覆盖至pass141：222份导出（含重复）、37544条指令/150176字节匹配，完整consumer另487条匹配。新增观察准备、75项Python/122 subtests和10项真实LLDB自有夹具清理证据见`factory-observer-preparation.json`。本批仍无微信附加、原生调用、发送或产品JSON接线。

## pass155：客户端标识输入来源

已核验 `0x30f2168` 的非空缓存复用、对象+0x18的record来源、记录标识格式化链、固定后缀原始字节与64位计数器原值消费顺序；时间来自record+0x114，local_id来自+0xf4，local_id为零且+0x260非空时直接采用该string。合同补入研究JSON字段5，未修改产品配方。定点6份导出769指令、19个关键位置、后缀及thunk分支核验通过，见 `newsendmsg-client-id-source-result.md` 和 `newsendmsg-client-id-source-verification.json`。计数器初始化/并发序列化、记录方向、文本type及真实client-ID仍未证明；不恢复活体验证，A7未完成。

## pass156～159：构造侧记录类型和local_type两半

context构造器`0x30ef9e0`将`0x30efce4`生成的shared record存入+0x18/+0x20；factory调用`0xac6038`写同一record虚表`0x9eb04f0`。完整构造到producer派发链仍缺。新setter`0x4cbcfd4`写record+0x10高32位，再把+0xc完整64位同步到local_type/+0x108；`0x4cbbd20`负责+0xc低32位，field3只读低半。factory从输入对象vslot+0x10/+0x18分别取这两个值。另见低半写1分支，但未证明是普通文本入口，不据此定值。13份导出4903指令、21位置及新脚本Ruff通过，详见`newsendmsg-record-input-result.md`、对应合同与验证JSON。未操作微信，不启用产品配方，A7未完成。

## pass160～166：输入对象类型getter

两条context输入构造分支的payload虚表`0x9eb26a0`/`0x9eb2918`均经+0x10槽读取payload+0xe4低半，经+0x18槽读取+0xe8高半；+0x20槽恒返回1属于另一字段。精确常量证明这两条分支分别设低/高值49/1及49/51，高半1不能当作普通文本type证据。22份导出5576指令、11关键位置、2组常量和6槽dyld链核验通过，见`newsendmsg-input-type-result.md`及其合同/验证JSON。普通文本type和完整派发仍未证明，A7未完成；账号安全停止约束保持。

## pass167～173：类型1正文转换切片

基础构造器的+0xe4/+0xe8均初始化为零；新转换器真实入口`0x4c6eff4`明确写低类型1，将source+0x130/+0x148字符串复制到新payload+0x5c8/+0x5e0。工厂`0x4c6f204`经`0x4c6f2c4`构建payload虚表`0x9eb2bb8`，两层均使用隐藏x8返回shared pair；不得把内部地址`0x4c6f030`当作函数入口。公共helper`0x4c6c5d0`另复制source+0x350至payload+0x178，设payload+0x7c=2，业务含义未定且不属于低类型字段。

这是类型1与先前正文绑定偏移一致的直接转换证据，仍未证明完整普通文本发送链中的source同类型身份、转换器所属对象及到producer的派发。6份定点导出232指令、32关键位置及4个dyld链槽核验通过，新验证器和模式扫描脚本Ruff通过；详见`newsendmsg-type-one-content-result.md`与对应合同/验证JSON。本切片没有运行或操作微信，产品配方保持拒绝，A7未完成；账号安全停止约束优先于前文历史观察建议。

## pass174～182：转换器归属与对象身份边界

追到`0x4c876bc`选择函数后，确认上一写1方法`0x4c6eff4`位于选择值49/115所建对象`0x9eacf38`的+0x18槽；当前选择函数实际调用+0x10槽，不能由输出1倒推普通文本输入。数值1经`0x4c8cbe0 -> 0x4c8cd0c`构造虚表`0x9ead718`，+0x10/0x18分别为`0x4c7fbc0`/`0x4c7ffa4`。公共工厂`0x4c6b5b8`的实际输出虚表`0x9eba160`与此前数据库record的`0x9eb04f0`不同；不得把同偏移+0x130/+0x148直接套作相同数据库字段。

数值1的复制分支还受`0x48a60b4`精确16字节`announcement@all`谓词控制；false时复制source+0xb8至转换结果+0x148，true时另走转换，业务含义未定。10份精确导出2061指令、39关键位置、4个dyld链槽及比较常量核验，新脚本Ruff通过；详见`newsendmsg-conversion-dispatch-result.md`及合同/验证JSON。下一证据缺口为到已证明发送context的正向关联，不能继续依同偏移推定；A7未完成，账号安全停止保持，无微信操作或产品接线。

## pass183～192：发送context的正向队列链

从`0x317df64`构造已知context出发，确认其将input+0x90字符串放入context+0x38并用作队列key，按shared context入队、筛选+b4状态、移除及放入另一队列后构建异步回调；key方向尚未定名。正文functor`0x9def270`捕获context shared pair和service/key，invoke`0x322274c`经`0x31d15fc`继续，另一回调还有下一层提交，不能据阶段结果推定排空。

后续handler选择经输入三个虚槽、数值映射和名称查找；实际注册身份仍缺。`0x30d58e0`调用handler+0x90；对已知表`0x9de7f68`该槽是仅日志/构造0/0结果的`0x30d8538`，producer`0x30bda14`位于+0xd8，是不同阶段。较早准备函数`0x31cf3a4`和到producer的派发尚未全通，不据此断言整条链从未发送。9450条导出指令、54关键位置、4槽dyld链及构造thunk核验，新脚本Ruff通过；详见`newsendmsg-forward-queue-result.md`和合同/验证JSON。无微信操作、产品接线或装机，A7未完成，账号安全停止保持。

## pass193～199：状态3阶段和准确虚表身份

`0x31ce06c`在先前结果两个字为零、context flag低位为1、所选handler非空后设状态3并调用`0x30d4354`；真实参数为x0/handler、x1/context shared pair地址、隐藏x8/result。kind1依据input+0xd8字节选handler+0x80或+0x88，此成员偏移不能与handler的producer虚槽+0xd8混淆。已知表+0x88=`0x303fdf0`，仅保留临时shared pair并重定向+0x80=`0x30d82d8`，后者构造0/0结果。

独立dyld解码还确认该表+0x78=`0x30bcd9c`，此前pass195导出的`0x30d7958`不属于这一槽，不能用于解释该表的准备行为。状态3后的两条通知进一步进入`0x30d00d0(handler+0x18,record)`和`0x30d0a14(handler+0x90,flags,record)`；这些容器的实际目标尚缺，所选handler及到producer仍未全通。13份导出8891指令、39关键位置、5槽及重定向x8保留核验，新脚本Ruff通过，见`newsendmsg-state-three-result.md`及合同/验证JSON。下一步仅离线核验通知目标与注册身份；没有微信操作或产品接线，A7未完成，账号安全停止保持。

## pass200～205：文本handler身份与正文准备

注册名称的冻结字节核验确认此前`0x9de7f68`为LocationMessageHandler；`0x30e74f4`提供精确TextMessageHandler名称，经`0x30e7aa0`生成`0x9de9a68`并注册，初始化调用者把数值1与该名称交给映射helper。文本表+0x78=`0x3105a98`，专门输入分支将+0x5c8正文复制至context record+0x130；+0xd8=`0x3107b0c`读取该正文、+0xc类型、+0x114时间和客户端标识构建条目，经共用`0x30bee20`请求。field1由`0x30f1d74`提供，含普通+0x30后备与特殊嵌套分支，方向未完全定名。

两条通知为signalslot容器：直接调用或复制record并转交executor；实际订阅者仍缺。19份导出7494指令、66关键位置、9槽及两个精确名称核验，新脚本Ruff通过；见`newsendmsg-text-handler-result.md`及合同/验证JSON。新证据改变下一步：优先证明service数值/名称表到文本对象及producer的完整派发，不再把Location业务输入套入文本。输入RTTI、方向、线程/config/排空及独立回执仍开放；没有微信操作/产品接线，A7未完成，账号安全停止保持。

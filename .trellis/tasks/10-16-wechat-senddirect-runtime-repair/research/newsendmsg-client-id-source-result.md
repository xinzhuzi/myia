# 4.1.15 客户端标识输入链离线核验

## 范围

仅留存 ARM64 薄片及只读 Ghidra 工程；不运行、附加、操作微信，不调用原生函数或发送。账号安全停止约束继续有效。本切片补充研究 JSON 的字段5输入合同，不能启用产品配方。

## 已观察的静态事实

- `text-contract-pass77/native-fn-30f2168.asm:7` 起将 x0 保存在 x20、隐藏返回区 x8 保存在 x19；对象+0xb8 是24字节 string 缓存。缓存非空直接复制返回，不重新消费计数值。输入是持有记录的生产对象，不能把 record 指针直接传入此函数。
- `0x30f2234` 从对象+0x18取 record。非空分支调用 `0x4cbe440(record)`，把其返回 string 放进 ostream，再追加固定后缀和计数器原值。无 record 分支仅输出计数器原值。
- 后缀初始化在 `0x30f2288` 从精确地址 `0x88b02f8` 复制8字节 `5f78776563686174`，再附加 underscore，得到 `_xwechat_`。Ghidra 的相邻字符串标签不能代替精确取址；这里没有按标签名猜作 `sending_`。
- `0x30f22c4..0x30f22d0` 及无 record 分支 `0x30f245c..0x30f246c` 都先将全局 `0xa05a2b8` 原来的64位值装入 x1，再用另一寄存器加一并写回；ostream接收的是原值。不能按反编译文本中赋值顺序误用加一后的值。
- `0x30f247c` 取得 stream 内容，`0x30f2498..0x30f24a4` 转入对象+0xb8缓存。`pass155/0x3b1afc` 是长度明确的 ostream string 写入；`0x5f96e3c` 从 stream buffer 复制 string，未在这两步引入新的业务标识。

## 记录标识的来源

`text-contract-pass114/native-fn-4cbe440.asm` 构造临时标识对象后转交 `0x8ad29c`。冻结指令 `0x4d31170` 的直接分支独立解码目标为 `0x4d310bc`，与既有 thunk 声明相符。

`pass130/0x4d310bc` 将 `0x4cbd624(record)` 选出的 string、record+0x114 的32位 create_time、record+0xf4 的32位 local_id、record+0x100 的64位值及 record+0x260 的 string 复制到临时对象。

`pass155/0x8ad29c` 对该临时对象的真实选择是：

1. local_id 为0且 record+0x260 的 string 非空时，直接返回该 string。
2. 其他情况，将选出的 string、underscore、`std::to_string(uint32 create_time)`、underscore、`std::to_string(uint32 local_id)`连接。复制进来的64位 record+0x100 在这个格式化函数中没有被读取。

因此时间和记录标识的来源已定位，但 `0x4cbd624` 所选 string 的账号业务名称仍未证明；不能把它改名为已确认的发送者或收件人。

## 本轮验证及未完成项

`newsendmsg-client-id-source-verification.json`：6份定点导出769条指令与完整哈希匹配的冻结薄片一致，19个关键指令位置、后缀原始字节及 record thunk 目标检查通过；新验证脚本 Ruff 通过。3份新增导出见 `text-contract-pass155/`，Ghidra退出0、readOnly/noanalysis、未附加。

这证明静态来源，不证明全局计数器的初始化、跨线程序列化、唯一性或当前运行值；也未观察实际客户端ID。无 record 分支不是可擅自替换正常 producer 的兜底。运行时不使用本机另起的计数器或自造时间替代原生状态。

仍缺收件人方向、普通文本 type、完整 producer/record 同类型关联、调度线程及最终排空合同、完整可执行适配和独立直发回执。研究合同保持 `live_ready=false`、`send_verified=false`、`callable_for_send=false`，A7及实施20～24保持开放。账号安全原因尚未确认，不恢复活体验证。

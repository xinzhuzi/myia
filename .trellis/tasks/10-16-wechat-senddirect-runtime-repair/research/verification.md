# 修复与安装验收记录（2026-10-16）

**已交付：桥接入口隐式附加修复、失效驱动拒绝、离线缓冲区实现，保护修复已装入两个本机入口。**
**未交付：微信4.1.15任意正文原生直发。任务保持in_progress，L3未完成，不归档。**

**后续观察更新**：用户另行明确授权的一次观察已在21.053秒结束，成功脱附、原微信进程存活且调试位清除，未命中、未发送，授权已消费。观察器9项清理验证通过；静态默认普通回调已定位为空实现。详见`observation-and-callback-result.md`。下方“无活附加/runtime_calls=0”描述的是此前产品安装/被动验证轮，不代表后续研究没有执行上述授权观察；原生发送仍未完成。

## 落地变化

1. doctor.direct_channel默认直接读取磁盘，彻底移开execute_send/LLDB调用链。
2. send_direct --dry-run在取钥、目标解析、PID、LLDB和发送占位之前返回磁盘结果。
3. 正常CLI在取钥之前检查配置和驱动拒绝门；execute_send及raw batch也独立拦截。
   已证伪4.1.15配方不可通过改入口、锚表、版本标签或环境变量恢复。
4. 移除“零风险”提示，明确磁盘匹配不代表运行时或发送就绪；配置不是活附加授权。
5. 三方版本锁、组件合同、README及golden响应同步到0.9.1。
6. output-buffer-4115.cjs实现正确五字段输出缓冲区写入、长度重置及故障清空，
   不安装hook、不创建Task、不附加、不发送；未打包/装机该原生研究模块。

## 当前磁盘验证

| 验证层 | 结果 | 范围/限制 |
|---|---|---|
| 微信桥全部测试+桌面微信资源三项 | 845 passed, 14 skipped | UI/进程边界以桩隔离，14项真机门控保持跳过 |
| 本轮事故回归 | 15 passed | 配置开/关、重复doctor、FAT/thin、错误架构/边界、CLI/raw batch拒绝 |
| 缓冲区假内存测试 | 14 passed | 中文、长数据、缩短、视图、保护区和故障路径；不是实际发送 |
| 相关Python lint | All checks passed | 产品变更、测试及本轮Library/ai脚本 |
| 两个实际安装包 | 均0.9.1，runtime_calls=0 | 每套3次direct doctor、1次dry-run、CLI/raw batch拒绝，无发送状态文件 |
| 两个真实启动器，cwd=/ | dry-run exit0，正常入口exit24 | Python子进程审计禁止运行时spawn，命中数0；不做UI/发送验证 |
| 13个原生函数指令比对 | 4611条/18444字节全匹配 | 只证明留存二进制对应；不替代自动签名、类型、所有权及动态回执 |

实际安装包的doctor测试刻意把LLDB检查器设成missing，证明磁盘检查不依赖LLDB；
该字段不是本机工具安装清单。真实Resources/wechat.dylib的完整arm64身份与锚点均匹配。
本轮没有附加WeChat，没有操作UI、剪贴板或发送消息，没有重新测量用户感知流畅度。

精确命令、退出码及日志见 `verification-result.json`、`final-*.log`。
安装件证据见 `installed-passive-managed.json`、`installed-passive-standalone.json`、
`launcher-verification.json`。安装前差异与源码哈希见 `installation-inventory.json`、
`standalone-repair.diff`；已复核差异只涉及本轮入口/版本/文档改动。

## 两个安装入口

- 独立桥：`/Users/zhengbingjin/.myia/plugins/wechat-bridge`，仅同步7个必要文件。
- 桌面Python：`/Users/zhengbingjin/Library/Application Support/MYIA/python`，发行包0.8.4→0.9.1。
  逐项核对其余发行依赖版本，零变化；包内Python源码与仓库完全相同。
- 本地wheel：`wheels/wechat_bridge-0.9.1-py3-none-any.whl`。
  SHA256=`cc0aea78d21834bf81e53c107f7b6d19b5253df02ab5f9947e70154ddcdada65`。
- 安装前备份：`deployment-backup/`，72个代码/元数据文件，`sha256.json`逐件记录。
  未读取聊天数据库/真实密钥；历史备份仅供核对，不自动恢复旧驱动。
- 签名App资源未修改，未重打包App，未重启App或微信。后续发行须由更新后的源码构建。
- release-plugins脚本使用Git archive且不含wechat-bridge，本轮未调用；无Git/worktree/归档。

## 原生发送的剩余条件

Task+0x1c8和+0x1f0为分别原生复制和析构的buffer，不可当普通指针槽改写。
0x5daa6fc已按二进制指令解码确认为直接跳往复制函数0x5daa3c8，见native-thunk-proof.json。
特殊Req2Buf分支消费Task中已序列化的数据并继续包装；替换最终输出为裸protobuf尚不成立。
普通mmcallback_虚表+0x50实现、外部上下文/回调生命周期仍缺证明；具体证据与模块合同见
`native-repair-contract.md`。没有生成猜测签名或可运行的发送配方。

必须先补齐该关联及合格的取消/失败/到时脱附执行器，再取得用户对目标/用途/最长时限
的本次明确授权，才能前台单次验证真正回执。不能将上述离线通过或安装成功称为直发成功。
旧sentinel和旧实验编排器保持禁用，不接管或终止其他会话。

本轮由主线程实现与终审，无新增子代理。GitNexus对CLI main和错误报告函数评估LOW；
新回归测试尚未入索引，已按确切文件原文和可复现测试核验，未把索引缺失视为无影响。

## 版本JSON纠正（后续用户指令）

实际生效文件为`~/Library/Application Support/MYIA/wechat-bridge/send-direct-anchors.json`，
两套安装桥均通过同一数据根读取；不是component.json，也不是仓外OneBot旧版地址表。
当前Info.plist为4.1.15/270135，完整ARM64哈希及16字节锚点仍匹配；未改版本标签或哈希。
失效的是原生调用/对象布局合同，JSON原先仍将schema-3模板路线标作完整配方。

先保存`anchor-json-backup-20261016/send-direct-anchors.json`，再原子更新note，
将offsets的send_entry、enqueue_a、enqueue_b、service_ptr_mode、svc_vtable_off、
svc_invariants_hex、arg_abi置null。保留schema及身份门，不加入未经证明的新地址/布局。
变更前后哈希和精确字段清单见`anchor-json-alignment-change.json`。

`Library/ai/check_wechat_anchor_alignment_20261016.py --source standalone|managed`
由实际桌面Python分别加载两套0.9.1安装件：直接读取真实锚表后检查磁盘身份及不可调用状态；
CLI在任务私有沙箱运行，演练exit0、正常入口/execute_send/raw batch均exit24。
每套runtime_calls=0，无发送状态文件；报告为`anchor-json-verified-{source}.json`。
`uv run --no-sync python -m pytest -q tests/wechat-bridge/test_send_direct.py tests/wechat-bridge/test_send_direct_passive.py`
本次77 passed/1 skipped（真机门控），新增检查脚本ruff通过。未修改产品函数或上层HTTP协议。

这是撤销失效配方并核实版本身份，不是完成4.1.15原生直发；A7/L3保持开放。

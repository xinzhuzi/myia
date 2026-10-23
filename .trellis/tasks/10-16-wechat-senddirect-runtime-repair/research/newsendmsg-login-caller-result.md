# 登录调用者与编号缓存来源（2026-10-18，实施66）

## 本轮解决的来源疑点

- selector0：`0x11bad90`在`0x11bb7d4`和`0x11bb7e4`用地址`0x983dbd0`处的NUL构造两个空string，随后于`0x11bb7f8`分别以x1/x2传入`0x41009a0`。已核验string构造器的strlen、短string长度和NUL路径。这个调用点不能提供最终账号身份；不能推广到所有selector0结果。
- selector1：`0x2b38c0`在`0x2b3984`传入state+0x18首string、state+0x60原始值、state+0x30/+0x48另外两个string。状态虚表`0x9bf7f90`的+0x60槽为该函数；类型名称为冻结RTTI原文`_6074bdc6`，不能据此猜业务名称。
- 所选构造链：`0x2a16a8`的数值6分支按key object `0xa51cd78`查map，取node+0x20或默认variant；经过`0x6fe2590`及`0x20ba10`的隐藏x8输出路线得到字节string，复制进`0x2b355c`的x2输入；thunk为`0x2b35f8`。构造器安装上述虚表，以`0x2b3f8c`把三string/原始64位结构复制至state+0x18。这里证明转换路径，未证明所有variant都保持同一字符串值。
- 同一key的生产者：`0x2b1650`调用`0x3c7579c`；成功时把第一输出的data/length转为type10 variant，交给`0x2b2110`返回的map node+0x20。getter从`0xa4266c0`复制第一string，要求三份缓存均非空；之前还允许执行一次可选callback，故不是无副作用的纯读取。
- 该缓存的所选写入：`0x3c7534c`现场构造字符`3`和NUL，传给`0x487929c`，再把隐藏x8返回string移入`0xa4266c0`。仅证明编号键参数与存储路径，`0x487929c`精确语义、初始化key文本及实际dispatcher连接仍须继续核验。不能称它为用户名字段。

## 验证

`python3 Library/ai/verify_wechat_login_caller_20261018.py`退出0。16份选择导出共3113原始指令位置匹配冻结薄片；148项关键位置、25条独立分支目标、3个dyld槽及NUL/类型名称字节核验通过，新验证器Ruff通过。证据`login-caller-20261018-verification.json`。

合同SHA256：`b13b5b24ed259afc9b5b05274825c2badd40e8283454285564570623e37d4b96`。
验证器SHA256：`36807f81055b69c1be9a3cbd3b9189aca4abe5f7c48abda230ab5bc5c32310dd`。

dyld解码器曾拒绝将`0xa51cd78`等全局对象当作修复指针槽；未绕过断言，后续按真实调用引用分析对象。RTTI指针`0x9bf8030`解码值高位原样保留为`0x80000000084e0bc0`，单独核验其已知名称位置，不宣称运行时去标记规则。

## 边界与下一步

这些是所选静态路径，不证明该map一定传给该工厂、不证明state在调用前无其他修改、不证明转换前后字节恒等或业务身份。剩余编号键3业务语义、map key初始化文本/dispatcher、selector0最终结果保持、全部记录/方向与嵌套schema；原生线程/group/config、取消状态0清理与完整排空、完整适配器、真实发送/独立回执及部署仍未完成。

实施66只完成本离线来源切片。A7及11/18/20～24/55保持开放；账号停止约束未变，无微信/账号操作、无产品或安装件变更，无Git/worktree/删除/归档。下一步核验编号getter精确语义及map生产/消费之间的实际派发链。

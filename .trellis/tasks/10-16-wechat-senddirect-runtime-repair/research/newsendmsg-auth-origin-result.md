# 登录响应字段来源与调用方覆盖（2026-10-18，实施64）

## 结论与适配影响

所选普通登录结果生产者0x2fd7104在成功入口及response+0x30 bit1门内，将UnifyAuthResponse.field4 / AcctSectResp.field1字符串复制到结果payload+0x70。**但这不是无条件的最终账号来源**：0x2fea968的capture+0x48==1分支在调用该生产者后，于0x2feade0用capture+0x50字符串覆盖同一结果+0x70，然后才检查结果+4成功字节并构建账号安装输入。禁止将中间协议字段直接命名为最终账号字符串或发送人。

这补证实施63上游结果+0x70的一处生产和明确覆盖。后续适配必须保留分支及最终赋值来源；不能把“响应字段4.1”固定填进业务映射JSON。当前合同仍拒绝可发送状态，不装入产品。

## 已证明的编号字段与类型

- 父对象虚表0x9edc360，名称getter0x50e1ab4按冻结常量lane重建`micromsg.UnifyAuthResponse`；field2/wire0写+0x30，field4/wire2写+0x18子消息指针，存在位在+0x38的bit3。
- 子对象分配0x90，虚表0x9edc1f8；名称getter0x50deef0重建`micromsg.AcctSectResp`。field1/wire2由0x8b0535b跳表第1项派发至0x50ddba0，使用+0x8的string指针、+0x8c bit0存在位与0xa524ad0默认string哨值。精确业务字段名尚未证明，不称UserName。
- 父parser读取嵌套长度并核对深度，调用0x50ddaf4；子parser按短/长string存储准备18字节对象再调用0x5ab514c。只解释上述字段，不宣称完整schema已恢复。
- 0x2fd7104的原始输入bundle为x1，隐藏x8结果含+0x20 shared pair。首两个32位错误值均零才进入成功处理；response位于bundle+0x20。缺失section指针会读默认response的+0x18，不代表服务端实际提供field4。

## 覆盖与捕获生产

0x2fea968的x0是捕获对象。capture+0x48==1进入0x2feaca8，调用0x2fd7104后把返回区+0x20的shared pair留存在帧内。0x2feadd8/add x0,result+0x70，0x2feaddc/add x1,capture+0x50，0x2feade0完成string赋值。capture+0x48==0改调0x2fd02c8，不能把selector1的覆盖结论套给该分支。

0x2fc361c中0x2fc43b8所选x21对象，经0x2fec014分别复制到stack+0x40、stack+0x2b8、stack+0x1e0及最终functor+0x48。0x2fec014复制首uint32和+8处string（含长string复制），故捕获selector在+0x48、所选string在+0x50。最终functor写虚表0x9de0b00，+0x30槽独立dyld解码为0x2fea968。此处只证明立即生产，不猜x21对象的业务类型或用户名来源。

## 本轮验证及局限

命令：`python3 Library/ai/verify_wechat_auth_origin_20261018.py auth-origin-20261018-verification.json`。

9份选定Ghidra函数导出4540指令、两个完整LLVM parser范围1088指令均逐条匹配冻结薄片；去重5142个位置，186处关键指令、19个独立分支目标、8个dyld槽及2个重建类型名通过。两个parser边界由compact-unwind独立重算，分别为[0x50ddaf4,0x50de534)与[0x50e0fb0,0x50e1670)。不把重叠LLVM/Ghidra指令重复算作不同证据。两个Python脚本Ruff通过；未重跑历史真机/安装验证。

合同：`newsendmsg-auth-origin-contract.json`；验证器：`Library/ai/verify_wechat_auth_origin_20261018.py`；验证JSON保留合同/脚本/前置合同SHA256、导出清单与边界。实施63合同与账号停止记录哈希保持不变，A7、11/18/20～24/55及L3状态未关闭。

pass331漏传table count，Ghidra主进程退出0但脚本报错、无table.tsv；该次不能算成功证据，原日志保留。读取脚本参数后以pass332补传0xa完成表查询。pass330/332用于定位，pass333选用主生产者、pass334选用复制函数；pass335/336仅为下一处上游追踪定位，不计入本验证覆盖。

下一处已定位调用点为0x410dc54内0x410de38，x1取当时x19后调用0x2fc361c。仍须追原始输入、selector0及其他覆盖、完整记录/特殊路线，随后才能完成业务映射。真实线程/取消最终释放、完整原生适配、真实发送/独立回执及部署仍缺。账号停止约束保持；本轮无微信进程/UI/调试附加/原生调用/发送/登录操作，无产品接线、安装或Git操作。按当前模型可用性由主线程顺序处理，未启动子代理。

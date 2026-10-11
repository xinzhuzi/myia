# D4 豁免执行 — 内存扫描机制落地 + 提权真跑挂起(2026-10-11)

> 执行件:数据工-D4豁免(工作流子代理)。
> 豁免口径 = 主人「全部解决」令 + 豁免边界(对微信进程只读内存 vm_read 类 READ ONLY;
> 禁写/禁注入/禁调试器附加;sudo -n 非交互探测不可用即止,绝不索要/使用密码;
> 密钥即取即用落数据根私有区 600)。
> **红线 6 纪律**:本文零聊天内容、零密钥材料;证据只留形状(计数/码值/时长/速率)。

## 0. 结论速览

- **sudo 非交互探测:不可用**(`sudo -n true` → `sudo: a password is required`,exit 1)
  → 按豁免令边界**不硬来**:真跑挂起,主人单条提权命令已备(§5),`keyObtained=false`(如实)。
- **memsearch 空壳 → 配置可启真实现落地**(design §4 口径升级):只读 vm_read 单遍
  批处理 + 32B 滑窗候选 + 复用 E1 离线 HMAC 校验器 + 全量命中才落 `keys.json`
  (600;sudo 会话属主自动归还发起用户,见 §5);
  开关 = 桥组件配置键 `mem_search_enabled`(**缺省关**),CLI 挂 `localdb key-scan`。
- 合成内存全链单测全绿(命中/跨段拼接/预算截断/部分命中不落缓存/守卫钉死);
  实机扫描速率实测 **0.34 MiB/s**(4/8/16MiB 三档一致),256MiB 预算外推 ≈ **12.4 分钟**单遍。
- AC7 查询真跑同前挂起(依赖密钥);密钥一得(扫描命中或外部引入),E2/E3 链一步闭合
  (`resolve_keys` 消费通路 2026-10-11 审查轮已落码,无须再改代码)。

## 1. 提权探测(先做,不可用即止)

```console
$ sudo -n true
sudo: a password is required        # exit=1
```

→ 非交互提权不在,**绝不索要/使用密码**(豁免令原文)。落法 = 把真跑能力完整备好、
门禁钉死,主人以单条提权命令亲自触发(§5)。

## 2. 机制与边界(真实现落位,`wechat_bridge/memsearch.py`)

- **只读机械**(macOS mach 子集,ctypes 直呼 libSystem,零第三方依赖):
  `task_for_pid`(取 task port)→ `mach_vm_region`(VM_REGION_BASIC_INFO_64 枚举区)
  → `mach_vm_read_overwrite`(1 MiB 分段读,读进本进程缓冲即离手);用毕
  `mach_port_deallocate`。**零写、零注入、零调试语义**。
- **区筛选**:只取「可读可写且非 shared」区(malloc 堆焦点——SQLCipher key 是登录后
  生成的运行时 32 字节值,在堆结构中持有);滤除区与超上限区(>64 MiB)在**源头**
  记账跳过(区尺寸/保护位只在枚举处已知),计数如实进形状载荷。
- **滑窗候选即校验**(流式,不驻留候选集):31 字节跨段重叠(同区相邻段拼接恰好
  覆盖一次,换区即清);每 32 字节窗直接对首库(最小 page1)做离线 HMAC-SHA512
  校验(复用 E1 `verify_key_for_page`:salt⊕0x3A → PBKDF2-SHA512 2 轮 mac_key →
  HMAC 对 page1 数据段+小端页号比对尾部 64B);命中即交叉验证其余库,与 E1
  `acquire_key` 同构。4.1.x 密钥已不以 hex 文本存内存(research/localdb-e2e.md
  §1.3 三方旁证),故候选=原始 32 字节窗,不预设 hex 路径。
- **预算**(模块常量,刻意无配置面——预算即边界,边界不给人调):
  单区 64 MiB / 单次批处理总预算 256 MiB / 段 1 MiB;耗尽如实标 `interrupted`。
- **落盘纪律**:只在**全量命中**时 `write_key_cache`(数据根私有区
  `wechat-localdb/keys.json`,600,目录 700;sudo 会话属主归还发起用户,
  SUDO_UID/SUDO_GID);部分命中不落缓存(缓存=全量验证
  子集,与 E1 同纪律);全部应答/消息只承载形状(pids/区数/字节/滑窗/校验次数)。
- **只读红线源码级钉死**(tests/wechat-bridge/test_localdb_key.py
  `TestMemsearchShell::test_source_readonly_guards`):必需只读机械
  (`task_for_pid`/`mach_vm_region`/`mach_vm_read_overwrite`)必须在场;
  写/注入/调试类(`vm_write`/`vm_protect`/`vm_copy`/`ptrace`/`task_set_*`/
  `task_suspend`/`task_resume`/`thread_create`/`thread_set_*`/`task_policy`/
  `OpenProcess`/`WriteProcessMemory`)零引用。
- **三重门**(`acquire_key_from_memory` 逐门校验,缺一即 exit 21 结构化拒):
  ①主人 D4 豁免裁决在案(任务档承载);②配置 `mem_search_enabled=true`(缺省关);
  ③root 提权 + darwin 平台。进程族缺位(pgrep -x WeChat 零命中)→ exit 10 如实。

## 3. 配置可启(默认关口径的升级)

E1 空壳期口径:「无配置键,启用唯一途径 = 代码层显式改 `MEMORY_SEARCH_ENABLED`」。
豁免令后按 design §4 原文(「开关默认关,主人显式开启才生效」)升级为**配置可启**:

- 新配置键 `mem_search_enabled`(布尔,缺省 `false`;非布尔 usage 拒载;
  `null` 与未声明同语义回落缺省)——`config.py` / `component.json`
  config_defaults(真锁互钉单测)/ README / design §7 四处同步。
- component.json cli_contract 与 README 增补 `localdb key-scan`;redlines 措辞更新为
  「默认关,仅 D4 豁免后配置显式开启 + 提权才生效,且只读 vm_read 单遍零常驻」。
- 设计口径出处:design.md §4/§6/§7 已同步增补(本批提交)。

## 4. 实测证据(全部本会话亲跑)

| 检查 | 命令 | 结果 |
|---|---|---|
| sudo 非交互探测 | `sudo -n true` | exit 1,`a password is required` → 不可用 |
| 桥套件 | `.venv/bin/python -m pytest tests/wechat-bridge -q` | **137 passed / 4 skipped / 1 failed**;唯一失败 = `test_ax_gate.py::…stub_raises`,炸点在 `pixel.py:496`——**像素工在途未提交文件**(两轮跑之间被并行会话修改),非本批改动;本批触及面单独跑 = **85 passed** |
| ruff | `uvx ruff@0.16.10 check plugins/wechat-bridge/wechat_bridge tests/wechat-bridge` | All checks passed |
| golden | `MYIA_WECHAT_BRIDGE_REGEN_GOLDEN=1` 两轮再生成后稳定 | 漂移三处均为本批预期:probe/config 载荷增 `mem_search_enabled:false`、两处 fix_hint 措辞统一(「空壳」→配置键口径)、新场景 `err_memsearch_default_off` |
| 合成内存全链 | 单测(注入段源,key 埋点) | 命中→落缓存 600 ✓;跨段横卧 31B 拼接命中 ✓;预算截断如实 interrupted+不超收 ✓;部分命中不落缓存 ✓;零命中 exit 21 形状 ✓;缺省关/未提权/非 darwin/进程缺位四门 ✓ |
| 扫描测速 | 合成 4/8/8/16 MiB 随机内存+埋 key | **0.34 MiB/s** 四档一致(≈5.6µs/窗);命中全部证实;256 MiB 预算外推 ≈ **12.4 min** 单遍 |
| 真子进程冒烟 | `MYIA_HOME=<tmp> PYTHONPATH=<组件根> .venv/bin/python -m wechat_bridge localdb key-scan --json` | exit 21,`key_unavailable`「默认关(配置门未开)」——**escalation 命令形态真跑通过**(缺省关语义如实) |
| 同上 probe | `… python -m wechat_bridge --probe` | exit 0,degraded(key_unavailable);config 节带 `mem_search_enabled: false` 如实 |

## 5. 主人单条提权命令(真跑待此;keyObtained=false 的闭合途径)

```sh
mkdir -p "$HOME/Library/Application Support/MYIA/wechat-bridge" && printf '{"mem_search_enabled": true}\n' > "$HOME/Library/Application Support/MYIA/wechat-bridge/config.json" && sudo env MYIA_HOME="$HOME/Library/Application Support/MYIA" PYTHONPATH="/Users/zhengbingjin/Project/Github/MYIA/plugins/wechat-bridge" /Users/zhengbingjin/Project/Github/MYIA/.venv/bin/python -m wechat_bridge localdb key-scan --json; rc=$?; sudo chown -R "$(id -u):$(id -g)" "$HOME/Library/Application Support/MYIA/wechat-localdb" 2>/dev/null; (exit $rc)
```

**机理与边界(一次性批处理式只读扫描)**:

- 前半 = 显式开启开关(主人运行此命令即主人显式开启;事后还原 =
  `echo '{}' > "$HOME/Library/Application Support/MYIA/wechat-bridge/config.json"`
  回全缺省即关);中段 = root 提权下**一次**遍历扫描,扫完进程即退,
  零常驻、零轮询、零重试;尾部 = 属主归还(见下),`rc=$?` 先存扫描
  退出码、chown 对不存在目录静默跳过、`(exit $rc)` 原样奉还——零命中
  exit 21 等诚实退出码**不被 chown 吞掉**。
- **属主归还(成功分支不自坏,2026-10-12 复审增补)**:key-scan 门③只放行
  root,若 root 直接落 `keys.json`,缓存目录与文件即 root 属主,此后用户侧
  `localdb query`/sidecar 读缓存 PermissionError(被 `read_key_cache` 如实
  None 语义收编)→ `resolve_keys` 静默回落 E1 → **扫描实为命中却被报成
  零命中**,「一步闭合」自坏。双保险:①组件侧 `write_key_cache` 在
  euid==0 且 sudo 会话(SUDO_UID/SUDO_GID 在场)时自动把目录与文件属主
  归还发起 sudo 的用户(本批复测钉死);②命令尾部显式 `sudo chown`
  兜底(旧装机件/非 sudo root 会话场景)。
- 对微信进程只做 vm_read 类只读系统调用;可写私有区 32B 滑窗 × 离线 HMAC;
  禁写内存/禁注入/禁调试器附加/禁重签名(源码守卫钉死,非口头约束)。
- 预算:单区 64 MiB、总 256 MiB,实测速率外推全程 ≈12 分钟(期间微信零扰动、
  零前台操作;扫描器不触碰窗口/AX,纯内核只读调用)。
- 密码语义:sudo 密码由主人按日常习惯亲自输入,**桥与子代理全程不索要、
  不读、不存密码**。
- 命中 → `keys.json` 落数据根私有区(600,属主归还发起用户,见上)→
  `localdb query` 一步闭合(AC7);
  零命中/部分命中/内核拒绝 → exit 21 形状如实,**诚实第一:扫不到就扫不到**。
- **如实预告(不包装)**:本机微信为 hardened runtime 签名(codesign 实测
  `flags=0x10000(runtime)`,无 `get-task-allow`)——XNU 对 restricted 目标的
  `task_for_pid` 要求调用方持调试类 entitlement,**root 亦可能被拒
  (KERN_FAILURE)**。该拒绝即「红线内(不重签/不 lldb)此路在本机不可达」的
  如实信号,应答会原样上报 mach 码;届时 D4 收口回落 ②外部密钥引入
  (`keys.json`,组件校验器直接消费)或 ③长灰 degraded。

## 6. 红线自查

- 全程零激活调用、零合成点击、零窗口开合;真实微信进程内存**零触碰**
  (扫描只以注入段源在单测中验证;真跑挂起)。
- 密钥材料零入 git/日志/报告:测试全部合成 key;本文与应答只有形状计数。
- sudo 探测仅一次非交互尝试,无密码索求;无任何对微信进程的写/注入/调试
  (源码级守卫 + 本批零真跑双保险)。

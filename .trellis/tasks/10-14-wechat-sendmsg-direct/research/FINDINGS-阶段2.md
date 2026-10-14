# SendMsg 直调勘察·阶段 2 战果(10-14 晚)

## 定案事实(实证)

1. **活入口=FUN_043f88e4**(主线程,真发即命中,hit4 断点实证):RPC 家族真调度器(直调 05e1d050×4=service-id 分支所在)。
2. **归档张冠李戴勘误**:031ab38c(旧"主流程")与 043f88e4 角色互换——字符串「SendMsgFtouser」(0x88bac38)xref 两函数,branch 结构在 043f88e4。
3. 直接调用者=FUN_00a05ea0=协程 lambda(operator(),XOR 现场解码,task_service 族)——静态攀爬到此为止(协程函数指针入帧,无静态 xref)。
4. 明文(user,content)在协程创建点之上,尚未拿到。

## 剩余路线(下阶段)

- a. 断点 hit 时大范围 dump x0 对象内存搜正文 UTF-8(protobuf 层判明);
- b. 从协程创建点(malloc/make_task 对 00a05ea0 thunk 的装载)动态断点反向定位;
- c. ObjC 层试探:上文 UI 入口(Enter 键)→ ChatMgr 族的 runtime 方法枚举。

## 工程坑入册

- **Ghidra 遇中文路径必炸**(log4j URL 解析撞非 ASCII)——正解=`_JAVA_OPTIONS=-Dlog4j.configurationFile=file:///tmp/log4j2-min.xml` 覆盖,零移动零重装;符号链接无效(exec 解析回真路径)。
- 已分析工程 wxui.gpr(2.1GB)复用 + `-process -noanalysis` = 分钟级定向反编译(全量重分析 48 分钟不必)。

# MSI 装到 D 盘:属性名与命令式(tauri v2 WiX 模板实证)

任务:10-18-win-install-disk-pyenv 探查项①。日期:2026-10-18。
证据源:本机 `cargo tauri --version` = **tauri-cli 2.11.1**,其 bundler 模板
`crates/tauri-bundler/src/bundle/windows/msi/main.wxs`(git tag
`tauri-cli-v2.11.1`,commit e5ae5b93)已原样归档于本目录
`tauri-cli-2.11.1-msi-main.wxs`。**本会话无 Windows 主机,命令式为模板源码
定论 + 待实机一次核验**(验证法见文末)。

## 定论:属性名是 `INSTALLDIR`,不需要 TRANSFORMS

模板三处关键钉死(行号对应归档件):

1. **安装目录的 WiX Directory Id = `INSTALLDIR`**(L121-122):

   ```xml
   <Directory Id="$(var.PlatformProgramFilesFolder)" Name="PFiles">
       <Directory Id="INSTALLDIR" Name="{{product_name}}"/>
   ```

   (v1 判例里流传的 `APPLICATIONFOLDER` 名在 v2 模板**不存在**;v2 就是
   `INSTALLDIR`。)

2. **`INSTALLDIR` 是被 author 过的公共属性**(L76-83):模板声明了
   `<Property Id="INSTALLDIR">` 并挂两个 `RegistrySearch`(读
   `HKCU\Software\<manufacturer>\<product>` 的 nsis 缺省键 + `InstallDir`
   名值)。属性全大写 = 公共属性 → **可从 msiexec 命令行赋值**;这正是
   「Directory Id 同名公共属性可改写安装目录」这条 Windows Installer 机制
   生效的前提。

3. UI 侧 `<Property Id="WIXUI_INSTALLDIR" Value="INSTALLDIR" />`(L94):
   交互安装的目录选择对话框也绑同一个属性。

`TRANSFORMS`(.mst)是本地化/定制变换机制,与目录覆盖无关,**不需要**。

## 命令式(静默装到 D 盘)

```bat
msiexec /i myssia_0.0.4_x64.msi /qn INSTALLDIR="D:\myssia" /l*v install.log
```

注意:

- **路径不得以 `\` 结尾**:`INSTALLDIR="D:\myssia\"` 的尾部 `\"` 会被
  msiexec 命令行解析当转义引号吞掉,经典坑;写 `D:\myssia` 即可。
- 需管理员上下文(模板默认 per-machine 进 Program Files);`/qn` 全静默,
  `/passive` 可留进度条。
- **AppSearch 优先级**:命令行值先进会话,`AppSearch`(RegistrySearch)在
  其后跑、**命中即覆盖**——即「曾装过的机器上,注册表里的旧目录赢过命令行
  INSTALLDIR」。全新装机(无 `HKCU\Software\<manufacturer>\<product>` 键)时
  命令行值存活生效。**把已装机实例迁去 D 盘 = 先卸载(或清掉该注册表键)
  再带 INSTALLDIR 装**;升级(同目录)不受影响,读注册表沿用旧目录正是
  预期。
- 实机核验法:① 日志 `install.log` 搜 `INSTALLDIR`(AppSearch 段看属性终值);
  ② 装完查 `HKCU\Software\<manufacturer>\<product>\InstallDir` 值;③ 直接看
  `D:\myssia\myssia-desktop.exe` 在位。manufacturer/product 取值见
  `tauri.conf.json` 的 `productName`/`identifier` 域。

## 与本任务代码面的接合

- 壳侧 `pyenv_env_base`(main.rs,10-18 改造)取 `current_exe()` 父目录做
  可写探测:装到 `D:\myssia` → exe 同目录可写 → python 环境根 =
  `D:\myssia\python`;装默认 `C:\Program Files\myssia` → 探针失败 → 回落
  `%APPDATA%\MYIA\python`(存量行为不破)。
- **卸载语义(prd 注记)**:模板 L185-186 有 `<RemoveFolder Id="INSTALLDIR"
  On="uninstall" />`——MSI 标准动作只删「安装器自建的空目录」,运行期生成的
  `python/`(非 MSI 装的文件)通常**残留**(非空目录删不动);但主人指令
  的语义按「python 在安装路径下,卸载/清目录即环境消」如实接受。守卫:
  进度戳 `python-env.json` 恒落数据根,重装同目录时戳说 ready 而 python
  缺位 → detect 判 error 引导重装,不误判 ready(本次新增测试
  `detect_with_injected_env_base_splits_python_from_stamp` 与
  `injected_env_base_puts_python_in_install_dir_keeps_stamp_in_data_root`
  双钉)。

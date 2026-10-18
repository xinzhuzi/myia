# PRD:Windows 上 Python 环境根随安装目录(10-18-win-install-disk-pyenv)

## 主人指令(2026-10-18)

Windows 上「Python 需要安装在安装路径下面」——自管 Python 环境根从数据根
(`%APPDATA%\MYIA\python`)改为**随应用安装目录**(如 `D:\myssia\python`);
装 `C:\Program Files`(不可写)时须保底回落数据根——默认安装路径的存量
行为不能破。

## 需求(Req)

1. Windows:exe 同目录存在且可写 → 环境根 = `<安装目录>/python`;
2. Windows:安装目录不可写(默认 Program Files)/ exe 目录缺位 → 回落
   `<数据根>/python`(存量行为一字不变);
3. macOS:恒数据根,零行为变化;
4. 进度戳(`python-env.json`)/ 镜像设置(`pyenv-settings.json`)恒落数据根
   (用户态数据不随安装目录走)。

## 决议(D)

- **D1 纯函数三分支**:`pyenv::python_env_base_on(data_root, exe_dir,
  windows)`(pyenv.rs)——Windows+可写 exe 目录 → 安装目录;否则数据根。
  可写探测 = 目录在 + 建写删探针文件(名带 pid 防并发互踩)。运行期入口
  `python_env_base(data_root, myia_home_set, exe_dir)` + main.rs
  `pyenv_env_base(app)`(取 `current_exe()` 父目录,与 data_root 同款按调用
  重解析,探针廉价且自愈)。
- **D2 MYIA_HOME 沙箱豁免**:显式 MYIA_HOME(自动化/补验独立实例域)恒
  数据根不注入——沙箱布局确定性是既定契约(tests/desktop 与 AUTOSETUP
  冒烟都以 `<MYIA_HOME>/python` 为锚),MYIA_HOME「不夺权」同款惯例。
- **D3 用户态数据恒数据根**:进度戳/镜像设置/下载缓存
  (`downloads/`)/组件戳/服务目录/playwright-browsers 全部不动;只有
  `python/`(及解压暂存 `.pyenv-staging/`、pip site-packages)落 env_base。
- **D4 MSI 卸载/升级语义注记(grill 自检定案)**:python 在安装目录 →
  **卸载或手工清目录即环境消**——这是主人明确要的形态,如实接受。WiX 模板
  的 `RemoveFolder On="uninstall"` 只删安装器自建的空目录,运行期生成的
  `python/` 通常残留;但语义按「可能被删」设计。**守卫:戳在数据根**,
  重装同目录时戳说 ready 而 python 缺位 → detect 判 error(「环境进度戳记
  ready 但 Python 缺位」)引导重装,不误判 ready——既有判定链天然覆盖,
  本次以测试双钉(detect 分根测试 + 安装链注入形态测试)。升级覆盖安装
  (major upgrade 沿用旧目录)不删运行期目录 → 环境存活,零额外处理。
- **D5 磁盘预检与解压暂存随 env_base**:预检查 env_base 所在盘(解压 +
  site-packages 大头落点);解压暂存同落 env_base——rename 原子改名要求
  同卷,跨盘(C: 数据根 / D: 安装目录)时暂存落数据根反而会炸
  EXDEV/ERROR_NOT_SAME_DEVICE。
- **D6 IPC 契约零变化**:`install_path`/`python_path` 字段语义 = 实际落点
  (注入后即安装目录形态),载荷键集不变。

## 消费点(全部切 env_base)

spawn(main.rs)、status/detect/pyenv_sync_deps(pyenv.rs)、安装链
(pyenv_install.rs:布局守卫/python_bin/解压/预检)、组件安装/服务启停/
回收(pyenv_components.rs 六处)。

## 验收(AC)

- 单测三分支:可写安装目录注入 / 不可写回落(unix chmod 0555 实盘形态)/
  macOS 恒数据根 + MYIA_HOME 沙箱豁免 + 分根 detect(python 走 env_base、
  戳走数据根、MSI 卸载形态不误判 ready)。
- 安装链注入形态:env_base ≠ 数据根全链真跑(python/暂存落安装目录,戳/
  下载缓存留数据根)。
- 门禁:`cargo test` 162 passed / 0 failed(2 ignored 为既有真网门控冒烟)
  + `cargo check` 净(仅存量 sanitize_file_name 警告,非本任务)+ 四改动
  文件 rustfmt 净。

## 探查产物(research/)

- `install-to-d.md`:MSI 装 D 盘 = `msiexec /i … /qn INSTALLDIR="D:\myssia"`
  (tauri-cli 2.11.1 模板实证;不需 TRANSFORMS;归档 `tauri-cli-2.11.1-msi-main.wxs`)。
- `headless-setup.md`:无头装环境钩子 `MYIA_PYENV_AUTOSETUP=1|force` 在
  (main.rs setup),schtasks+cmd 命令式落档。
- `download-proxy.md`:壳下载走 reqwest 0.13.5 且**吃** WinINET 系统代理
  (updater 默认特性把 system-proxy 拉回);直连逃生 = `NO_PROXY=*`;
  仅清 HTTP_PROXY env 无效(注册表补位)。

## 终局(2026-10-18 晨,v0.0.6 全轮)

v0.0.5 抓出 mkfifo 出厂 bug(serve 无 darwin 守卫)→ d3dbb0f8 修复 →
v0.0.6 全链收口:D 盘安装(INSTALLDIR=D:\myssia)+ Python 落
D:\myssia\python(3.14.8,戳落数据根 state=ready)+ sidecar 真起
(安装路径 python.exe 驱动 serve,version ping 0.0.6 过)。终审全链
证据独立核验(tag/MSI 比特一致/安装日志/进程/时序单调),app 留机运行。
三轮流水线:0.0.4 验链→0.0.5 抓虫→0.0.6 闭环。

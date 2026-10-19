# 「安装 Python 环境」的无头触发面(MYIA_PYENV_AUTOSETUP)

任务:10-18-win-install-disk-pyenv 探查项②。日期:2026-10-18。
源码定论:desktop/src-tauri/src/main.rs setup() 内(L1093 起,mac AUTOSETUP
同款钩子,发布包无人设置)。

## 结论:env 钩子在,无头可行(非「只能 UI 触发」)

设置页「开始配置」走 `pyenv_start_setup` IPC(UI 面);但壳 setup() 里有
**`MYIA_PYENV_AUTOSETUP` 启动即装钩子**(10-05 第 5 步落地,自动化端到端
冒烟用):

- 值 `"1"`:仅当当前态 `not_configured`(全新装机主链)才拉起安装链;
- 值 `"force"`:无视当前态重跑(ready 幂等二跑 / error 态补跑验证用;
  `installing` 态会被 `start_install_thread` 占坑护栏拒,不构成双跑);
- 镜像读数据根 `pyenv-settings.json`(安装前预写该文件即可指定
  mirror_runtime/mirror_pypi,如指向内网静态服务器);
- 钩子在 setup() 内、UI 之外的壳启动序列执行——**零交互**,但注意 Windows
  发布包主窗 `visible: true` 出厂(tauri.windows.conf.json,10-14
  win-startup-show),所以「无头」= 无需点击,不是无窗口。

## Windows 命令式

GUI app 不继承计划任务外的用户环境变量,env 必须在同一 cmd 进程里 set:

一次性手工(管理员或普通 cmd 均可):

```bat
cmd /c "set MYIA_PYENV_AUTOSETUP=1&& D:\myssia\myssia-desktop.exe"
```

计划任务(schtasks,cmd 包装注入 env;`start ""` 分离让 schtasks 立即回收):

```bat
schtasks /create /tn "MYIA-PyenvAutoSetup" /tr "cmd /c set MYIA_PYENV_AUTOSETUP=1&& start \"\" \"D:\myssia\myssia-desktop.exe\"" /sc once /st 22:30
schtasks /run /tn "MYIA-PyenvAutoSetup"
```

- 上一轮安装以 error 收场(如断网)时,`"1"` 不会再触发(not_configured
  才触发)——补跑用 `force`:`set MYIA_PYENV_AUTOSETUP=force&& …`。
- 与 10-18 安装目录注入的接合:exe 在 `D:\myssia`,可写 → python 环境装到
  `D:\myssia\python`;`MYIA_HOME` 显式设置时恒数据根不注入(沙箱豁免),
  自动化断言仍以 `<MYIA_HOME>/python` 为锚。
- 代理逃生(下载段,见 download-proxy.md):同 cmd 里可再叠
  `set NO_PROXY=*&&` 直连。

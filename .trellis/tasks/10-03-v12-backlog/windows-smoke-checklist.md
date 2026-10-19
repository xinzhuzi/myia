# Windows 真机冒烟步骤单(主人侧;2026-10-19 重建)

> 背景:原步骤单放 /tmp 已被清理吞失(/tmp 吞件三犯在案),本单依归档
> `archive/2026-10/10-04-windows-build/prd.md` §真机冒烟清单 重建,落活档防再吞。
> 真机档案(2026-10-05 实测):zbj@192.168.0.101,SSH 免密(cmd 通道),MSVC/WebView2
> 已装,MYIA 0.0.1 已装保留,myia-show.cmd 亮窗脚本在位。

## 0. 取安装包(任选其一)

- 浏览器:GitHub Releases → v0.0.1 → `myia_0.0.1_x64.msi`(121.8MiB,ASCII 名)
- 或命令行(本机代下后scp):`gh release download v0.0.1 -p "myia_0.0.1_x64.msi" -R xinzhuzi/myia`

## 1. 七项清单(逐项看结果,勾一项记一项)

| # | 项 | 怎么验 | 通过标准 |
|---|---|---|---|
| 1 | msi 安装 | 双击或 `msiexec /i myia_0.0.1_x64.msi /passive` | 开始菜单快捷方式出现;「设置-应用」卸载项出现 |
| 2 | SmartScreen/Defender | 首次运行 myia.exe | 拦截形态与 README Windows 安装节口径一致(文档说会拦、怎么放行) |
| 3 | 首跑种子 | 首启后查 `%APPDATA%\MYIA\plugins\*.yaml` | 五件 yaml 在位;五屏数据/空态正常 |
| 4 | **keychain→Windows 凭据管理器(DPAPI)链** | 种子插件真用 `keychain:` 引用(ai-news.yaml:126,131、credentials.yaml:28);在 Windows 凭据管理器看条目 | 凭据可存取;**缺席时应报 `keychain_backend_unavailable` 结构化错而非崩溃**(该链 Windows 侧从未真跑过,CI 三次 run 全死在 uv sync,此项最值得盯) |
| 5 | sidecar 无黑窗 | 启动 app 观察 | 无黑色控制台窗闪出(CREATE_NO_WINDOW) |
| 6 | 静默升级 | 设置页检查更新 → msi passive 升级 → relaunch | 全程无感完成 |
| 7 | 单实例 | MSI 装好后连开两次 | Windows 无 flock,观察项非阻塞:第二次启动行为(唤出/共存)如实记 |

## 2. 回执

逐项结果(过/不过+形态截图)回给 AI 侧即可,尤其 #4 的 DPAPI 链结果决定
是否需要 Windows 侧凭据链修复档。冒烟为「如实注记,不阻交付」口径——
清单源于 10-04-windows-build(D10 裁决:真机有无未知时冒烟=主人侧清单)。

# 10-04-windows-build 冒烟证据(2026-10-04,proxy+win 冒烟员)

静态 + dry 口径(CI 真跑不可行 → 如实 manual,推 origin 后首跑验证):

| 文件 | 内容 | 对应 AC |
|---|---|---|
| `workflow_static_assertions.py/.log` | desktop-release.yml yaml.safe_load 解析 + 34 项矩阵静态断言:三 job 清单/windows-msi 转正式(无 continue-on-error、timeout 60、windows-latest、py3.11+node22+rust stable)/产物清单诊断步/ASCII 改名/win-msi artifact(error 门)/mac 主线形态(macos-14、app,dmg、latest.json 移出、tag 门)/release-finalize(ubuntu-latest、needs、always()+mac result 门、latest.json 单写者、win 条件并入、latest-json 无条件 artifact)→ **34 PASS,exit 0**;actionlint → clean | AC2/AC3/AC4(静态面) |
| `win_build_dry_logic.py/.log` | workflow 原文 run 块本地演练(零外网):D1 版本解析四场景(tag/分支无参回退 conf/分支带参/预发布)+ ::warn:: 路径;D2/D3 win+mac ASCII 改名(fake bundle 树,产物名与内容逐一断言);D4 latest.json 两分支(win 在=并入+URL ASCII / 缺席=仅 darwin+warn);D5 build-sidecar.sh 守卫(darwin 拒 windows 目标 exit 1;MYIA_SIDECAR_SKIP=1 快路径 exit 0);D6 ocrmac marker(pyproject:50、uv.lock:1979/2003、uv export)+ URL 体系 tsinghua → **30 PASS,exit 0** | AC1(静态面)/AC4(生成逻辑)/AC6(版本回退) |
| `docs-consistency.log` | Releases 链接 vs git remote(xinzhuzi/myia 一致)、ASCII 前缀 myia_ 三处口径(workflow/README/UPDATER)、README 链接目标存在、productName/version 基座;2 观察项(en 半区安装节无 Windows 小节=留主人;路线图「暂无 Windows 包」发布后需回改) | AC5 |
| `full-pytest.log` | 全量 pytest → **3495 passed, 19 skipped, 0 failed(exit 0)** | AC6(pytest 部分) |

补充:tauri.conf.json `bundle.icon` 含 `icons/icon.ico`(文件在,84,679 B)与 myia-core.spec darwin 门(py_compile ok)均已核;mac sidecar 构建本会话**未重跑**(构建需 uv sync 外网,冒烟口径零外网)——实施会话记录 exit 0/124,059,712 B(prd 验收记录),本会话核磁盘产物在位 124,120,784 B(10-04 11:57)+ SKIP 快路径可用。CI 实跑(windows-msi conclusion、artifacts、latest-json、run URL 回填)= 推 origin 后首跑,留 leftovers。

# install-log — 世事.app 静默换装(面板修复版)

- 日期:2026-10-05
- 操作者:装机员(workflow subagent)
- 源(bundle 产物):`desktop/src-tauri/target/release/bundle/macos/世事.app`
- 目标:`/Applications/世事.app`

## 1. 防竞态检查

| 命令 | 输出要点 | 退出码 |
|---|---|---|
| `ls -la /Applications/世事.app/Contents/MacOS/` | 旧二进制 mtime `Oct 5 04:21`(13931536 B) | 0 |
| `date "+%Y-%m-%d %H:%M:%S"` | 检查时刻 `2026-10-05 11:24:15` | 0 |

mtime 距今约 7 小时 ≥ 3 分钟阈值 → 判定无并行换装,**未触发等待轮**,直接放行。

bundle 产物侧确认:`ls -la .../bundle/macos/世事.app/Contents/MacOS/` → 二进制 mtime `Oct 5 11:23`(13931536 B),退出码 0。

## 2. 运行实例检查

| 命令 | 输出 | 退出码 |
|---|---|---|
| `pgrep -x MYIA` | 无输出(无实例) | 1 |

无实例 → 跳过 osascript quit。

## 3. 换装(三步)

起始时间戳 `date +%s`,备份名带 `date +%H%M%S` = `112434`。

| 步骤 | 命令 | 退出码 |
|---|---|---|
| 备份 | `ditto "/Applications/世事.app" "/tmp/世事.app.bak-palette-112434"` | 0 |
| 删旧 | `rm -rf "/Applications/世事.app"` | 0 |
| 装新 | `ditto "<repo>/desktop/src-tauri/target/release/bundle/macos/世事.app" "/Applications/世事.app"` | 0 |

**耗时:1 秒**(`ELAPSED=1s`)。

## 4. 核对

| 命令 | 结果 | 退出码 |
|---|---|---|
| `stat -f "%z %N"` 三方尺寸 | 装后 `/Applications/.../MYIA` = 13931536 B;bundle 产物 = 13931536 B;备份 = 13931536 B | 0 |
| `cmp -s` 装后 vs bundle 产物 | 字节级一致 | 0 |
| `ls -la /Applications/世事.app/Contents/MacOS/` | 二进制 13931536 B,mtime `Oct 5 11:23`(随 ditto 保留源 mtime) | 0 |
| 备份旧包确认 | `/tmp/世事.app.bak-palette-112434/Contents/MacOS/MYIA` mtime `Oct 5 04:21:52 2026` → 确为换装前旧包 | 0 |

## 5. 终态

- 新包路径:`/Applications/世事.app`(二进制与 bundle 产物尺寸一致且字节级相同)
- 备份路径:`/tmp/世事.app.bak-palette-112434`(旧 04:21 构建)
- 未启动 app(冒烟线会自启);未 push;未跑全量测试(门禁由脚本统一执行)。

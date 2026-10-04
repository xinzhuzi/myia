# r2 活性条去行话回修:装机包无头冒烟(2026-10-05 00:52)

> 背景:主人 review「ticker 活跃/1 个 job/裸路径——用户看得懂吗」→ r2 文案回修
> (41ccdba)→ 除单测/门禁外,补装机包级无头冒烟一环。工具与截图:
> `.zcode/smoke/croncopy-drive.cjs` + `croncopy-shot.png`(gitignore 本地件)。

## 链路(真实组合)

- sidecar = `/Applications/世事.app/Contents/MacOS/myssia-core`(00:43 换装版,
  装机包自带二进制直驱 `serve`;MYIA_HOME 经桥旁路旋钮 `SMOKE_MYIA_HOME` 注沙箱)
- UI = vite 源码(ui-src 已提交态)+ `__TAURI_INTERNALS__` shim → bridge.mjs;
  装机包内嵌 UI 与源码同源(00:43 构建,哈希已核),等价
- 沙箱 home `/tmp/myia-cron-smoke`:job 冒烟A(every 1h,启用)+ 冒烟B(--paused)
  → jobs_total=2 / jobs_enabled=1;serve home 模式自带 cron ticker(entry.py:327),
  心跳真活 → 绿条为真「调度器运行中」非 mock

## 断言结果(SMOKE: PASS,7/7)

活性条逐字:`调度器运行中 · 下次运行 10/05 01:50 · 1/2 个任务启用 · 数据目录 /tmp/myia-cron-smoke`

| 检查 | 结果 |
|------|------|
| 调度器运行中(绿条,ticker 真心跳) | ✓ |
| 下次运行(真 next_run_at) | ✓ |
| 1/2 个任务启用(部分暂停分数形态) | ✓ |
| 数据目录 前缀 | ✓ |
| 表行渲染(冒烟A) | ✓ |
| console/pageerror 零错误 | ✓ |

## 顺带事项

- bridge.mjs 加 `SMOKE_MYIA_HOME` 旁路旋钮:缺省仍显式清空 MYIA_HOME(dev 回退
  原行为不变);装机包 sidecar + 沙箱 home 的冒烟形态自此可复用
- 冒烟后桥/vite 进程已清、沙箱已删;仓库根曾误落的 `cron/`(CLI 数据根=cwd
  乌龙)已清,git status 零残留

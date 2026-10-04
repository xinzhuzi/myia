# 执行计划——桌面自管 Python 环境

前置:PRD 决议 D1-D6 与 design.md 已定案(2026-10-05 主人批);执行按序,每步带验证门。

## 顺序清单

- [ ] 1. 随包交付物:myssia 源码打包进 tauri resources + 入口模块(`myssia_desktop_entry`,复用 entry.py 协议面)+ `runtime-manifest.json`(钉主人 URL+sha256 实算+win 等效件)+ `requirements-lock.txt`
      门:resources 内容清单核验;锁版清单与 pyproject 一致性测试
- [ ] 2. Rust 壳:环境探测(就绪/未配置/依赖漂移三态)+ spawn 改造 + `pyenv_not_ready` 空态事件
      门:壳侧单测;未配置态启动不崩(UI 空态可见)
- [ ] 3. 安装链执行器(壳内):状态机+幂等进度戳+sha256 校验+磁盘预检+错误分类
      门:单测(含坏包/中断重试);本地静态服务器钉版文件全链真跑
- [ ] 4. 设置屏区块:开始配置/路径/双镜像覆盖/安装明细/同步依赖
      门:vitest+tsc;IPC 契约测试
- [ ] 5. 依赖安装与自检:pip 锁版装 + sidecar version ping 自检
      门:沙箱数据根端到端(AC1 主链)
- [ ] 6. 存量迁移:首启检测+一次性引导(D5)
      门:旧数据根夹具测试,数据零丢失断言
- [ ] 7. 打包链收口:build-sidecar.sh/spec 退役注记、desktop-release.yml 适配、tauri.conf externalBin→resources
      门:tauri build 出包且包体显著小于 118M;CI 门控绿
- [ ] 8. 文档与装机:docs zh/en getting-started 新安装叙事;装机冒烟+静默换装
      门:AC1-AC5 逐条回标;AC6 Windows 真机留主人侧;AC7/AC8 核验

## 回滚点

- 任一步后均可回退:数据根布局不变,旧冻结版包可直接重装回落(数据无损)
- 打包链退役放最后一步,之前任一态都可双轨(冻结版照发)

## 风险盯点

- python-build-standalone 下载源可用性(镜像覆盖是正门)
- pip 国内连通性(索引覆盖是正门)
- 依赖锁版与 myssia 源码随包版本漂移 → 同步依赖按钮兜底(D4)

# 遗留清账终批:目验取证+占用视图真卸载+py3.14+发布说明+覆盖安装

## Goal

清单 AI 可做四域:T1 目验取证(cron 隔夜/媒体CDN/取钥器行)/T2 数据根占用视图+真卸载/T3 自管 Python 3.14 升级链(zstd 全解码)/T4 v0.0.4 发布说明前置;深度探索→计划→grill 拷问→执行→深化→打包覆盖安装

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only. For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 决议注记(py314 域,2026-10-14 执行时落笔;均留主人过目)

### D3-v2 改钉:自管 Python 3.12.7 → 3.14.8(PBS release 20261013,迁址后新 org astral-sh)

前钉 D3(2026-10-05 PRD 决议,tests/desktop/test_pyenv_resources.py 原 :42 注「一字不改」)由此作废——本次改钉是新决议 **D3-v2**,非悄悄改;断言常量/注释/任务档/提交信息四方同载。新钉 URL 全文:

- mac(aarch64-apple-darwin):
  `https://github.com/astral-sh/python-build-standalone/releases/download/20261013/cpython-3.14.8+20261013-aarch64-apple-darwin-install_only.tar.gz`
  sha256=`709f419d175eb015f810b68aa54bdae1d776c9824cb362aa701c93b0a9f2a9e7`
- win(x86_64-pc-windows-msvc):
  `https://github.com/astral-sh/python-build-standalone/releases/download/20261013/cpython-3.14.8+20261013-x86_64-pc-windows-msvc-install_only.tar.gz`
  sha256=`3adacae2a39dfcbebe8d95a6e87a0dee167a057ab8f822eacf38e5fa4c97f76e`

distribution 同步换 `astral-sh/python-build-standalone`(Q8:旧 org 值与 astral-sh 域 URL 构成自相矛盾元数据);extract_root_dir=python / python_bin 契约不变。Windows 侧本机仅做资产下载+sha256 对拍,**未实装验证**(macOS 机无法跑 Windows 实装),如实注记。回滚=manifest 回钉旧值(indygreg release 仍在)+python-3.12.bak 改名回+删新 python-env.json/双戳全套。

### Phase A 基线口径偏差注记

生产 3.12.7 自管解释器**无 pytest 模块**(实测 `No module named pytest`),往生产环境 pip 装 pytest 会污染依赖指纹链(python-env.json 漂移),故基线改为「双沙箱 A/B」:PBS 3.12.7@20241016(旧钉,sha256 对 manifest 现值)与 PBS 3.14.8@20261013 两个干净沙箱同配方(装齐 requirements-lock.txt + pytest),同命令 `python3 -m pytest -q` 对拍通过数——只差解释器版本,比污染生产环境取基线更可控。

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

### Phase A 终轮 R3 判定与第四处钉版断言(2026-10-14 23:37)

- 终轮 R3:根套件 3.12.7 vs 3.14.8 = **6288 passed == 6288 passed**(60 skipped 同;各 1 failed 且为同一测试 `tests/classify/test_classifier_package.py::test_distribution_metadata_version_and_trove_classifiers`——锁钉 PyPI `myssia-classifier==0.0.1`(requirements-lock.txt:27)vs 测试期 0.0.3 的仓内既有漂移,lock-only 环境必红、dev 工作区 -e 装配则绿,与解释器无关);`pytest -q tests/wechat-bridge` **双侧 758 passed / 20 skipped / EXIT=0 全绿**。结论:无 3.14 专属红,不触发 degradedPaths 冻结。
- Q8 三处之外的**第四处钉版断言**:`tests/desktop/test_pyenv_e2e.py:654` 硬断言 `"Python 3.12.7"`(本轮亲跑暴露),已同步为 3.14.8(提交 a2a02d6);tests/ 全树 grep 三词(3.12.7/20241016/indygreg)清零。
- e2e 会话夹具 wheels 缓存 marker 只认锁 sha(test_pyenv_e2e.py:138-152):**换钉后旧 3.12 ABI wheels 缓存会拒配报「缓存损坏」**,需删 `~/Library/Caches/myia-pyenv-e2e/wheels` 重建(本机已重建为 3.14 wheels,42 件);上游建议后续把 marker 扩为锁 sha+运行时 sha(留主人裁决,未擅改)。
- 桥两级 import 链 3.12/3.14 幂等实证:`python -m wechat_bridge --version` 双侧沙箱均 `wechat-bridge 0.8.4` EXIT=0。

### Phase C 生产切换移交装机维护窗(编排裁决,2026-10-14 23:44)

- 迁移窗口发现生产数据根被并行改动(storage 线按 Q4 连坐口径整目录回收:playwright-browsers/、crawl4ai/searxng 组件戳、services/searxng/ 已删;searxng 8888 监听随之消失;7 个 chrome-headless 孤儿进程仍在跑待装机阶段统一清)。升级裁决:**py314 生产切换(退 app→mv python→删戳→force 重装)并入「打包覆盖安装」同一维护窗执行,一次停机两件事**。
- 装机员约束(编排裁决原文):**force 重装不得复活 storage 线已回收的组件**——crawl4ai/searxng/playwright-browsers 三者的戳与目录保持未装态(用户回收意图);重装范围 = python 本体 + 仍处装态的组件戳(table/trafilatura/telethon/wechat-bridge)。
- 就绪件:evidence/py314/ 已留迁移脚本 phase-c-migration.sh(8888 放行门/argv 锚组杀/归档预播种/force 直跑二进制/ready 等待,逐 gate)与 app 包内 manifest 原值备份(bundle-manifest.orig-indygreg-3.12.7.json,回滚用);app 包内 manifest 已同步 D3-v2(adhoc 签名不破启);mirror_pypi 临时设置已用毕恢复 `{}`(装机窗如需提速可再置,装毕恢复);MYIA_HOME 独立域彩排已全绿(五段 done 至 ready、selfcheck 过、zstd OK,证据 rehearsal-python-env.json)。
- 迁移窗口情报流缺档注记:weixin-sns */5 全天档在跑,装机窗停机期间缺档由该窗统一注记。

## 终局回执(簿记归档员落笔,2026-10-15;材料=编排回执逐字)

- **四域**(编排材料逐字):`{"k":"storage","done":true}` / `{"k":"py314","done":true}` / `{"k":"release-notes","done":true}`。
  - storage:代码 56ba74c 落库(pyenv_storage_usage/pyenv_reclaim_storage 两命令+存储卡三件+main.rs 注册,8 件 1540 行)。
  - py314:代码已 a2a02d6(D3-v2 改钉)+d4914a1(R3 判定注记);装机切换见下。
  - release-notes:CHANGELOG v0.0.4 段落+窗注(187 件口径;storage/py314 落库后补录与否留主人推 tag 前裁决)——56ba74c 同批落库。
  - **T1 目验取证域缺口如实注记**:编排材料标「四域」仅附三域回执对象,T1(cron 隔夜/媒体CDN/取钥器行)无编排回执;evidence 仅 key-fetcher-row-weixin-sandbox.png 一件(取钥器行),cron 隔夜与媒体 CDN 两项目验取证未见于 evidence/ 与提交史,按未收编排判定如实留档,不代判。
- **门禁**:绿(编排回执;簿记员未重跑)。
- **复查**:过(编排回执;簿记员未重跑)。
- **装机**(编排回执逐字):`{"rebuilt":true,"swapped":true}`——重打包+换装均成;证据 evidence/install-window/(build/components/py314/swap 四日志+sessionA2/B2/C 三截图);约束兑现亲验:install-window/py314.log:8-9 `absent-ok playwright-browsers` / `absent-ok services/searxng`(storage 线回收组件未复活)。
- **簿记事实**:代码提交 56ba74c(8 件,含 tests/conftest.py ORT_DISABLE_TELEMETRY 门禁支撑件——归属链:全仓活跃线中唯本线跑 Python 全量门禁,UI sweep 为纯前端线不认领);evidence/ 敏感性扫描过(凭据词零命中;十六进制串逐个核对=PBS 公开 sha256/pip wheel 指纹/缓存路径,components.log:96-97、py314.log:11);并行在途件(UI sweep 屏族+frontend-ui.md+ghidra scripts+sendmsg_hunt.c 等)未碰。

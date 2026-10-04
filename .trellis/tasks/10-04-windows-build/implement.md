# implement — Windows 产物化:CI 构建与发行文档

执行序(依赖关系驱动):F1 解锁一切 → F2 配置 → F3 workflow → dispatch 验证循环
→ F4 文档 → 定向检查收口。每步带验证命令与回滚点;全量门禁由脚本统一,
本任务只自跑定向检查。

---

## 阶段 0:前置核对(不动文件)

- [x] 0.1 读 `research/windows-build-current-state.md` + prd + design(本档的
      上下文就是这三件)。
      → 终检复核:research 档在位(随本档入档),验收记录通篇锚 research 各节
- [x] 0.2 `git status --porcelain` 记录外来未提交清单;确认 pyproject.toml /
      uv.lock 改动内容(`git diff pyproject.toml uv.lock`),后续叠加勿覆写。
      **2026-10-04 实况**:起草期间树上飞大规模 shishi→myia 改名扫荡(24→271
      未提交项:pyproject 包名、workflow 资产前缀、README、myia-classifier
      目录等);实施前先等/取扫荡后基线,本档 ASCII 前缀按 myia 落。
      → 扫荡实况已记 prd Constraints;终检实读 pyproject/uv.lock diff=ocrmac
      标记最小侵入+改名残余(叠加式成立)
- [x] 0.3 确认 `desktop/src-tauri/icons/icon.ico` 存在(84,679 B,2026-10-03)。
      → 终检复跑 `ls -la`:84,679 B 在位

## 阶段 1:F1 依赖根因修复

- [x] 1.1 `pyproject.toml` vision extra:`"ocrmac>=1.0"` →
      `"ocrmac>=1.0; sys_platform == 'darwin'"`(带注释:macOS Vision 独占,
      Windows 无 wheel,CI run 37117015528 实锤)。
      → 终检实读 pyproject.toml:50 marker + :47 注释在位
- [x] 1.2 重锁(镜像 env 保 URL 体系):
      ```bash
      UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv lock
      ```
      `git diff uv.lock` 人工核:预期 diff 限于 ocrmac 条目 marker(+可能的
      hash 重排);超预期即停,回报告。
      **回滚点**:revert pyproject+uv.lock 两文件即可。
      → 终检实读:uv.lock:1979/2003 ocrmac marker;ocrmac sdist+wheel 两条 URL
      均 tsinghua(镜像体系不变)
- [x] 1.3 定向验证(mac 侧装配不回归):
      ```bash
      UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv sync --frozen --no-dev --extra vision --dry-run
      ```
      (零报错即锁与标记自洽;不真装,不动项目 .venv。)
      → 实施会话实跑 exit 0(验收记录表);终检批次经 uv export 断言 marker 行
- [ ] 1.4 (CI 侧最终验证留给阶段 4 的 windows job;本机无 Windows,不伪造。)
      → 如实:CI 侧未跑,归阶段 4(推 origin 首跑)

## 阶段 2:F2 打包配置

- [x] 2.1 `desktop/myia-core.spec`:ocrmac 的 collect_all 三行包进
      `if sys.platform == 'darwin':`(顶部已 import os,补 import sys)。
      → 终检实读 myia-core.spec:17-19 darwin 门在位
- [x] 2.2 `desktop/src-tauri/tauri.conf.json` `bundle.icon` 数组追加
      `"icons/icon.ico"`(保持 icns/png 原序,追加式)。
      → 终检复跑 json.load:`['icons/icon.icns','icons/icon.png','icons/icon.ico']`
- [x] 2.3 定向验证:
      ```bash
      python3 -c "import json;json.load(open('desktop/src-tauri/tauri.conf.json'));print('conf ok')"
      python3 -m py_compile desktop/myia-core.spec 2>/dev/null || desktop/.venv-build/bin/python -c "compile(open('desktop/myia-core.spec').read(),'s','exec');print('spec syntax ok')"
      ```
      → 终检复跑:conf ok + py_compile ok
- [x] 2.4 mac 侧 sidecar 构建不回归(AC6;产物大小同量级):
      ```bash
      cd desktop && bash build-sidecar.sh aarch64-apple-darwin && ls -la src-tauri/binaries/
      ```
      (耗时 ~分钟级;失败即 F2 引入回归,回滚点=两文件 revert。)
      **回滚点**:spec + tauri.conf.json 独立可退。
      → 实施会话 exit 0,产物 124,059,712 B(验收记录);终检核磁盘产物在位
      124,120,784 B(11:57 时间戳,大小同量级)

## 阶段 3:F3 workflow 重构(desktop-release.yml)

- [x] 3.1 dispatch 版本入参:`on.workflow_dispatch.inputs.version`(required:
      false)+ 各 job VERSION 解析改为「inputs.version || ref_name#v,非 semver
      时回退 `jq -r .version src-tauri/tauri.conf.json`」。
- [x] 3.2 macos-dmg job:latest.json 生成/上传两步移出;新增 upload-artifact
      (`mac-updater`:myia.app.tar.gz.sig——前缀随改名扫荡后现行口径);其余
      步骤(守卫/构建/ASCII 改名/挂 dmg+tar.gz+sig)不动;所有 Release 上传步加
      `if: startsWith(github.ref, 'refs/tags/')`。
- [x] 3.3 windows-msi job:删 `continue-on-error: true`;加 `timeout-minutes: 60`
      (grill R2-D6c);删原 softprops 上传步;新增「产物清单(诊断)」「产物改
      ASCII 名」(msi-updater/ → `myia_${VERSION}_x64.msi`/`.sig`,glob 以清单
      日志为准)两步 + upload-artifact(`win-msi`);job 内无 Release 上传步
      (挂载全归 3.4 归聚 job)。
- [x] 3.4 新增 release-finalize job(grill R2-D6 三修后形态):
      `runs-on: ubuntu-latest`(jq 预装)+ `needs: [macos-dmg, windows-msi]` +
      `if: always() && needs.macos-dmg.result == 'success'`;download 两 artifacts;
      写 latest.json(darwin-aarch64 恒在 + windows-x86_64 条件并入,URL 指
      ASCII 资产名);latest.json 无条件 upload-artifact(`latest-json`——dispatch
      循环可复核生成逻辑);softprops 两步(win 在则挂 msi+sig;挂 latest.json)
      各加 `if: startsWith(github.ref, 'refs/tags/')`,**job 本体不整体 tag 门**。
- [x] 3.5 头部注释「已知边界」段更新(Windows 正式目标;latest.json 单写者;
      手工补条目降级为应急路径)。
- [x] 3.6 定向验证:
      ```bash
      python3 -c "import yaml;d=yaml.safe_load(open('.github/workflows/desktop-release.yml'));print(sorted(d['jobs']))"
      # 期望:['macos-dmg','release-finalize','windows-msi'] 且 yaml 可解析
      actionlint .github/workflows/desktop-release.yml
      # grill R2-焦点1 补:actionlint 1.7.12 在装(/opt/homebrew/bin),覆盖 run 块
      # shellcheck(脚本 dry 逻辑的语法面)+ needs 引用 + 表达式错误;基线文件
      # 实测 clean(2026-10-04 本会话跑过),改后仍须 clean。
      ```
      → 终检复跑(2026-10-04):jobs=`['macos-dmg','release-finalize','windows-msi']`;
      windows-msi 无 continue-on-error、timeout-minutes=60;dispatch inputs=
      ['version'];actionlint exit 0 clean;实施会话另跑 workflow 静态断言 34 PASS
      + dry D1/D2/D4(fake bundle 树/latest.json 双分支)30 PASS(证据在 evidence/)

## 阶段 4:dispatch 验证循环(本任务的「CI 绿」证据)

- [ ] 4.1 分支含全部改动后:
      ```bash
      gh workflow run desktop-release.yml -R xinzhuzi/shishi --ref <任务分支>
      gh run watch <run-id> --exit-status  # 或轮询 gh run view
      ```
      (长任务纪律:后台跑 + 轮 gh,不 sleep 轮询。)
- [ ] 4.2 判据:windows-msi job conclusion=success(AC2);日志含 bundle 目录
      清单(3.3 的诊断步);artifacts 含 win-msi(myia_*_x64.msi+.sig)+
      latest-json(latest.json 内容人验:mac 条目恒在、win 条目并入、URL 指
      ASCII 资产名——AC4 的 dispatch 侧证据)。
- [ ] 4.3 失败迭代:按日志修(预期雷区=msi/msi-updater 命名、WiX 对世事
      ProductName 的编码容忍、rapidocr 收编路径;处置见 design §6 风险表),
      每轮多点并修再 dispatch;**不上 tag 直到 dispatch 绿**。
- [ ] 4.4 绿后回填:run URL + 产物清单记入 prd「验收记录」节(新增)。
      **回滚点**:workflow 单文件 revert 即回旧态(允许失败),mac 链两态等价。
      → 如实(2026-10-04 终检):4.1-4.4 全未跑——CI 真跑前提=分支推 origin,
      留推后首跑(主人/后续会话);静态/dry 替代证据见 3.6 注记与 evidence/

## 阶段 5:F4 文档

- [x] 5.1 README「下载安装(桌面应用)」节:macOS 小节后并列 Windows 小节
      (design §4.1 五要点;追加式,不动 macOS 文案)。
      → 终检实读 README:196-213 Windows(x64) 小节在位(SmartScreen 放行/
      Defender 误报/%APPDATA%\MYIA/首跑种子/msi passive)
- [x] 5.2 desktop/UPDATER.md:§3 Windows 段改自动化口径;§6 旧口径替换;
      与 workflow 头注释三方一致。
      → 终检实读 UPDATER §3(归聚单写者口径)/§6(Windows 正式目标条)在位
- [x] 5.3 真机冒烟清单(主人侧)落 prd「验收记录」上方的独立小节
      (design §4.3 六项;标注「主人侧,如实注记不阻交付」+ 口径双源注记)。
      → 终检实读:七项清单在 prd「真机冒烟清单」节(R2-D10 补第七项 DPAPI 链)

## 阶段 6:收口定向检查(全量门禁归脚本)

- [x] 6.1 `python3 -c "import json;json.load(open('desktop/src-tauri/tauri.conf.json'))"`
      (2.3 已跑,终态复跑)。
      → 终检复跑 ok
- [x] 6.2 阶段 3.6 的 workflow yaml 解析复跑。
      → 终检复跑 ok(jobs 三元组 + dispatch inputs 断言)
- [x] 6.3 README/UPDATER 改动 `git diff` 通读(仅文档面,无代码面)。
      → 终检通读:README/UPDATER diff 均文档面(README 余量 hunks 属并行改名波)
- [x] 6.4 明确不在本任务跑的:全量 pytest(归脚本统一门禁;且本任务零 Python
      行为变更,pyproject marker 对 mac 侧测试无影响——uv sync --frozen dry-run
      已在 1.3 验证锁自洽)。
      → 全量 pytest 由三任务终检批次统一实跑:3495 passed/0 failed(2026-10-04)
- [x] 6.5 检视共享热点文件零触碰:`git status` 确认 desktop/entry.py /
      src/myia/schema.py / tests/test_desktop_sidecar_protocol.py /
      desktop/ui-src 无本任务改动。
      → 终检核对:本任务改动面=pyproject/uv.lock/myia-core.spec/tauri.conf/
      desktop-release.yml/README/UPDATER(+本档);entry.py/schema.py/协议测试/
      ui-src 树上在途改动均归属 b234/改名波/hermes-cron 波,非本任务

## 完成判据(与 prd AC 对应)

| AC | 阶段 | 证据形态 |
|---|---|---|
| AC1 | 1 | pyproject diff + uv.lock marker + windows job 的 uv sync 步绿 |
| AC2 | 4 | dispatch run URL,jobs 结论 |
| AC3 | 2/4 | conf diff + macos-dmg job 绿 |
| AC4 | 3/4 | artifacts 清单 + (tag 后)Release 资产与 latest.json |
| AC5 | 5 | README/UPDATER diff |
| AC6 | 2/6 | mac sidecar 构建产物 ls + dispatch 版本回退日志 |
| AC7 | 4/5 | 验收记录回填;归档留主人 |

# 交付报告:插件分发新规范——声明随包、源码远取(10-06-plugin-src-remote-fetch)

> 收尾员 2026-10-06 · task.json 已置 review · 主人令:「是这些源码不能随包,但是这些配置可以」
> 勾选纪律:亲跑/亲验=勾并注据;commit 记录在档=引注;未做/不可考=如实记,不虚构。

## 1. 一句话结果

规范三线中两线半落地并全绿入库(打包收窄✅、安装远取链✅、兼容三层✅),**批4 发布链(真锁产出)整批未做**——AC6 不勾、AC1 锁面缺;批3 收窄已进 main 而锁未进,**下一个发布动作前批4 必须落地,否则收窄包内 9 件源码型插件点装将结构性 `plugin_lock_missing`**(批序铁律「同船发布」的意义即在此,见 §8 留主人)。

## 2. 各阶段与 commits 对账(地面对账)

| 阶段 | commit | 时间 | 内容摘要 |
|------|--------|------|---------|
| 立档 | (未单独提交,档随收尾笔入 git) | 21:39-21:43 | prd/design/implement 三件套;D1-D8 全按推荐自决标可翻案 |
| 批3 打包净化线 | `0c624c4` | 22:04 | tauri.conf.json resources 11 组件包收敛两声明件映射;test_installer_resources.py 门禁反转(INV-1~3 入 docstring);真构建实证 564K→204K/52→32 件 |
| 批1+批2 安装远取链 | `9f2dc9a` | 22:18 | 新模块 src/myssia/plugins/remote.py(锁 schema/fetch/sha256/安全解包/编排);manifest.py install.source 内容寻址化;entry.py 三岔编排;测试 45+9 例全 mock |
| 深审修复批 | `cb09dda` | 22:42 | 四发现修复:size 前置对账/digest 严格口径/声明面漂移告警/__pycache__ 污染拒;全量 4873 过 |
| 批5 装机验证 | (无 commit,evidence 不入 git 按主人收尾令) | 23:02-23:14 | 干净树沙箱构建 BUILD-EXIT=0 + 截图 5 张(收尾员未亲读像素,§6) |
| 收尾 | 本轮两笔 | — | 任务档现状笔 + 收尾文档笔(spec 三处/AC 勾选/报告/task.json review);排除 evidence(笔A 亦排除 reports) |

**源码残留对账**:`git status` 工作树除本任务档未跟踪外零改动——本任务源码全部随三 commits 入库,零残留零补提交需求;任务档按主人令入 git(见 §7 提交注记)。

## 3. 门禁

**收尾轮亲跑(2026-10-06,当前 HEAD=cb09dda)**:

| 门禁 | 命令 | 结果 |
|------|------|------|
| 定向三文件 | `uv run --no-sync pytest -q tests/plugins/test_plugin_remote_fetch.py tests/desktop/test_bundled_plugins_install.py tests/desktop/test_installer_resources.py` | **136 passed**(0.39s) |
| 全量 pytest | `uv run --no-sync pytest -q` | **4873 passed, 40 skipped**(113.33s) |
| ruff | `uvx ruff@0.16.10 check .` | **All checks passed** |
| 包面键空间 | `find <验证包>/Resources/plugins -type f` / `-name "*.py"` | 恰 32 件=10 声明 YAML+11 包×2;`*.py` **计 0**;零 vendor/credhunter 子包/__pycache__;plugins.lock.json 缺席(批4 佐证) |

**各阶段 commit 记录门禁(收尾轮未复跑,引 commit 消息)**:批3=test_installer_resources 49 测+pyenv 两文件 31 测+cargo check/test --locked 80 过+vitest 577/577;批1+2=全量主树 4867 过+干净 worktree 4863 过+ruff 五文件;深审批=两测试文件 87 passed+全量 4873 过+ruff 四文件+GitNexus impact 三符号全 LOW。vitest/cargo 面收尾轮未复跑(无源码改动于彼面,批3 记录在案)。

## 4. 深审批(cb09dda)

四发现全修,全测试钉死:

1. **锁 size 前置对账**:install_remote 在 verify_sha256 前加 `len(payload)==asset.size` 门,不等即 `integrity_mismatch`(data 带 expected_size/actual_size/url)零残件早拒——锁 size 字段不再是纯声明。
2. **digest 严格口径**:verify_sha256 删 `strip().lower()` 宽容归一化,大写/带空白/带换行 digest 一律拒;与锁 `_check_sha256`/manifest `SHA256_HEX_RE` 双处口径统一。
3. **声明面 digest 漂移告警**:解包后 store.install 前新 `_warn_declared_digest_drift`(纯告警零门);顺带实证「发布脚本同源回填 manifest.install.sha256」在自包含 tarball 形态下**自指不可行,批4 落地需另裁**。
4. **`_bundled_dir_carries_source` 收紧**:「子树存在 *.py」判定——纯声明件目录混入 __pycache__ 不再误判旧包直拷(装出缺 adapter 空壳件),归 `plugin_lock_missing` 结构化拒;D3 旧包回退六形态实测复验保住。

**不随本笔(如实)**:深审 medium 两条(坏包窗口门禁:「锁必须在」负断言)——现在加必红 main(锁不存在),随批4 真锁同船。

## 5. 五流程(批5 装机验收步骤1)对账——不可考如实记

| # | 流程 | 状态 |
|---|------|------|
| ① | 设置页随包插件卡 11 件全可见 | 截图留痕(pkg-plugins-*.png ×4 + pkg-settings.png,23:10-23:14);**收尾员模型无图像输入未亲读像素**,以实施员留痕身份入档 |
| ② | 点装真网真装 | **无回执在档**;且真锁缺席(批4)下远取成功路径不可能真机验——mock 端到端已钉死(test_bundled_plugins_install 远取主路径含 list 已装态对账) |
| ③ | 断网点装→结构化错可见 | **无回执在档**;mock 面四态拉取失败全测(plugin_fetch_failed 带 status) |
| ④ | 已装件零扰动逐字节比对 | **真机无回执**;mock 面「已装旧件跨成功+失败+列表+卸他件四操作逐字节零扰动」测试在档(9f2dc9a) |
| ⑤ | 卸载重装循环 | **无回执在档**;卸载语义 INV-6 store 契约零改动+全量绿佐证 |

## 6. 装机证据(evidence/,按主人收尾令不入 git)

- `pkg-build.log`:干净树 /private/tmp/myia-pkg-verify/clean 全链构建(clean:pycache→vite→cargo release 39.53s→bundle),**BUILD-EXIT=0**,世事.app 17.31 MiB;构建产物包面收尾轮亲验见 §3。
- `pkg-settings.png`/`pkg-plugins-{full,mid,tail,tail2}.png`:设置页与插件列表截图(实施员留痕,收尾员未读像素)。

## 7. spec 落地(收尾笔,AC7)

1. **`.trellis/spec/domain/connector-selection.md`**:硬规则节追加「**插件源码不随包:装机包只带声明(plugin.yaml/README),adapter/vendor 按需远取落数据根**(判例 2026-10-06)」——含锁机制/回退语义/myssia-src 例外/门禁指针(主人收尾令指定原文)。
2. **`.trellis/spec/desktop/sidecar-protocol.md` #64**:旧「目录映射→直调 store」描述与 9f2dc9a 三岔编排漂移,核对抓出并同步(远取主路径/旧包直拷回退/plugin_lock_missing 三岔+失败词表)。
3. **`.trellis/spec/domain/security-baseline.md`**:Plugin 节补「插件源码远取链完整性门」(锁双门:size+sha256 严格口径/解包成员白名单/.staging 清残零半装)。

## 8. AC 对账与遗留留主人事项

**AC 对账**:AC2/AC3/AC4/AC5/AC7 ✅ 勾(亲跑+commit 双据);AC1 ❌ 不勾(前两句全验+门禁钉死,唯「根级 plugins.lock.json」随批4);AC6 ❌ 不勾(批4 整批未做)。明细见 prd §4 勾选注记。

**留主人(按优先级)**:

1. **【发布硬前置】批4 发布链整批**:`desktop/scripts/release-plugins-lock.mjs`(git archive 逐件产资产,双保险断言 vendor//__pycache__/*.pyc 不入)+ justfile `release-plugins` 目标 + 真锁产出 + 锁映射进 tauri.conf.json + 锁覆盖门禁 + 发布文档。**批3 收窄已进 main:收窄包内 9 件源码型插件无直拷源码,锁缺席即 plugin_lock_missing——批4 不落地则下一个发布动作必产出「插件装不上」的包**(批序铁律「同船发布」的现压力点)。
2. **深审 medium 两条**(「锁必须在」负断言门禁):随批4 真锁同船加。
3. **manifest.install.sha256 回填方案另裁**:深审批实证自包含 tarball 形态下发布脚本同源回填自指不可行(cb09dda);批4 设计时需另裁(如产锁后二次回填重打包,或接受声明面漂移告警语义)。
4. **批5 真机五连(②-⑤)随真锁后补**:真锁+资产上传后按 implement 批5 步骤1 补真机验收(静默铁律 MYIA_SMOKE_GEOMETRY)。
5. **D6 可翻案加急件(纯文档)**:21 处 plugin.yaml `install.source` 旧 myia.git URL 批量改 shishi(机器事实源=锁,不影响功能)。
6. **D5 增强批留后续**:vendor 点装即全功能(manifest vendor.pin 直连上游 tar.gz 链接者形态)。

## 9. 提交注记

笔A(任务档现状):prd/design/implement/task.json/check.jsonl/implement.jsonl 执行期快照(排除 evidence/ 与 reports/)。笔B(收尾文档,detect-changes 豁免类):spec 三处+prd AC 勾选+implement 回填+task.json review+本报告。绝不 push;evidence 大图(≈4.3MB×5)按主人令不入 git。

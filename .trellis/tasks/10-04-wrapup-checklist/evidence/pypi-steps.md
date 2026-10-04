# PyPI 双包 pending publisher 人肉步骤单 + Re-run 待命(10-04-wrapup-checklist 第一节 1)

> 生成:2026-10-04,PyPI 准备员(离线预检)。pypi.org 密码在主人手;TOTP 种子在钥匙串 `pypi.org-totp`、恢复码在 `pypi.org-recovery-codes`——本档生成过程未触碰任何钥匙串条目。步骤单每个字段值由 run 37195700263 的 OIDC claims 权威锚定,取证原文见文末第 4 节。

## 0. 一眼结论:登记四元组(两包各登记一条,除项目名外五字段全同)

| pypi.org 表单字段 | 精确值 | 依据 |
|---|---|---|
| PyPI project name | `myssia`(第 1 条)/ `myssia-classifier`(第 2 条) | 2026-10-04 定名终局(wrapup prd 第一节 1);双名在 pypi.org 与 test.pypi.org 均 404 = 未被占用(取证 #5) |
| Owner | `xinzhuzi` | OIDC claim `repository_owner`(取证 #3) |
| Repository | `myia` | OIDC claim `repository: xinzhuzi/myia`(取证 #3);`gh api` 实测仓库现名 = `xinzhuzi/myia`(取证 #1) |
| Workflow name | `pypi-publish.yml` | OIDC claim `workflow_ref: xinzhuzi/myia/.github/workflows/pypi-publish.yml@refs/heads/main`(取证 #3) |
| Environment | **`pypi`(必填,不要留空)** | OIDC claim `environment: pypi` 在场(publish job 声明 `environment: pypi`,pypi-publish.yml:250);PyPI 官方 troubleshooting:owner/repo/workflow filename/environment 四字段两侧必须一致("check if the workflow is using the same environment as configured when the publisher was configured on PyPI",取证 #7)——工作流带了 environment 而登记留空 = 不匹配 = invalid-publisher |

> ⚠️ **别照工作流文件头抄**:`.github/workflows/pypi-publish.yml:14-21` 注释块写的四元组是 `repository = myssia`,系「仓库拟改名 myssia」时期口径,已陈旧(仓库终名 myia)。登记以上表为准,即 OIDC claims 实测值。

## 1. 人肉步骤单(主人 2 分钟版,逐屏逐字段)

### 屏 1|登录 pypi.org

1. 浏览器开 `https://pypi.org/account/login/`,输入用户名 + 密码(密码在主人手,AI 无)。
2. 出 2FA「Enter two-factor authentication code」时:用你平时的出码工具,从钥匙串条目 **`pypi.org-totp`** 的种子出当前 6 位码。码 ~30 秒滚动;被拒就等下一个窗口的新码,勿复用旧码连试。
3. **Fastly 反自动化应对**:pypi.org 前置 Fastly,可能弹人机校验页("Verify you are human" / "Please stand by")或限流页(HTTP 429 "Too many requests")。应对:正常浏览器直开、等 30–60 秒再点一次、一分钟内不要反复提交登录;若 TOTP 被吞,重试时换下一窗口的新码。
4. 兜底:2FA 码不可用时用恢复码(钥匙串 `pypi.org-recovery-codes`,最后手段,消费一张少一张)。

### 屏 2|进入 Publishing 页

登录后右上头像 → **Account settings** → 顶部标签 **Publishing**;直达 URL:`https://pypi.org/manage/account/publishing/`。页面下方有 **Pending publishers** 表(现有挂起行都列在这)。

### 屏 3|添加两条 pending publisher(GitHub Actions 表单)

页面「Add a new pending publisher」区(GitHub Actions 是默认 tab),逐字段填:

| 字段 | 第 1 条 | 第 2 条 |
|---|---|---|
| PyPI project name | `myssia` | `myssia-classifier` |
| Owner | `xinzhuzi` | `xinzhuzi` |
| Repository | `myia` | `myia` |
| Workflow name | `pypi-publish.yml` | `pypi-publish.yml` |
| Environment | `pypi` | `pypi` |

每条填完点 **Add**。**成功预期**:绿色横幅(Successfully added a new pending publisher 量级),且下方 Pending publishers 表新增一行;两条加完 = 共提交两次。

- 若报 "there is already a pending publisher with these configurations" 类似文案 → 说明此前建过,转屏 4 核对旧行的 Repository 是否 `myia`,不是就删旧重加。
- 若报项目名相似被拒("too similar to an existing project")→ myia 当年就栽在 mypy 相似保护;myssia 表单此前实测可通过(journal 2026-10-04 在案)。若真被拒,**截图回话,勿连点硬试**(反复提交触发限流)。

### 屏 4|删旧行(shishi/myia→shishi→myssia 改名期遗留)

同一页 **Pending publishers** 表逐行核对:凡满足任一条件即删(行尾垃圾桶图标 → Delete 确认):

- Repository 列 ≠ `myia`(如 `shishi`、`myssia`——改名各时期口径);
- Project 列是旧项目名(`shishi` / `shishi-classifier` / `myia` / `myia-classifier`)。

**终态判据:表里恰好两行 = `myssia` 与 `myssia-classifier`,Repository 均为 `myia`,workflow=`pypi-publish.yml`,environment=`pypi`。**
若表本来就是空的(从未建成过)→ 直接跳过本屏。

### 屏 5(可选)|test-pypi 演练的前置,不做可跳

test.pypi.org 与 pypi.org **账号与登记完全独立**。2026-10-04 10:32Z 的 dispatch run 打的就是 test.pypi,同样 invalid-publisher(取证 #3)→ test 侧现无任何 publisher。要做演练:在 `https://test.pypi.org` 注册/登录(无账号需新注册+2FA),然后把屏 2–4 原样再做一遍(域名换 test.pypi.org)。
不做演练直接打正式也稳:三次 run 里 build+verify 两步全绿,唯一红点就是 publisher 登记;且 0.0.1 双端 404 = 版本从未落地、无覆盖风险(取证 #5)。

**完成即回话「建好了」,AI 执行第 2 节命令。**

## 2. Re-run 待命命令(主人回话后 AI 执行)

主命令(正式 PyPI,双包同发,OIDC,main 现行代码):

```bash
gh workflow run pypi-publish.yml --repo xinzhuzi/myia --ref main -f repository=pypi -f package=both -f use-api-token=false
```

观察(发布 run 约 1 分钟出结果):

```bash
gh run list --repo xinzhuzi/myia --workflow pypi-publish.yml --limit 1
gh run watch <run-id> --repo xinzhuzi/myia --exit-status
```

**绿判据**:publish job 绿;`https://pypi.org/project/myssia/` 与 `https://pypi.org/project/myssia-classifier/` 出 0.0.1。

test-pypi 演练选项(仅当主人做了屏 5 才可用):

```bash
gh workflow run pypi-publish.yml --repo xinzhuzi/myia --ref main -f repository=test-pypi -f package=both -f use-api-token=false
```

**为什么不是 `gh run rerun`(预检实测,两个旧 run 都不能 rerun)**:

- `37195700263`(10-04 dispatch 红 run):输入是 repository=**test-pypi** + package=**myssia-classifier**(log: `PACKAGE: myssia-classifier`、`上传目标:test-pypi → https://test.pypi.org/legacy/`),rerun 原样复用 → 打错索引 + 漏 myssia 主包。
- `37117015481`(10-03 v0.0.1 tag run):tag commit `96751a5a` 是 shishi 时代代码,build 实产 `shishi-0.0.1-*` / `shishi_classifier-0.0.1-*`(取证 #4)→ rerun 会以废弃名发布。

失败应急:

- 仍红 `invalid-publisher` → 对第 0 节四元组逐字段核(最常见:Environment 留空、Repository 误填 myssia/shishi);可对照本档第 4 节 claims 原文。
- 上传半途而废(PyPI 同版本禁覆盖)→ 该版本烧毁,处置 = bump 0.0.2 重发(勿再发 0.0.1)。

## 3. 成功后的已知后续(挂账,不在本次代办内)

- dispatch 发布**不触发** attach-release(仅 tag 事件,pypi-publish.yml:316)→ wheel/sdist 不会自动挂 GitHub Release v0.0.1;要挂可后续本地 `uv build` + `gh release upload v0.0.1` 补。
- `pypi-publish.yml:14-21` 头注释 `repository = myssia` 陈旧,待后续提交修正为 `myia`(本次零代码改动、不 commit)。
- 后续版本走 v* tag 流即含 attach-release;项目建成后 pending publisher 自动转正为项目 publisher,再发版无需重登记。

## 4. 预检取证(本档生成时实跑,命令+原文)

1. **仓库现名**:`gh api repos/xinzhuzi/myia` → `{"default_branch":"main","full_name":"xinzhuzi/myia","private":false}`(经 API 权威确认,现名 myia 非 shishi/myssia)。
2. **GitHub environment 已在**:`gh api repos/xinzhuzi/myia/environments` → `{"name":"pypi","protection":0}`。
3. **run 37195700263**(2026-10-04T10:32Z,workflow_dispatch,main@b8e20a2,31s 红):build 绿(仅 myssia-classifier:`PACKAGE: myssia-classifier`,实产 `myssia_classifier-0.0.1-py3-none-any.whl`/`myssia_classifier-0.0.1.tar.gz`);publish 红;`上传目标:test-pypi → https://test.pypi.org/legacy/`。OIDC 报错原文(`gh run view 37195700263 --log-failed`):

   ```text
   ##[error]Trusted publishing exchange failure:
   Token request failed: the server refused the request for the following reasons:
   * `invalid-publisher`: valid token, but no corresponding publisher (Publisher with matching claims was not found)
   ...
   * `sub`: `repo:xinzhuzi@13790359/myia@1399222178:environment:pypi`
   * `repository`: `xinzhuzi/myia`
   * `repository_owner`: `xinzhuzi`
   * `repository_owner_id`: `13790359`
   * `workflow_ref`: `xinzhuzi/myia/.github/workflows/pypi-publish.yml@refs/heads/main`
   * `job_workflow_ref`: `xinzhuzi/myia/.github/workflows/pypi-publish.yml@refs/heads/main`
   * `ref`: `refs/heads/main`
   * `environment`: `pypi`
   ```

   → test.pypi.org 侧**确证**无匹配 publisher(现行 claims 下)。
4. **run 37117015481**(2026-10-03T12:32Z,push tag v0.0.1@96751a5a,26s 红,即「最近一次 v0.0.1 发布 run」):`上传目标:tag 事件→固定 pypi → https://upload.pypi.org/legacy/`;build 绿,实产 `shishi_classifier-0.0.1.tar.gz`/`shishi_classifier-0.0.1-py3-none-any.whl`/`shishi-0.0.1.tar.gz`/`shishi-0.0.1-py3-none-any.whl`(jobs API 取 build 日志);publish 红 OIDC 同款 `invalid-publisher`,claims 为 `repository: xinzhuzi/shishi`、`ref: refs/tags/v0.0.1`、`environment: pypi`(当时仓名 shishi)。→ pypi.org 侧当时无 shishi 口径 publisher;改名 myia 后的现行口径未在 pypi.org 试过(主人登记尚未做,见 wrapup prd 第一节 1)。
   另:37115937696(10-03 10:17Z)红在 verify 脚本旧名 glob,未到 publish,与登记无关。
5. **双包名双端未占用**:`curl -o /dev/null -w '%{http_code}' https://pypi.org/pypi/{myssia,myssia-classifier}/json` → 双 404;test.pypi.org 同法双 404。零成功发布在案。
6. **版本与触发**:两 pyproject 均 `version = "0.0.1"`(pyproject.toml:7、myssia-classifier/pyproject.toml:7);工作流触发 = `push.tags:["v*"]` + `workflow_dispatch`(inputs:repository=test-pypi|pypi、package=myssia-classifier|myssia|both、use-api-token 布尔);`git diff` 实测 origin/main == 本地 HEAD,pypi-publish.yml/双 pyproject 三件无差异(dispatch 即跑现行 myssia 代码)。
7. **environment 必填依据**:PyPI 官方 troubleshooting(https://docs.pypi.org/trusted-publishers/troubleshooting/,报错信息自带的排错链接):"check if the workflow is using the same environment as configured when the publisher was configured on PyPI";并要求 `repository_owner`/`repository`/workflow filename/environment 两侧一致。结合 claims `environment: pypi` 在场 → 登记必须填 `pypi`。

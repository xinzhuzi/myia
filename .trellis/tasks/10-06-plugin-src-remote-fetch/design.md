# design.md — 10-06-plugin-src-remote-fetch 技术设计(执行级)

> 决议出处:prd §5(D1~D8,全按推荐自决、可翻案);本档把决议落到模块/契约/测试级。

## D1 总形态(三面改动,一张图)

```
发布期(release prep,发布机):                     装机期(用户机,零 Rust 改动):
  plugins/<id> ──tar──> dist/plugin-<id>.tar.gz      Resources/plugins/
       │ sha256                │ gh release upload     ├─ <id>/plugin.yaml + README.md   ← 声明(离线可见)
       ▼                       ▼                       ├─ plugins.lock.json             ← 锁(内容寻址事实源)
  desktop/resources/plugins.lock.json ──tauri resources──┘
                                                      点装 plugins.bundled.install {id}
                                                        → 读锁 → httpx GET url
                                                        → sha256 校验 → 安全解包 .staging/
                                                        → InstalledPluginStore.install(同门)
                                                        → ~/.myia/plugins/<id>(原子落位)
```

- **锁缺席回退**(D3):旧包(包内有源码、无锁)→ 现行 `_locate_bundled_plugin_dir` + `store.install(source)` 直拷路径原样走,零改动零删除。
- **dev 形态**:env 不注入 → `bundled_plugins_unavailable` 原样;仓库内开发用 CLI `myssia plugin install plugins/<id>`(cli.py:4519)零变化。

## D2 远取载体选型(D1 决议的论据,实测数)

| 方案 | 实测/事实 | 裁 |
|------|-----------|----|
| **A. per-plugin release 资产 tar.gz + 锁钉 tag+sha256** ✅ | 单件 KB~百 KB 级(最大 credhunter 压缩后预计 <100K);repo 已有 release 面与 gh 流程;合主人「release tag + sha256」原话;与 runtime-manifest.json(url+sha256+archive)同构判例 | 采纳 |
| B. 整仓 codeload tar.gz(ref=commit sha) | `git archive --format=tar.gz HEAD` 实测 **68MB**(含 .trellis 归档证据图/demo 视频等);每装机首次拉全仓不可接受,且无每件完整性粒度 | 弃 |
| C. git fetch 按 sha(含 submodule) | 需用户机 git 二进制(Windows 装机不保);submodule 二跳拉取慢且不可钉 tar 字节 | 弃 |

资产命名:`plugin-<id>.tar.gz`(如 `plugin-myssia-proxy.tar.gz`),内容 = `plugins/<id>/` 目录树(打包时排除 __pycache__/.pyc;credhunter 含自有 credhunter/ 子包;osint/theharvester 不含 vendor/,D5)。资产 URL 形:`https://github.com/xinzhuzi/shishi/releases/download/<tag>/plugin-<id>.tar.gz`。

## D3 锁契约(D2)

新核心模块 `src/myssia/plugins/remote.py`(D4)内以 pydantic 定义(prd R3):

```json
{
  "manifest_version": 1,
  "repo": "https://github.com/xinzhuzi/shishi",
  "tag": "v0.0.2",
  "generated_at": "2026-10-06T00:00:00+08:00",
  "assets": {
    "myssia-proxy": {"url": "https://github.com/xinzhuzi/shishi/releases/download/v0.0.2/plugin-myssia-proxy.tar.gz",
                      "sha256": "<64hex>", "size": 4096, "version": "1.0.0"}
  }
}
```

- `version` 冗余自资产内 plugin.yaml(装机预显用,装机后以实拉 manifest 校验为准——锁只作发现面提示,不放松 store 校验)。
- 校验规则(载入即拒,结构化 `plugin_lock_invalid`):tag 非空、sha256 严格 64-hex、url 必须以 `{repo}/releases/download/{tag}/` 前缀开头(锁内自洽,防锁字段互相矛盾)、size>0。
- 落包:tauri.conf.json resources 增一行 `"../../desktop/resources/plugins.lock.json": "plugins/plugins.lock.json"`;sidecar 经 `MYIA_BUNDLED_PLUGINS` 目录(即 Resources/plugins)同目录读 `<root>/plugins.lock.json`——**零 Rust 改动**(pyenv.rs:241 `bundled_plugins_dir` 已指向该根)。

## D4 远取模块(src/myssia/plugins/remote.py)

```
load_plugins_lock(root: Path) -> PluginsLock | None      # 缺文件=None(回退语义);坏文件=PluginLockError(plugin_lock_invalid)
fetch_plugin_asset(entry, *, timeout) -> bytes            # httpx 同步客户端(trustenv 沿系统代理);非 2xx=PluginFetchError(plugin_fetch_failed, data 带 status/url)
verify_sha256(payload, expected) -> None                  # 不符=IntegrityMismatch(integrity_mismatch, data 带期望/实得)
extract_staging(payload, staging_dir) -> Path             # tarfile 解包:py>=3.12 filter="data"(3.11 fallback 手工防穿越:拒绝对路径/../symlink);成员须落在唯一顶层前缀 plugins/<id>/ 下并剥壳(staging 根=包根);非法定名=PluginArchiveError(plugin_archive_invalid)
install_remote(lock, plugin_id, store, *, force) -> dict  # 编排:fetch→verify→extract→store.install(staging_dir, force=force);任一失败清 .staging 残目录再抛
```

- 错误面全走 `PluginStoreError` 子类(code/中文 message/结构化 errors),entry.py 侧沿现模式包成 `ProtocolError` 透传(desktop/entry.py:1044-1050 同款)。
- 暂存(D8):`<install_root>/.staging/<id>-<4hex 随机>/`,与安装根同文件系统;`store.install` 现为 copytree(installed.py:336),staging 命中失败由 `install_remote` finally 清残——**不改 store**。
- httpx 为核心既有依赖(pyproject `httpx[socks]>=0.27`),零新依赖(核心依赖红线)。

## D5 entry.py 安装编排改造(desktop/entry.py `_m_plugins_bundled_install`)

```
root = _bundled_plugins_root()
if root is None: → bundled_plugins_unavailable(原样)
id/force 校验(原样 _PLUGIN_ID_RE 门)
lock = load_plugins_lock(root)
if lock is not None and id in lock.assets:
    result = install_remote(lock, id, InstalledPluginStore(ctx.install_root), force=force)   # 新主路径
elif <root>/<id> 目录含 adapter.py 或任意源码件:   # 旧包回退(D3)
    → 现行 _locate_bundled_plugin_dir + store.install(source) 直拷(零改动)
else:
    → ProtocolError("plugin_lock_missing", …)   # 新包但锁没条目 = 结构化拒,不静默不虚构
应答 {ok, dir, version} 契约不变
```

- `plugins.bundled.list` / `uninstall` / `category_install` **零改动**(声明仍在包内,发现面照常;卸载是安装根操作本就不依赖包内源码)。
- UI(bundled-plugins-card.tsx):安装按钮错误面沿现 ProtocolError 渲染路径;仅补一条文案级提示「源码型件安装需网络」(批4 核对现 error 渲染是否已足,足则零 UI 改动)。

## D6 打包改造(tauri.conf.json)

- 11 组件包逐件收敛为两行映射(plugin.yaml/README.md);删 adapter.py ×9、render_crawl4ai.py ×1、credhunter/ 整目录 ×1。
- 品类 YAML 10 件、demo、fixture plugin.yaml、myssia-src 五映射、runtime-manifest/requirements-lock/components.json:全部**不动**(INV-4 + 「配置可随包」)。
- beforeBuildCommand `npm run clean:pycache` 保留(纵深防御,虽然逐文件映射已天然排除)。

## D7 发布前置脚本与 justfile(AC6)

- 新脚本 `desktop/scripts/release-plugins-lock.mjs`(node,与 clean-pycache.mjs 同目录同形态;不需 Python env,发布机免 uv):
  1. 逐件 `git archive --format=tar.gz -o dist/plugin-<id>.tar.gz HEAD plugins/<id>`(11 件循环)。**必须 git archive 而非文件系统 tar**:文件系统 tar 会把工作树未跟踪件一并打进——__pycache__ 之外最关键是 osint/theharvester 已 init 的 submodule 工作树(vendor/Photon、vendor/theHarvester 全量 GPL 源码)会被整体裹进资产,越分发红线;git archive 只出 tracked 文件,submodule 以 gitlink 存在、内容天然不进资产。git archive 字节确定性(commit id 进头、mtime=commit 时间)保证同 commit 重跑同 sha256。脚本内加双保险断言:资产成员表不得含 `vendor/`、`__pycache__`、`*.pyc`;
  2. 计算 sha256/size,写 `desktop/resources/plugins.lock.json`(repo=shishi,tag=argv 传入);
  2b. 资产路径形:`plugins/<id>/…`(git archive 带仓库相对前缀)——`extract_staging` 按此前缀剥壳(staging 根=包根,plugin.yaml 落顶),见 D4 注;
  3. `gh release upload <tag> dist/plugin-*.tar.gz --clobber`。
- justfile 新目标 `release-plugins tag=<tag>`(纯门面,透传退出码);`build-desktop` 不自动串(发布是显式动作,避免日常构建误传资产)。
- 幂等:重跑即重产重传(资产覆盖语义 gh --clobber;sha256 变化随锁同步)。

## D8 门禁与测试设计(全 mock 零网络,repo 纪律)

| 面 | 文件 | 内容 |
|----|------|------|
| 打包合规(反转) | tests/desktop/test_installer_resources.py | 11 件 × {plugin.yaml, README.md} 必须在;`*.py`/vendor/credhunter 子包/__pycache__ 映射必须在 resources **键空间不存在**(负断言遍历全 map);模块 docstring 重写为新规范(AC7);品类/运行时面断言原样保留 |
| 锁覆盖 | 同上文件或新 tests/desktop/test_plugins_lock.py | 锁 11 件全覆盖;tag/sha256(64hex)/url 前缀自洽;resources 有锁映射 |
| 远取单元 | 新 tests/plugins/test_plugin_remote_fetch.py | httpx MockTransport:2xx/404/超时;sha256 对/错;夹具 tar.gz 好/坏(zip-slip 恶意件拒);staging 清残;编排成功路径落 store |
| 安装编排 | tests/desktop/test_bundled_plugins_install.py(扩展) | 新路径(锁在+条目在)走远取;旧包回退(锁缺+源码在)直拷;新包无条目→plugin_lock_missing;已装未 force 拒;uninstall 不受影响 |
| dev 通道 | 既有测试 | 跑全量不红即证(pytest 全量门禁) |

门禁口径:`uv run --no-sync pytest -q`(全量)+ ruff + `tsc -b && vite build`(若 UI 有改动)+ 装机外科验收(批5)。

## D9 风险与边界(承接 prd §7,补充设计级)

- **tar 名穿越**:extract_staging 显式成员白名单校验(成员路径必须相对、不得含 `..`、不得 symlink;py3.12 `filter="data"` + 3.11 手工双保险)。
- **锁与资产漂移**:资产重传后旧锁 sha256 失配 → integrity_mismatch(设计内);发布流程文档写明「动插件源码必重跑 release-plugins」。
- **httpx 超时**:fetch 钉 timeout(缺省 60s,小资产足够);UI 层不新增取消面(点装是短动作)。
- **Windows**:tar.gz 解包 tarfile 跨平台;路径处理全 pathlib;gh/tar 仅发布机需要。

# 装机回执(F5 装机包刷新换装段;打包安装员子代理,2026-10-11)

> 本文件只记装机事实(打包安装员产出);F5 复选框归主会话勾选,本档不代勾。
> 打包 HEAD = `0c9e3ec`(工作树干净,含本档时点全部五笔:af4f1d0/58c0410/469da88/0c9e3ec 等)。

## 1. 门禁(全绿,本会话亲跑)

| 门禁 | 命令 | 结果 |
|---|---|---|
| pytest 全量 | `just test`(TZ=Asia/Shanghai) | **5309 passed / 44 skipped / 0 failed**(152.45s) |
| vitest | 同上第二步 | **744 passed**(35 文件) |
| ruff + tsc/vite build + cargo check | `just check` | exit 0 全绿(chunk>500kB 警告既有非致命) |

## 2. 打包(按仓库自配方;PyInstaller sidecar 链已退役见 desktop/build-sidecar.sh 头注)

- 命令:`just build-desktop`(`npm --prefix desktop run tauri build`;beforeBuildCommand 链 clean:pycache + vite 前端)。
- 产物:`desktop/src-tauri/target/release/bundle/macos/世事.app` **17.92 MiB** + `dmg/世事_0.0.3_aarch64.dmg` 8.14 MiB(2026-10-11 22:09,二进制链接 22:09:32)。

## 3. 新包源验证(换装前,先验源再删旧——判例)

- **随包 Python 源逐字节一致**:`diff -rq <新包>/Contents/Resources/myssia-src/myssia src/myssia` 零差异;`entry.py` `cmp` 一致。
- **内嵌 UI dist 按字节特征验**(裸 grep 无效,Tauri 2 把 frontendDist 以 brotli 压进 MYIA 二进制;借调 `desktop/ui-src/e2e/package_smoke.py::extract_embedded_dist` Mach-O 胖指针+brotli 解压):解出 6 件(index.html/1 css/myssia-icon.svg/3 js),标记命中 **微信本机×5 / weixin_local×6 / wechat_local×5 / AX 权限×1**——F3 双卡+F4 只读入口确在新包。
- codesign:`adhoc, linker-signed`;`--verify --strict` 报「code has no resources…」为构建固有告警(源包同报,journal-1.md:599 判例),非换装引入。

## 4. 换装(2026-10-11 22:13,静默;回执 /tmp/wx-install-1011.{log,exit}=「ok installed」)

| 项 | 值 |
|---|---|
| 现装(换装前记录在案) | `/Applications/世事.app` 0.0.3,MYIA 二进制 inode=324014921,mtime **2026-10-11 21:49:34**,size 14,483,696,总 21M(不含 469da88/0c9e3ec;谱系⊆0c9e3ec,覆写零损失) |
| 退出 | `osascript quit app id com.myssia.app`(温和,零夺焦),MYIA 退净,托管 python serve 随 stdin EOF 自清 |
| 备份 | `mv` 保 inode → **`/tmp/世事.app.bak-wxui-221345`** |
| 覆盖 | `cp -R` 新包 → `/Applications/世事.app`;装后二进制与构建产物 `cmp` **逐字节一致**(新 inode=324108409,mtime 22:13:47,size 14,550,160) |
| 缓存清 | `rm -rf ~/Library/WebKit/com.myssia.app ~/Library/Caches/com.myssia.app`(判例铁律;`com.myia.app` 两路径本机不存在) |
| 复原 | `open -g` 后台静默拉起(零焦点;窗口缺省 visible:false 不弹窗)——MYIA pid 48118(22:15:10 起)+ 托管 python serve pid 48126,跑新包 |

## 5. 装机冒烟(装机包代码 + 托管 python 3.12.7,MYIA_HOME 沙箱)

- 注:ask 中「sidecar 二进制」形态已退役——现架构 sidecar = 托管 python `-m myssia_desktop_entry serve` + 随包 Resources 源码(desktop/src-tauri/src/pyenv.rs:6-8),冒烟按同口径跑包内代码。
- CLI:`PYTHONPATH=/Applications/世事.app/Contents/Resources/myssia-src MYIA_HOME=<沙箱> python3 -m myssia.cli cron list --json` → `{"count": 0, "jobs": []}` **exit 0**,data_root 锚定沙箱。
- **weixin_local 通道三态如实记录**(`myssia.wechat_local_sidecar.handle_wechat_local("probe", {})` 自装机包):
  ```json
  {"ok": false, "state": "bridge_unavailable", "checks": {"bridge_component": "missing"},
   "wechat_version": null, "bridge_version": null,
   "reasons": [{"code": "component_missing", "fix_hint": "到设置安装 wechat-bridge 组件(前置 brew install sqlcipher),或在品类 YAML 的 push 条目配 wechat_bridge_bin 指向桥 bin 路径"}]}
  ```
  = **bridge_unavailable(黄灰态)**:受管组件 wechat-bridge 本机未装机(`~/.myia/plugins/wechat-bridge` 与数据根均无),属 F5/B3 组件下载链的真机验证项,如实灰态不装死——UI 卡将显灰并带修复指引。
- 通道注册面:装机包 `myssia.push.CHANNELS` 含 `weixin-local`,**总数 33**,与 F1 批注一致;`myssia/push/weixin_local.py` 自装机包路径载入。
- 随包种子:Resources/plugins 25 项在位。
- 静默面:全程零合成点击、零窗口激活、零微信窗口开合;probe 零成本零内容读取(design §2 判据)。
- 未做(如实):`MYIA_SHOW_ON_START=1` 直跑亮窗验证(可选项,本轮取更静口径,未跑)。

## 6. 私有数据红线自查

本档零聊天内容、零密钥材料;证据只含计数/schema/状态码/路径与时间戳。

## 7. 组件装机回执(装机员子代理,2026-10-11 22:42;「全部解决」令装机端段)

> 清零 §5 的 `component_missing` 灰态:把受管组件 wechat-bridge 装到本机。
> `~/.myia/plugins` 是运行时目录不入 git;入库的只有组件源码侧改动。

### 7.1 装机前补源码侧部署脚本(commit `e39d8c5`)

- 实况:组件源码**缺 bin**——MYIA 消费点 `myssia.push.weixin_local.DEFAULT_BRIDGE_BIN` 指
  `~/.myia/plugins/wechat-bridge/bin/wechat-bridge`(weixin_local.py:85),源侧此前只有
  `entry: wechat_bridge/__main__.py` 包入口,无 bin 启动器。
- 补齐:`plugins/wechat-bridge/bin/wechat-bridge`(纯转接启动器,零业务逻辑):解析组件根 →
  `MYIA_WECHAT_BRIDGE_PYTHON` env > `<数据根>/python/bin/python3`(自管环境,数据根解析与
  `wechat_bridge.config.myssia_home` 同序)> PATH `python3`,选首个 **Python ≥3.11**
  (component.json requires)→ exec `python -m wechat_bridge`;失败 stderr+exit 2。
  本机实选 = 自管 python 3.12.7(`~/Library/Application Support/MYIA/python`)。
- component.json 补 `"bin": "bin/wechat-bridge"` 字段;README 补装机形态注记。
- 门禁:`uv run --no-sync python -m pytest tests/wechat-bridge -q` = **119 passed / 4 skipped**;
  `uvx ruff@0.16.10 check plugins/wechat-bridge tests/wechat-bridge` = All checks passed。

### 7.2 前置检测(design §5.1)与装机

- sqlcipher:**已装 4.19.0**(`/opt/homebrew/Cellar/sqlcipher/4.19.0`,localdb-e2e.md §2.1
  同款)→ 按口径跳过安装;`/opt/homebrew/opt/sqlcipher/bin/sqlcipher --version` 实跑报
  SQLCipher 4.19.0 community。
- 装机:`rsync -a --exclude __pycache__` 源目录 → `~/.myia/plugins/wechat-bridge/`+
  `chmod 755 bin/wechat-bridge`;装后 `diff -rq`(排 `__pycache__`)对源零差异。
  installed 语义(本组件消费面)= bin 在场且可执行(weixin_local.py:222 / wechat_local_sidecar.py:117
  的文件检查;pyenv_components 的 pip 指纹戳注册表不收录 bridge 类组件,不伪造戳文件)。

### 7.3 probe 三态前后对照(通道级 = `myssia.wechat_local_sidecar.handle_wechat_local("probe",{})`,装机包同口径)

| | 装机前(22:36 实跑) | 装机后(22:43 实跑) |
|---|---|---|
| state | `bridge_unavailable`(黄灰) | **`degraded`**(托盘态预期,非 unavailable) |
| checks | `bridge_component: missing`,其余无 | `bridge_component/wechat_process/ax_permission/localdb_storage` 全 `ok`;`main_window/ax_tree` `unknown`;`localdb_key` `unavailable` |
| versions | wechat/bridge 双 null | `wechat_version=4.1.15` / `bridge_version=0.2.0` |
| reasons | `component_missing`(装组件指引) | `key_unavailable`(D4 裁决指引;E1 定论如实) |

- 直跑 bin(`~/.myia/plugins/wechat-bridge/bin/wechat-bridge --probe`)exit=0,载荷与通道级一致;
  `main_window=unknown` 因自管 python 无 pyobjc Quartz(组件可选依赖,system_checks 设计行为:unknown 如实上报)。
- 补充取证:同 bin 以 `MYIA_WECHAT_BRIDGE_PYTHON=<仓库 venv>`(含 Quartz)实跑 →
  `main_window=fail`,reasons = `window_closed + key_unavailable` → 仍 `degraded`——托盘态完整语义
  (README「微信托盘态如实 degraded(window_closed)」)双路坐实。
- 通道错误族一条(真桥):`handle_wechat_local("query",{"chat_id":"filehelper","since_days":7})` →
  `WechatLocalSidecarError(code=key_unavailable)`,消息只含形状计数(行数=35 候选=5081 校验=101620
  命中=0/20 库,与 localdb-e2e.md §1.1 E1 实测同值)+ fix_hint 指引 D4 两案——sidecar 错误映射
  (exit 21 → 具名族)真机闭合。
- 静默面:全程零合成点击、零窗口激活、零微信窗口开合;probe/query 全只读(query 即 E1 的
  key_info.db 离线校验路径,零进程接触零出网)。
- 未做(如实):桌面 UI 卡亮窗目验(不碰运行中 MYIA app 的前台,probe 为按调执行,下次卡刷新即吃新态);
  localdb 真查询闭合仍挂 D4(keys.json 外部密钥引入即通,见 §7.3 错误族消息)。

## 8. D5 分发链换装回执(打包安装员子代理,2026-10-12 12:45;「都解决」令分发链验段)

> ask=Rust 安装器与 resources 都变(185484a)→ 按仓库配方全量重打包+静默换装+换装后真机验
> 分发链四件:随包注册表条目/设置页组件行可见(无头=resources 读取层)/pip 源码形态冒烟
> (独立 venv 装机包 Resources 内组件目录)/本机 `~/.myia/plugins/wechat-bridge` 0.3.0 不破。
> ask 中「sidecar PyInstaller+tauri build」为旧词——sidecar 冻结链 2026-10-05 已退役
> (desktop/build-sidecar.sh:2 档注),现配方 = `just build-desktop`(§2 同款),照此执行。
> tcc/截屏像素验证本轮不做(上轮已过,按 ask 只验分发链);task.json 勾选归主会话。

### 8.1 构建面三折(如实)

1. **首构阻断(HEAD=185484a 工作树净)**:`just build-desktop` exit 1——`tsc -b` 两错
   (`settings.test.tsx:69` fixture `paths` 项用旧名 `plugin`(types.ts:237 已改 `{category,path}`)、
   `sources/api.ts:446` 三元分支裸名 `plugin`(:442 声明已改 `category`))= 1920b6d 概念清词
   改名残留,该会话未重跑 `tsc -b`(vitest 不查型)。跨任务机械收口两行 → **bdaaf96**
   (tsc --force 零错+settings/sources 两屏 vitest 176p/11 文件+detect-changes 2 符号 risk=low)。
2. **打包卫生收口 → b9c5054**:bdaaf96 后构建产物实测——tauri resources 无排除语义把
   `plugins/wechat-bridge` 里 D5 会话本机 pip 冒烟遗留的 `build/`+`wechat_bridge.egg-info/`+
   `wechat_bridge/__pycache__`(3.12/3.14 双版本字节码)原样打进包;clean-pycache.mjs 缺省根
   漏了 D5 新随包第三棵树且垃圾规则不含 pip 工件——补齐(真树清理实跑 6 条目)+packaging 真跑
   测试扩 5 垃圾形+缺省根断言(11p)。
3. **主树构建遭并行在途混入 → worktree 判例**:b9c5054 主树构建成品(12:32:56)经
   `package_smoke.py::extract_embedded_dist`(Mach-O 胖指针+brotli)提取内嵌 dist,实测含
   `data-fullcanvas` 标记=并行 feed 会话提交前在途改动进了包(vite 构建窗口撞上其首次落盘;
   mtime 在换装后才更新是二次写,首写早于构建)。循 journal-1.md:598 判例转
   `git worktree add /tmp/myia-wxui-d5 b9c5054 --detach` 干净构建(ui-src npm ci+desktop
   npm install+tauri build,exit 0,12:40:06,18.10 MiB app+8.20 MiB dmg),worktree 产物
   复验:内嵌 dist 6 件零 `data-fullcanvas`、entry.py 与 worktree `cmp` 一致、随包源
   `diff -rq` 零差异、组件目录净五项;验毕 worktree 已 `git worktree remove --force` 清场。

### 8.2 换装(2026-10-12 12:45:51,静默;链日志 /tmp/wxui-d5-install.log)

| 项 | 值 |
|---|---|
| 现装(换装前记录在案) | inode=325428859,mtime **2026-10-12 12:37:13**——系并行 feed 会话 6f55129 的装机换装(commit 自述「装机重打包换装+重签」,12:37:13 落位,其内含 feed 详情整屏化特性;非我方任何产物,`cmp` 与主树/worktree 两包均不一致) |
| 退出 | `osascript quit app id com.myssia.app`(温和,零夺焦),MYIA 首轮探测即退净;serve 子进程随 stdin EOF 自清 |
| 备份 | `mv` 保 inode → **`/tmp/世事.app.bak-wxui3-124551`** |
| 覆盖 | `cp -R` worktree b9c5054 包 → `/Applications/世事.app`;装后二进制与构建产物 `cmp` **逐字节一致**(新 inode=325470154,mtime 12:45:51,size 14,533,472) |
| 缓存清 | `rm -rf ~/Library/WebKit/com.myssia.app ~/Library/Caches/com.myssia.app`(判例铁律) |
| 复原 | `open -g` 后台静默拉起(零焦点;窗口缺省 visible:false 不弹窗)——MYIA pid 38216 + 托管 python serve pid 38223,跑新包 |
| 竞态如实注 | 12:37 feed 会话换装与 12:45 本轮换装为双写(journal-1.md:601 双换装竞速同款):**现装 b9c5054 不含 6f55129 feed 详情整屏化**(该特性已入库,随下次任一会话装机刷新回归);本轮回执谱系 = b9c5054 worktree 包,cmp 锚点在案可随时复核 |

### 8.3 分发链四验(换装后真机,全过)

| 验 | 命令/路径 | 结果 |
|---|---|---|
| ① 随包注册表条目 | 读 `/Applications/世事.app/Contents/Resources/components.json` | ids 六项 `table/trafilatura/crawl4ai/telethon/searxng/wechat-bridge`;bridge 行 `pip_spec=setuptools>=75 wheel>=0.45 / pip_src=wechat-bridge / post_install=pip-src-no-build-isolation` 齐 |
| ② 读取层断言(设置页组件行可见的无头等价) | 临时单测注 `pyenv_components.rs` 调**真读取层** `component_statuses(data_root, Some("/Applications/世事.app/Contents/Resources"))`(serde 解析+过滤同壳同款) | `cargo test --bin myssia-desktop installed_app_resources_registry_smoke` → **1 passed**(wechat-bridge 行在列);跑毕临时测还原,`cargo test` 全量回 90p/1i 基线、`git diff src/` 空 |
| ③ pip 源码形态冒烟 | 独立 venv `/tmp/wxui-d5-pipsmoke`(uv venv --seed,零碰仓库 .venv):一段 `pip install setuptools>=75 wheel>=0.45`(setuptools 84.0.0/wheel 0.48.0)→ 二段 `pip install --no-build-isolation /Applications/…/components/wechat-bridge` | `Successfully installed wechat-bridge-0.3.0 pillow-12.3.0 pyobjc-core/-Cocoa/-Quartz/-CoreML/-Vision-12.2.2`(全在钉窗);`MYIA_HOME=<沙箱> wechat-bridge --probe` → **exit 0,`state=degraded`,`bridge_version=0.3.0`** |
| ④ 本机组件不破 | `~/.myia/plugins/wechat-bridge` diff + probe | `component.json` version=0.3.0;包源与仓 HEAD `diff -rq` 零差异;`bin/wechat-bridge --probe` exit 0,degraded/七 checks/key_unavailable reason 与换装前基线逐项一致 |

- 组件目录卫生尾注(如实):③的二段装是 in-tree build,会在装机包 Resources 组件目录落
  `build/`+`egg-info`(与 b9c5054 收口的源码树同病)——冒烟后已 `rm -rf` 清回五项净,复核零残留;
  设置页真实两段装落点在自管 python 环境,不产生此尾随。
- 谱系小结:现装 = b9c5054(worktree 干净构建;含 185484a D5 全部+bdaaf96/b9c5054 两笔收口);
  不含 6f55129/bb9ba05(并行 feed/spec 线,下次刷新自然并入)。
- 私有数据红线自查:本档零聊天内容、零密钥材料;证据只含状态码/版本号/计数/inode/路径与时间戳。

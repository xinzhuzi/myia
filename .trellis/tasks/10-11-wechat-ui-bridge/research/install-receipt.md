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

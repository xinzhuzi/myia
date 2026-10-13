# 配置编辑屏:品类文件搜索 + 打开文件位置

主人令(2026-10-11):「配置编辑这块,无法搜索品类文件,因为以后品类文件会越来越多的,所以需要你可以做个搜索逻辑;再跑一次旁边,要有个按钮点击时打开本配置文件的文件位置,弹出文件夹」。

## 背景

- 配置编辑第六屏(desktop/ui-src/src/screens/yaml-editor/)左栏 FileList 平铺全部品类文件,无检索手段;品类文件随插件/品类扩容会持续增多,需要定位手段。
- 主人点名的按钮位置:「跑一次」旁边(编辑区工具条);行为 = 弹出该配置文件所在文件夹(系统文件管理器)。

## 方案

### ① 品类文件搜索(FileList)

- 列头下加搜索框(Input,aria-label=搜索品类文件),**前端态过滤,不发光**;
- 匹配口径:品类名(`category_name ?? name`)与文件名(`name`)子串、大小写不敏感(品类 id 一并参与,成本为零);
- 计数口径:未过滤 = `品类文件(N)`(既有文案与测试断言不动);过滤中 = `品类文件(命中/总数)`;
- 过滤零命中 = 内联空态提示(不吞列表);草稿伪条目不受过滤影响(未保存工作不可被搜索藏没)。

### ② 「打开位置」按钮(工具条)

- 位置:「跑一次」左侧,FolderOpen 图标 + 「打开位置」;`docReady === null` 禁用;
- 行为:弹当前文件所在文件夹(不要求选中文件本体);
- 实现:main.rs 新增 `reveal_yaml_dir` 命令——围栏校验(必须 `.yaml` 后缀 + 文件存在 + 父目录在)后经平台文件管理器打开(macOS `open` / Windows `explorer` / Linux `xdg-open`,`spawn()` 不等退出码——explorer.exe 成功也常回非零,等退出码会误报);
- **不扩 `shell:allow-open` 授权**(现仅 http/https;自定义命令不经 capability 门,免扩权);
- 错误经 asSidecarError 归一化进 findings 抽屉 ErrorBox。

## Acceptance Criteria

- [x] AC1 搜索:输入子串实时过滤(品类名/文件名/id,大小写不敏感);清空恢复全量
- [x] AC2 搜索计数:未过滤 `品类文件(N)` 原样;过滤中 `(命中/总数)`;零命中有内联提示;草稿条目不受过滤影响
- [x] AC3 打开位置:选中文件后按钮可用,点击触发 `reveal_yaml_dir`(file=当前路径);未选文件禁用
- [x] AC4 壳围栏:非 .yaml 后缀/文件不存在/无父目录 → 结构化报错不拉起进程;合法路径 → 平台文件管理器打开父目录(spawn 不等退出码)
- [x] AC5 测试:前端(过滤/计数/零命中/按钮调用/禁用态/错误态)+ Rust(围栏校验单测)全绿
- [x] AC6 门禁:vitest + tsc -b + cargo(测试/构建)+ npm run build 全绿
- [x] AC7 交付:入库 + 装机包已刷新换装(交付纪律)

## 边界

- 源管理弹窗(yaml-editor-dialog.tsx)不加搜索/位置按钮(主人点名的是配置编辑屏;弹窗是源管理语义,不扩散);
- 不做服务端过滤(存量规模前端过滤绰绰有余;协议 yaml.* 六方法不动)。

## 结果(交付回执,2026-10-11)

- **代码 7bb8314**(5 文件,+249/−6):file-list.tsx 搜索框+过滤+计数+零命中态;yaml-editor-screen.tsx 工具条「打开位置」(FolderOpen,未选文件禁用)+ revealError 抽屉槽;api.ts revealYamlDir 壳命令封装;main.rs `reveal_yaml_dir` + `yaml_dir_to_reveal` 围栏纯函数 + generate_handler 注册 + 围栏单测。
- **门禁**:本屏 vitest 22/22(含 5 新用例:过滤/计数切换/零命中/草稿不受滤/按钮调用/禁用态/错误态);全量 vitest 694/694(首轮 693/694,feed-screen 1 例并发 flake,单跑与复跑均全绿,与本改动无涉——diff 不触 feed 面);cargo test reveal_yaml_dir_fence 过;cargo build 过;tsc -b + vite build 过。
- **GitNexus**:编辑前 impact(FileList/YamlEditorScreen)=LOW(唯一调用方本屏);提交前 detect-changes 报 HIGH 经甄别为**行号漂移伪影**(main.rs 纯插入 66 行零删改,伪报 data_root 等未触符号),diff --cached 实证唯一新增 fn 即围栏函数。
- **装机(AC7)**:tauri build exit 0(世事.app 17.82MiB + DMG 0.0.3,12:11);换装前验源=新二进制字节 grep `reveal_yaml_dir` 命中;备份 `/tmp/myssia-yamleditor-backup-20261011-121329` 后 ditto 换装 /Applications/世事.app;`codesign --force --deep -s -`+`-vv --strict` 双过;WKWebView 缓存清理(仅 `~/Library/WebKit/com.myssia.app`,历史标识 myia-desktop/com.myia.desktop-spike 不动);装机二进制复核符号在案。**装机无头冒烟(package_smoke)全 PASS**:A0 预检清场/A1 open -g 静默启动/A2 主进程存活(pid 54647)/A4 CGWindowList 双窗/A5 数据根 .instance.lock/A6 安静退出全过;B 部分按自管 Python 架构治理 SKIP(行为面已在冻结期架构验证+本批 vitest 覆盖)。如实声明:「打开位置」的 Finder 弹出为系统交互,无头不可断言且实弹会弹 Finder 窗占主人屏,留主人下次启动 app 后顺手目验。


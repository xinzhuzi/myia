# implement:微信渠道模块化(勾选式;每步带验证命令)

## P0 前置(取证与清障)

- [ ] 0.1 并行在途检查:`git status` 核对六件+12 件零脏(脏=停,协调)
- [ ] 0.2 push 渠道发现机制取证:`rg -n "weixin_local|weixin-local|wecom" src/myssia/push/__init__.py src/myssia/push/base.py src/myssia/push/directory.py src/myssia/pipeline.py | head -30`——**输出清单贴本档**(设计 §2 注册面改指的依据)
- [ ] 0.3 引擎注册面取证:`rg -n "wechat_local" src/myssia/engines/__init__.py src/myssia/engines/registry* 2>/dev/null || rg -ln "engine.*wechat_local|wechat_local.*engine" src/myssia --glob '!engines/wechat_local.py'`
- [ ] 0.4 基线:全量 pytest+vitest+build 三跑记绿(design §5 命令)
- [ ] 0.5 符号引用全清单(修一处扫类的底账):`rg -ln "wechat_local_sidecar|wechat_stats_sidecar|push.weixin_local|push.wecom|push.weixin\b|engines.wechat_local" src desktop tests --glob '!__pycache__' --glob '!target'` → 贴档

## P1 python 包归位(先叶后干;每件=移动+薄壳+全引用更新+该件测试绿)

- [ ] 1.1 建 `src/myssia/wechat/__init__.py`(暂空,P3 充门面)
- [ ] 1.2 `wechat_local_sidecar.py` → `wechat/sidecar.py`;原位薄壳;引用方(sidecar 消费 4 处)改指新径或走薄壳(统一走新径,薄壳只保外部兼容)
- [ ] 1.3 `wechat_stats_sidecar.py` → `wechat/stats_sidecar.py`(+proxy_panel 引用核实)
- [ ] 1.4 `push/weixin.py` → `wechat/push_weixin.py` + 薄壳
- [ ] 1.5 `push/weixin_local.py` → `wechat/push_local.py` + 薄壳(**Rust 注释同步五处**)
- [ ] 1.6 `push/wecom.py` → `wechat/push_wecom.py` + 薄壳(pipeline.py 引用更新)
- [ ] 1.7 `engines/wechat_local.py` → `wechat/engine.py` + 薄壳(引擎注册面更新;1125 行最大件,单独一 commit)
- [ ] 1.8 P1 验证:pytest 全量绿 + 兼容壳探针(design §5)+ `git diff` 抽查三件确认纯移动判据(除 import/docstring 首行零逻辑改)

## P2 desktop 子域

- [ ] 2.1 `mkdir desktop/ui-src/src/screens/messaging/wechat/`;12 件 `git mv` 归位
- [ ] 2.2 组件相对导入与父引用(messaging-screen.tsx、api 层、command-palette/sidebar 如有)路径更新(依据 0.5 清单)
- [ ] 2.3 vitest+build 双绿(tsc 路径别名如涉 tsconfig paths 同步)

## P3 门面/注释/文档

- [ ] 3.1 `wechat/__init__.py` 充门面:re-export 六件公共符号 + `__all__`;补包 docstring(对齐 telegram 包口径)
- [ ] 3.2 keyprovider.rs 五处注释口径更新 → `cargo check` 零破坏
- [ ] 3.3 文档:桥 README 模块地图小节 + `.trellis/spec`(python 分层 spec)的微信模块条目(走 trellis-update-spec)
- [ ] 3.4 终验:全量 pytest+vitest+build+cargo check 四绿;AC 逐条勾

## 提交切分(每步一 commit,回滚友好)

1. `refactor(wechat): python 侧归位——sidecar/stats 双件` 2. `…push 三件` 3. `…engine 大件` 4. `refactor(desktop): 微信屏族子域` 5. `docs/门面与注释`

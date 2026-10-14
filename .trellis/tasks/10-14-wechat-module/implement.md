# implement v2:微信渠道模块化(R1 全吸收;勾选式,每步带验证)

## P0 前置(取证与底账)

- [ ] 0.1 并行清障:`git status` 真跑;核对七件+22 屏族零脏;与在途任务(sendmsg-direct,桥件在 plugins/)不相交性确认
- [ ] 0.2 push 注册机制底账:`rg -n "weixin|wecom" src/myssia/push/__init__.py` 输出贴档(已预勘:114/115/119 三 import,注册键名不变)
- [ ] 0.3 引擎注册面底账:`sed -n '160,200p' src/myssia/engines/registry.py` 贴档(:171 lambda/:180 `_load` 派生)
- [ ] 0.4 基线四关:pytest/vitest/build/cargo check 全绿记底(design §5 命令)
- [ ] 0.5 python 符号底账(修一处扫类的账本):
      `rg -ln "wechat_local_sidecar|wechat_stats_sidecar|push\.weixin_local|push\.weixin\b|push\.wecom|engines\.wechat_local" src desktop tests --glob '!__pycache__' --glob '!target'` 贴档
- [ ] 0.5.2 **TS 引用底账**(R1-F5 新增;0.5 的 python 串匹配不到 TS):
      `rg -ln "wechat-|wx-stats|wx-groupinfo|weixin-account" desktop/ui-src/src --glob '*.ts*' | grep -v "messaging/wechat/"` 输出与 design §1 的 TS 引用面清单对账,差异以实测为准贴档
- [ ] 0.6 测试 monkeypatch 底账(R1-F1):`rg -n "wechat_local_sidecar|engines\.wechat_local|weixin_local" tests/ | grep -i "import\|setattr"` → 四文件(local_handlers/local_media_handlers/stats_sidecar/test_wechat_local_engine)逐文件贴 setattr 计数

## P1 python 归位(先叶后干;每件=git mv+薄壳+仓内引用全改+该件测试迁新径+绿)

- [ ] 1.1 `mkdir src/myssia/wechat`;`__init__.py` 暂空(P3 充门面)
- [ ] 1.2 `push/weixin.py → wechat/push_weixin.py`;薄壳;改 push/__init__.py:114、entry.py:433
- [ ] 1.3 `push/weixin_local.py → wechat/push_local.py`;薄壳;改 push/__init__.py:115、local_sidecar:内联、engines/wechat_local.py、engines/wechat_local_notify.py:59
- [ ] 1.4 `push/wecom.py → wechat/push_wecom.py`;薄壳;改 push/__init__.py:119、pipeline.py
- [ ] 1.5 `wechat_local_sidecar.py → wechat/sidecar.py`;薄壳;改 stats_sidecar、engines/wechat_local、entry.py:434-436;**__file__ 探针**(stats 双件同批):config/wechat-stats.yaml 回落路径解析实测(design §5 末条,函数名先核对再跑)
- [ ] 1.6 `wechat_stats_sidecar.py → wechat/stats_sidecar.py`;薄壳
- [ ] 1.7 `engines/wechat_local_notify.py → wechat/notify.py`;薄壳
- [ ] 1.8 `engines/wechat_local.py → wechat/engine.py`(1125 行大件单独 commit);薄壳;**registry.py:171 lambda 改指 myssia.wechat.engine**(`_load` 加全路径变体);`python -c "from myssia.wechat.engine import WechatLocalEngine"` 直载验证
- [ ] 1.9 **测试迁移**(R1-F1 硬步骤):四测试文件 import 与 46+ setattr 目标全部改新径;`rg -n "myssia\.push\.weixin_local|myssia\.engines\.wechat_local|myssia import wechat_local_sidecar" tests/` 断言**零残留**
- [ ] 1.10 P1 终验:pytest 全量绿+兼容壳探针绿+抽查三件 git diff 确认移动判据(仅 import/docstring)

## P2 desktop 子域(依据 0.5.2 实测清单,不照抄 design 预勘)

- [ ] 2.1 `mkdir desktop/ui-src/src/screens/messaging/wechat/`;22 件按 design §1 清单 `git mv`(以 0.5.2 对账后的实测清单为准)
- [ ] 2.2 父引用更新(对象=0.5.2 清单:messaging-screen/api.ts/platform-icons(.test)/platform-overview/wx-stats-panel×2/feed api/feed-screen(.test)/lib/api/types.ts)
- [ ] 2.3 vitest+build 双绿

## P3 门面/注释/文档

- [ ] 3.1 `wechat/__init__.py` 门面:显式符号白名单+手工 `__all__`(不 import* 合并,F13);包 docstring 对齐 telegram 包口径+注明「超越 TG 形态」定位
- [ ] 3.2 keyprovider.rs 五处注释口径(5/26/66/200/397 行)→ cargo check 零破坏
- [ ] 3.3 文档:桥 README「19 文件」勘误(实况:纯 .py 27 件,R1-F12)+模块地图小节;spec 更新走 trellis-update-spec
- [ ] 3.4 终验四关+AC 逐条勾(AC4 按 v2 判据:移动件纯移动+白名单封闭集)

## 提交切分

1. `refactor(wechat): push 三件归位` 2. `…sidecar 双件+__file__ 探针` 3. `…notify+engine 大件+registry 改指` 4. `refactor(desktop): 微信屏族 22 件子域` 5. `docs/wechat: 门面+注释+模块地图`

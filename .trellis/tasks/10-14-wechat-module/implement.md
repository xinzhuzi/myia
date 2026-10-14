# implement v3:微信渠道模块化(R1+R2 全吸收;勾选式,每步带验证)

## P0 前置(取证与底账)

- [ ] 0.1 并行清障:`git status` 真跑贴档;核对七件+messaging 14 件零脏(在途任务脏档与七件不相交性以实测为准)
- [ ] 0.2 push 注册底账:`rg -n "weixin|wecom" src/myssia/push/__init__.py` 贴档(预勘:**wecom=114、weixin=115、weixin_local=119**,R2-F5 勘误;以实测为准)
- [ ] 0.3 引擎注册底账:`sed -n '160,200p' src/myssia/engines/registry.py` 贴档(:171 lambda/:180 派生)
- [ ] 0.4 基线四关:pytest/vitest/build/cargo check 全绿记底(design §5)
- [ ] 0.5 python 底账:`rg -ln "wechat_local_sidecar|wechat_stats_sidecar|push\.weixin_local|push\.weixin\b|push\.wecom|engines\.wechat_local" src desktop tests --glob '!__pycache__' --glob '!target'` 贴档
- [ ] 0.5.2 TS 底账(三探针并集,单探针有盲区 R2-F6):
      a) `rg -ln "wechat-|wx-stats|wx-groupinfo|weixin-account" desktop/ui-src/src --glob '*.ts*'`
      b) `rg -ln "from \"[./]*.*(wechat|weixin|wx-)" desktop/ui-src/src --glob '*.ts*'`
      c) `rg -ln "myssia\.push\.weixin|probe_bridge" desktop/ui-src/src --glob '*.ts*'`
      并集与 design §1「TS 父引用面」对账,差异以实测贴档(App.tsx 因分域方案已解除,若 a) 仍命中须记录为「引用不变」)
- [ ] 0.6 测试账实底账(R2-F1):`rg -ln "myssia\.push\.weixin_local|myssia\.engines\.wechat_local|myssia import wechat_local_sidecar|myssia import wechat_stats_sidecar|push\.weixin\b|push\.wecom" tests/` + 逐文件 `rg -c "monkeypatch.setattr" <file>` 贴档(预勘 9 文件,engine 测试 85 行 setattr)

## P1 python 归位(先叶后干;每件=git mv+薄壳+仓内引用全改(含函数内 lazy)+相关测试迁新径+绿)

- [ ] 1.1 `mkdir src/myssia/wechat`;`__init__.py` 暂空
- [ ] 1.2 `push/weixin.py → wechat/push_weixin.py`;薄壳;改 push/__init__:115、entry.py:433;tests/push/test_messaging_weixin_bridge.py 迁新径
- [ ] 1.3 `push/weixin_local.py → wechat/push_local.py`;薄壳;改 push/__init__:119、local_sidecar 顶层引用、engines/wechat_local、engines/wechat_local_notify:59、tests/push/test_messaging_weixin_local.py
- [ ] 1.4 `push/wecom.py → wechat/push_wecom.py`;薄壳;改 push/__init__:114、pipeline.py、tests/push/test_messaging_wecom.py、test_messaging_pipeline.py
- [ ] 1.5 `wechat_local_sidecar.py → wechat/sidecar.py`;薄壳;改 stats_sidecar(顶层+**:151 lazy _BASE**)、engines/wechat_local:142、entry.py:434-436;tests/desktop 两文件迁新径
- [ ] 1.6 `wechat_stats_sidecar.py → wechat/stats_sidecar.py`;薄壳;改 **entry.py:4814(函数内 lazy,R2-F4)**;test_wechat_stats_sidecar.py 迁新径;**__file__ 探针**(design §5 末条,实码 config_path)
- [ ] 1.7 `engines/wechat_local_notify.py → wechat/notify.py`;薄壳;**其内部 :59(push_local)/:99/:109(→engine)三处 import 改绝对新径**;tests/engines/test_wechat_local_notify.py 迁新径(14 setattr)
- [ ] 1.8 `engines/wechat_local.py → wechat/engine.py`(大件单独 commit);薄壳;**:331/:514 两处 lazy → myssia.wechat.notify**;registry.py:171 lambda 改指新径;`python -c "from myssia.wechat.engine import WechatLocalEngine"` 直载;test_wechat_local_engine.py 迁新径(85 行 setattr,58 处 wx_engine 目标)
- [ ] 1.9 P1 终验:pytest 全量绿;**design §5「仓内零残留」七旧径全量断言跑通**;抽查三件 git diff 判据(docstring 首行+一切 import 行,白名单封闭集外零改)
- [ ] 1.10 兼容壳探针(design §5)绿

## P2 desktop 子域(分域方案:只迁 messaging 14 件)

- [ ] 2.1 `mkdir desktop/ui-src/src/screens/messaging/wechat/`;messaging 14 件 `git mv`(清单=design §1;feed 4/settings 3/weixin-account 1 **不动零变更**)
- [ ] 2.2 父引用更新(对象=0.5.2 并集:messaging-screen.tsx、messaging/api.ts、platform-icons(.test)、platform-overview.tsx、wx-stats-panel×2、lib/api/types.ts)
- [ ] 2.3 vitest+build 双绿

## P3 门面/注释/文档

- [ ] 3.1 `wechat/__init__.py` 门面:显式符号白名单+手工 `__all__`;包 docstring 注明「超越 TG 形态」定位
- [ ] 3.2 keyprovider.rs 五处注释口径 → cargo check 零破坏
- [ ] 3.3 文档:桥 README 模块地图小节(计数以 `ls plugins/wechat-bridge/wechat_bridge/*.py | wc -l` 实测口径写,不写死数字);spec 走 trellis-update-spec
- [ ] 3.4 终验四关+AC 逐条勾(AC1=七件;AC4=移动判据+白名单封闭集;AC3=messaging 14 件子域+分域豁免注记)

## 提交切分

1. `refactor(wechat): push 三件归位` 2. `…sidecar 双件+entry 三处` 3. `…notify+engine+registry 改指` 4. `refactor(desktop): messaging 微信 14 件子域` 5. `docs/wechat: 门面+注释+模块地图`

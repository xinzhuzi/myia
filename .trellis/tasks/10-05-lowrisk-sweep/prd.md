# 低危尾款四件清扫(10-05-lowrisk-sweep)

## 背景

v12-backlog 池 2026-10-05 傍晚收口后余量定界:①低危尾款四件。本流逐件处置:三件经亲证确认已在库修复(裁掉销号,理由记档),一件修注记不修值。

## 范围与处置

### ①a zenrows css_extractor 显式 null 判值——裁(销号)

- 定位:`src/myssia/engines/zenrows.py:82` 现码 `return self.engine_options().get("css_extractor") is not None`(判值口径);docstring(:75-81)明记「css_extractor: ~(显式 null)= 空态」。
- 守卫:`tests/engines/test_saas_gated_engines.py:312-338` `test_zenrows_css_extractor_explicit_null_is_html_mode` 在库(:335 断言空态不发参,:336-338 断言 HTML 直通)。
- 裁理由:ead33f7(2026-10-05 12:00 批二复审遗留修复)已修在库,本轮亲证代码+测试双在;重复修=无操作。零代码零测试。

### ①b saas gated 引擎「零上游请求」守卫的 robots 盲区——裁(销号)

- 守卫一:`tests/engines/test_saas_gated_engines.py:176-192` `test_closed_gate_precedes_robots_zero_requests_including_robots`(:185 裸 handler 连 robots.txt 拉取一并 pytest.fail=关闭态零请求含 robots)。
- 守卫二:`:194-211` `test_robots_denied_open_gate_skips_paid_upstream_request`(:205 全站 Disallow,:211 断言 error_type==robots_disallowed 零付费上游)。
- 裁理由:ead33f7 两守卫在库,本轮亲证;盲区已封。零代码零测试。

### ①c sidecar-protocol「gates.get 非法参数」超前半句——裁(销号)

- 实际路径:`.trellis/spec/desktop/sidecar-protocol.md:282`(ask 所写 docs/ 前缀有偏差,文件实归 spec,如实记档)。
- 亲证:该行现文「`gates.get` 不校验 params —— 多余键忽略,仅入口层『params 非对象』通用拒绝;task 10-05-plugin-market-batch 批二第 11 步,遗留修对齐代码实况」;`grep "非法参数" 该文件` 零命中。
- 裁理由:超前半句已删并对齐代码,本轮亲证。零改动。

### ①d plugin manifest install.source 仓库名——修注记不修值

- 真名亲证(本轮):`git remote -v` → origin=`https://github.com/xinzhuzi/myia.git`;`gh api repos/xinzhuzi/myia` → `full_name=xinzhuzi/myia`、redirect_source=none(真名);`gh api repos/xinzhuzi/shishi` → 解析为 `xinzhuzi/myia`(shishi 系 301 别名)。**方向反转:旧注记称「远端已改名 MYIA→shishi」是错的,现值(myia)恰为真名。**
- 全仓统计(本轮亲跑):`grep -rl 'github.com/xinzhuzi/myia' plugins/*/plugin.yaml | wc -l` = 20 件零改动零重定向。
- golden 排查:`tests/plugins/test_plugin_packages.py:165` 对官方件真 manifest 断言 `install.source.startswith("https://")`(只锁前缀不锁仓库名)——注释行改动零断言影响,golden 无需再生。`desktop/src-tauri/tauri.conf.json:91` updater endpoint 同为 myia 真名无需改。
- 唯一动作:更正 `plugins/myssia-crawlab/plugin.yaml:27-32` 过时注记(现文方向反了,且悬着「统一切 shishi 批末专项」会诱导并行会话把 20 件改成别名方向),改写为真名口径+作废旧专项。
- 同步 v12-backlog 池档冻结该专项,广播防并行会话照旧执行。

## 验收标准(AC)

1. AC1(①a/①b/①c 销号):三件代码/测试/spec 现状亲证记录在 evidence,池档对应条目销号(标注裁理由+亲证引线)。
2. AC2(①d 注记):plugin.yaml 注记改为真名口径;`git diff` 仅注释行;20 件 source 值零改动;gh api 复核记录在案。
3. AC3(池档广播):v12-backlog 池档冻结「统一切 shishi」专项,方向反转说明入档。
4. AC4(门禁):`uv run --no-sync pytest tests/engines tests/plugins -q` 全绿 + ruff 定向零告警,数字如实记录。
5. AC5(纪律):git commit --only 本流文件;task.json 置 review。

## 非目标

- 不改 20 件 manifest source 值(现值=真名 fresh install 零重定向)。
- 不改 GitNexus 索引名(索引层滞后与远端名无关)。
- 不涉 fe-gap/G10/trafilatura/Reddit/plugins 发现通道等其余余量。

## AC 证据回填(2026-10-05 本轮亲跑)

1. **AC1 ✅ 三件销号亲证**:
   - ①a:`src/myssia/engines/zenrows.py:82` 现码 `return self.engine_options().get("css_extractor") is not None`(Read 亲证);docstring :75-81 判值口径明记;守卫 `tests/engines/test_saas_gated_engines.py:312-338`(Read 亲证,:335 空态不发参断言)。
   - ①b:`tests/engines/test_saas_gated_engines.py:176-192`(:185 裸 handler `pytest.fail(f"不应发起任何请求:{request.url}")` 连 robots 一并钉死)+ `:194-211`(:205 全站 Disallow,:211 `error_type == "robots_disallowed"`)均 Read 亲证。
   - ①c:`.trellis/spec/desktop/sidecar-protocol.md:282` 现文「`gates.get` 不校验 params —— 多余键忽略,仅入口层『params 非对象』通用拒绝」(sed 亲读);`grep -n "非法参数" .trellis/spec/desktop/sidecar-protocol.md` → 零命中(exit=1)。
   - 池档销号:10-03-v12-backlog/prd.md 尾部「本轮纪要(2026-10-05 低危尾款清扫轮)」三件销号注记落档。
2. **AC2 ✅ ①d 注记修正**:`git diff plugins/myssia-crawlab/plugin.yaml` 亲核=仅 8 行注释改动(source 值行零改动);`grep -rl 'github.com/xinzhuzi/myia' plugins/*/plugin.yaml | wc -l` = 20(亲跑);`gh api repos/xinzhuzi/myia` → `{"full_name":"xinzhuzi/myia","redirect":"none"}`、`gh api repos/xinzhuzi/shishi` → 解析为 xinzhuzi/myia(亲跑,真名反转坐实)。
3. **AC3 ✅ 池档广播**:池档纪要首段即「冻结广播:『统一切 shishi 批末专项』作废,任何并行会话勿再执行」,方向反转+后果(会把 20 件改成别名方向)+GitNexus 索引名豁免均入档。
4. **AC4 ✅ 门禁**:`uv run --no-sync pytest tests/engines tests/plugins -q` → **1001 passed, 39 skipped in 30.02s**(亲跑);`uvx ruff@0.16.10 check src/myssia/engines tests/engines tests/plugins` → `All checks passed!`(亲跑;本流零 py 改动,ruff 为涉及面定向确认)。
5. **AC5 ✅ 纪律**:git commit --only 本流四文件(plugin.yaml + 两档 prd.md + task.json);detect-changes 豁免口径=YAML 注释+md 文档+json 状态,零语义零代码符号改动(本流唯一代码库内改动是 YAML 注释行)。

## 执行注记

- ask 所写 `docs/sidecar-protocol.md` 路径有偏差:全仓 find 实际位于 `.trellis/spec/desktop/sidecar-protocol.md`(find 亲跑);按实际路径亲证,内容与计划定案一致。
- ①d 计划口径「17 件同惯例」与本轮亲跑 `grep … | wc -l` = **20** 不一致,以亲跑 20 为准(计划基线的 17 可能系旧快照口径)。
- 池档原无四件既有条目(系本轮基线新定界未入池档登记),销号动作以纪要段落形式落档并注明详情引线回本档。

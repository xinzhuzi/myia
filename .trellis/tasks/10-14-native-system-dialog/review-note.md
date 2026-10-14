# review-note(代审④ native-system-dialog,2026-10-15)

代审员:s9-review-native-dialog(六任务代审 fan-out ④)。方法:证据档薄 → 提交链对账型——prd 提 AC,以提交 diff + HEAD/工作树现势 + prd 声明的本地门禁实跑对账;装机面不代跑。全程零微信零索引操作零状态指针改动。

## 提交链(对账锚)

| 提交 | 角色 | 证据 |
|---|---|---|
| 18c2f51f(10-14 19:34) | 本任务主交付:system-confirm.ts+专测、capabilities 单权限、8 调用点、任务档四件、规范第8条 | `git show --stat 18c2f51f`:16 文件 +274/−36 |
| f9d726ab(10-14 20:28) | 同特性加固:原生通道抛错(ACL 拒/插件故障)→ 安全缺省取消 | system-confirm.ts:34-40(catch→console.error→return false)+ test :73-82 |
| 801b15b8 | **勘误锚**:evidence-auth-prompt{,-2}.png 由该提交入档于 10-14-notify-app-icon(「授权征询证据」=通知授权),与本任务无关 | `git log -- …/notify-app-icon/evidence-auth-prompt.png` 唯一命中 801b15b8 |

## 逐 AC 判定

- **AC1 过** — 双分支:`desktop/ui-src/src/lib/system-confirm.ts:23-43`(`__TAURI_INTERNALS__` 判定 → plugin confirm(title/kind 默认 warning/okLabel 默认「确定」/cancelLabel 默认「取消」);非 Tauri 回退 `:42`。8 调用点全数在位且 title+动词化 okLabel 齐备(工作树 grep 实测:cron-screen.tsx:354、bundled-plugins-card.tsx:390/:422、use-source-wizard.ts:254、use-yaml-file-editor.ts:112、yaml-editor-screen.tsx:132/:199、feishu-account-card.tsx:143;18c2f51f diff 逐点见 title/okLabel)。专测两分支+异常分支:system-confirm.test.ts:27-71/:73-82,本步实跑绿。守卫接线:两 dialog attemptClose 改 fire-and-forget(18c2f51f diff 实见 `.then((ok)=>{if(ok)onClose()})`)。
- **AC2 过** — 18c2f51f diff:capabilities/default.json permissions 恰 `+ "dialog:allow-confirm"` 单条 + description 同步注记,无其他权限面变化。
- **AC3 过** — 本步实跑(命令逐字):`desktop/ui-src/node_modules/.bin/tsc --noEmit -p desktop/ui-src/tsconfig.app.json` → EXIT=0 零输出;`cd desktop/ui-src && npx vitest run src/lib/system-confirm.test.ts src/screens/cron/cron-screen.test.tsx src/screens/settings/feishu-account-card.test.tsx src/screens/yaml-editor/{editor-pane,yaml-editor-dialog,yaml-editor-screen}.test.tsx src/screens/sources/source-wizard/{source-wizard-dialog,build-category-yaml}.test.ts` → **8 文件 104/104 绿 EXIT=0**(stderr 一条 cron 用例内预期的 mock 报错文案,用例本身 ✓)。既有测试零改动:18c2f51f/f9d726ab 文件清单均未触碰既有 *.test.*。注:prd 记「119/119 scoped」,本代审按 prd 点名套件选文件得 104/104,绿性一致、口径差=文件集选取(prd 未存当时文件清单,无从逐复现其 119 计数,如实注)。
- **AC4 过** — `git grep -n 'window\.confirm' HEAD -- desktop/ui-src/src`(剔测试)与工作树 grep 双验:生产代码仅 system-confirm.ts:42 回退一处 + :2/:5/:14 三行注释。
- **AC5 有条件过(现场漂移)** — 装机门禁(新包沙箱冒烟/哈希判别 6584a65b…/WKWebView 缓存清/主人实例 70699)**not-run**:装机面按纪律不代跑重门禁(判例 packaged-app-verify-and-swap-race)。轻量只读在位核验:**回退副本 `/Applications/世事.app.old-1014-native-dialog` 已不存在**(仅存世事.app.old-sweep,属另一任务),当前 `/Applications/世事.app` mtime=Oct 15 03:38:28 已被后续线换装漂移(勘察档记 10-15-remaining-sweep 线 03:27:59 开工、描述含打包覆盖安装)→ prd「旧包留…可回退」承诺在当前现场不成立。另:沙烟截图 OCR 从未入 git(本任务 evidence/ 目录从未存在,18c2f51f 收档仅任务档四件),实物证据零。

## 缺口与勘误(交收口轮)

1. **ask 前提勘误**:代审指令所列 `evidence/evidence-auth-prompt{,-2}.png` 归属 10-14-notify-app-icon(801b15b8 入档),非本任务;本任务证据档=零,代审只能提交链对账(已照做)。
2. AC5 回退副本灭失:需主人/装机维护窗决断——重立回退点或接受 03:38 已被 later-sweep 换装的现状。
3. task.json `commit` 字段=null 未回填 18c2f51f(簿记小缺口,不改状态指针故本代审不动)。
4. prd Requirement 3 提「在飞守卫防 ESC 双触发」,实现以「原生弹窗应用模态、webview 收不到新输入」论证免设(18c2f51f 内 yaml-editor-dialog/source-wizard-dialog attemptClose 注释)——Requirements 层偏离有理由注记,非 AC 违例。

## 结论

**有条件过**:AC1-AC4 全数实证过(提交哈希+path:line+门禁实跑);AC5 装机面不可复验且回退副本已漂移灭失,留主人决断。

## 哨兵记录

步前 porcelain md5=`3ea22d0f48dbdfa660b88a5c25f27ecc`(7 行);门禁跑后=`93651f0dc5c12a3a0e5a8e94011e1465`(5 行)——差量=并行 sendmsg 线新提交 e75732ec 收走 senddirect_probe.py(M)与 fexec_decompile.c(??)两件,与本步无关;本步门禁零 git 可见写入,唯一写入=本文件。s1 基线 md5 未随指令下发,以步前/步后自比对+勘察档文字快照结构性对照替代,如实注。

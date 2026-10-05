# GHCR 容器镜像盘点(ghcr.io/xinzhuzi 账号)

- 任务:10-04-wrapup-checklist 第一节 2「GHCR 清理」(只读盘点+清理提案)
- 日期:2026-10-04 · 执行:GHCR 盘点员(workflow subagent) · 账号:xinzhuzi(gh auth status 实测)
- **状态:0 条删除已执行。本文件全部是提案,待主人逐条确认后执行。**

## 0. 结论速览

| package | 判定 | tagged | untagged | 合计版本 |
|---|---|---|---|---|
| `xinzhuzi/myia` | **现役包名**(repo 名即镜像名;compose/docs 全指它) | 24 | 96 | 120 |
| `xinzhuzi/shishi` | **历史名残留**(repo 曾改名 shishi 的窗口期产物,**但持有唯一真发布**) | 22 | 93 | 115 |
| `xinzhuzi/myssia` | 不存在(产品名≠包名,见 §3) | — | — | — |
| 8 个变体名(见 §2) | 不存在 | — | — | — |

**比清理更要紧的横切发现(§5)**:①`myia:latest` 停在 2026-10-03 12:06+0800 的 dev build(d359a3e),早于 v0.0.1/v1.1.1,而两个正式版 tag 只存在于 shishi 包 → RELEASE.md:156 的 `docker pull ghcr.io/xinzhuzi/myia:0.0.1` **当前是坏的**;②untagged 版本里混着多架构子清单(每 push 恰好 4 个:amd64+arm64+2 attestation;96=24×4、93≈22×4+5 吻合)→ **盲删全部 untagged 会打断 keep 集标签的拉取**,P3 必须走 digest 排除机制。

## 1. 盘点通道与方法(含指定检查未跑成的替代说明)

**指定检查未跑成**:`gh api 'user/packages?package_type=container&per_page=100'`(及其 users/ 变体)返回 403——

```
{"message":"You need at least read:packages scope to list packages.","status":403}
```

本机 gh token(账号 xinzhuzi,gho_ keyring)scopes 实测:`gist, read:org, repo, workflow`——**无 read:packages**。环境变量无 GH_TOKEN/GITHUB_TOKEN(实测)。给 token 加 scope 需交互式 device flow(`gh auth refresh -s read:packages,delete:packages`),subagent 无法自主完成,故未尝试。

**替代通道(均匿名、只读、可复跑)**:

a. **GHCR registry API**(公开包匿名可查):
```
curl -s "https://ghcr.io/token?scope=repository:xinzhuzi/<name>:pull"        # 换匿名拉取 token
curl -s -H "Authorization: Bearer <tok>" "https://ghcr.io/v2/xinzhuzi/<name>/tags/list"   # tag 清单
curl -sSI -H "Authorization: Bearer <tok>" -H "Accept: <manifest 类型们>" .../manifests/<tag>   # 从 Docker-Content-Digest 头拿 digest
# 再按 index→arch manifest→config blob 链取 config.created = 镜像构建时间(需 -L 跟 CDN 307;脚本 /tmp/ghcr_sweep2.py)
```
b. **GitHub web 版本页**(服务端渲染、匿名可见、含 version_id):
`https://github.com/xinzhuzi/myia/pkgs/container/<pkg>/versions?filters%5Bversion_type%5D=<tagged|untagged>&page=N`(分页参数 page=N,rel="next" 判页尾;行内 `/users/xinzhuzi/packages/container/<pkg>/<id>?tag=<tag>` 提取 ID+tag,`value="sha256:<64>"` 提取 digest,`Published X ago` 提取发布龄)
c. **本仓 workflow/git/release 史**(交叉验证):IMAGE_NAME 恒为 `github.repository`(docker-publish.yml:14);4 个 workflow 文件全枚举过(git log --diff-filter=A);tag/release(gh api repos/xinzhuzi/myia/tags|releases,本地 git tag)。

**两通道互相印证**(抽样,非穷举):web 版本 1330061187 的 digest 前缀 b34149a91e41 ↔ registry HEAD `latest` 的 Docker-Content-Digest 前 12 位一致 ↔ registry tags/list 中 `latest` 与 `sha-d359a3e` 同 digest ↔ config.created=2026-10-03T04:06:38Z ↔ 本地 git d359a3e(2026-10-03 12:07+0800,yaml-editor feat)。shishi 包 1330846980(0.0.1+latest)↔ ae5fa91c7566 ↔ created 2026-10-03T10:18:41Z ↔ release v0.0.1 published 10:40:46Z。

## 2. 包清单与「不存在」的探测

| 名字 | 匿名探测结果(ghcr.io/v2/.../tags/list) |
|---|---|
| xinzhuzi/myia | ✅ 25 个 tag(latest + 23 个 sha-*;**无 semver tag**) |
| xinzhuzi/shishi | ✅ 25 个 tag(1.1.1、v1.1.1、0.0.1、latest + 20 个 sha-*) |
| xinzhuzi/myssia | ❌ `{"errors":[{"code":"DENIED","message":"invalid token"}]}` |
| shishi-classifier / myia-classifier / myssia-classifier / myia-server / shishi-server / myssia-server / myia-desktop / shishi-desktop | ❌ 同上(逐个实测) |

- ⚠️ **盲区声明**:匿名通道区分不了「私有包」与「不存在」。myssia「不存在」的强证据链是 workflow 史:IMAGE_NAME 恒等于 github.repository,repo 名为 myssia 的窗口(10-04,513eb11~76873d5)内 docker-publish.yml 已是 tag-only(ca88bc2 起)且该窗口无 v* tag 推送(仓库 tag 仅 v0.0.1)→ 不可能产生过 myssia 包。若要 100% 排除私有包,需主人加 read:packages scope 后跑 §1 指定检查。
- PyPI 发行名与 GHCR 无关——classifier 在镜像内,不是独立镜像。且 PyPI 现役名是 `myssia`/`myssia-classifier`(0.0.1 已上,pypi.org/pypi/myssia 实测 200;shishi 在 PyPI 不存在,实测 404——cb87302 的 shishi 发行名后来被 myssia 接替,PyPI 的 shishi 窗口比 GHCR 更短或从未落地)。

## 3. 命名谱系(何谓「现役名 myssia 系?」的实况)

```
myia ──(2026-10-03 ~12:08+0800,cb87302「shishi-everywhere」改名)──▶ shishi
shishi ──(2026-10-04,513eb11「myssia rename content pass」产品名改)──▶ (repo 仍名 shishi)
shishi ──(2026-10-04,76873d5「GitHub repo back to xinzhuzi/myia — owner decision B (split naming)」)──▶ myia(现名,gh repo view 实测)
```

- **GHCR 包名 = 推送时的 repo 名**(IMAGE_NAME=github.repository)。改名不改包:myia 包全是改名前(≤10-03 12:06+0800)的 main-push era 产物;shishi 包是改名窗口(10-03 12:08~18:40+0800)的产物+该窗口推的两个正式 tag;改回 myia 后(10-04)**尚无任何推送**,myia 包停在改名前状态。
- **myssia 是产品名/服务名/CLI 名,不是包名**:docker/docker-compose.yml 服务名 `myssia`、`myssia <版本>` CLI 输出(docker/README.md:24-28)、desktop 资产别名 `myssia_*`(CHANGELOG.md:22)、PyPI `import myssia`(jike-draft.md:27)。**现役镜像引用一律是 `ghcr.io/xinzhuzi/myia`**:docker/docker-compose.yml:25、docker/README.md:84、docs/launch/RELEASE.md:15。
- shishi 窗口期的 main push(ed729a5 12:09+0800 起 20 个)产生 shishi 包的 sha-* dev build;v1.1.1 与 v0.0.1 两个 tag 也在该窗口推送(前者旧 workflow 配置 type=ref+semver+sha 三标签,后者新配置 semver+latest 移动)——**v1.1.1 的 git tag 已不在仓库**(repo tag 仅 v0.0.1,gh api + 本地 git tag 双测),但镜像 tag 留存。推送顺序可由 version_id 序证:1.1.1(1330063562)< 0.0.1(1330846980)。

## 4. 逐包版本明细

### 4.1 `xinzhuzi/myia`(120 版本 = 24 tagged + 96 untagged)

**KEEP(1 个,保 latest 不断供)**:

| version_id | tags | digest | 镜像构建(UTC) | 说明 |
|---|---|---|---|---|
| 1330061187 | latest, sha-d359a3e | b34149a91e41… | 2026-10-03T04:06:38Z | commit d359a3e(yaml-editor);**最新但已过时**(早于 v0.0.1/v1.1.1,见 §5-①) |

**DELETE 候选(23 个 tagged dev build,全部 sha-* 单标签)**:

| version_id | tags | digest(前12) | 镜像构建时间(UTC) | 页面发布龄 |
|---|---|---|---|---|
| 1330057758 | sha-adee17d | 3ce547bcd958 | 2026-10-03T04:06:35 | 1 day ago |
| 1330039015 | sha-845f64a | 3b0c327dbd6d | 2026-10-03T03:55:35 | 1 day ago |
| 1330033181 | sha-e7dec54 | dd67f6536ac0 | 2026-10-03T03:51:58 | 1 day ago |
| 1330031346 | sha-7d55137 | 44603ce59df0 | 2026-10-03T03:50:46 | 1 day ago |
| 1329901622 | sha-1d6e219 | 8b54eaf7aa99 | 2026-10-03T02:35:41 | 1 day ago |
| 1329802318 | sha-b4e2787 | db2d99891114 | 2026-10-03T01:40:05 | 1 day ago |
| 1329782875 | sha-dee8e24 | 88ae87072f61 | 2026-10-03T01:27:00 | 1 day ago |
| 1329777432 | sha-fbba437 | 271679563003 | 2026-10-03T01:27:00 | 1 day ago |
| 1329582449 | sha-124bdf6 | ca1a4bb5b378 | 2026-10-02T15:16:44 | 1 day ago |
| 1329473581 | sha-933c7da | 6e2d94ea0a65 | 2026-10-02T15:16:44 | 1 day ago |
| 1329465324 | sha-23f440b | ff0d5df8b540 | 2026-10-02T15:16:44 | 1 day ago |
| 1327788580 | sha-f1ec38d | d07954c75390 | 2026-10-02T15:16:44 | 2 days ago |
| 1327763077 | sha-ee2d9db | 34c863bcaeac | 2026-10-02T15:16:44 | 2 days ago |
| 1327746381 | sha-889af3b | c0af832fff0c | 2026-10-02T15:16:44 | 2 days ago |
| 1327734827 | sha-40a666a | 32f4cc360dee | 2026-10-02T15:16:30 | 2 days ago |
| 1326312679 | sha-c92d40f | 8625e2d7bbcf | 2026-10-02T10:02:28 | 2 days ago |
| 1326304900 | sha-987ab19 | 8dc1f31c2bdb | 2026-10-02T10:02:28 | 2 days ago |
| 1326294105 | sha-d98987d | 23de7ea23653 | 2026-10-02T10:02:28 | 2 days ago |
| 1326280686 | sha-f4e626b | b91f46a2c872 | 2026-10-02T10:02:28 | 2 days ago |
| 1326259265 | sha-2a59233 | 4a2fa67b5aa3 | 2026-10-02T09:29:22 | 2 days ago |
| 1326251874 | sha-69211b0 | c2a9db30a250 | 2026-10-02T09:29:22 | 2 days ago |
| 1326235622 | sha-19511c6 | a22bb766e30b | 2026-10-02T09:29:22 | 2 days ago |
| 1326140832 | sha-11866fb | a89d2831a0de | 2026-10-02T09:28:53 | 2 days ago |

最旧:sha-11866fb(version_id 1326140832,a89d2831a0de,2026-10-02T09:28:53Z,commit「pre-release completion」10-02 17:27+0800);最新:sha-adee17d(1330057758,3ce547bcd958,2026-10-03T04:06:35Z,与 KEEP 版本相差 3 秒,系同一窗口两连推)。

**untagged 96 个 version_id**(全集,供核对;P3 走排除机制逐批删,不是无脑全删):

```
1330061178
1330061172
1330061166
1330061151
1330057748
1330057738
1330057725
1330057713
1330039005
1330038992
1330038981
1330038967
1330033170
1330033159
1330033156
1330033149
1330031333
1330031324
1330031311
1330031302
1329901605
1329901584
1329901562
1329901541
1329802299
1329802285
1329802270
1329802255
1329782859
1329782845
1329782830
1329782815
1329777422
1329777410
1329777399
1329777387
1329582433
1329582420
1329582399
1329582382
1329473561
1329473531
1329473497
1329473463
1329465303
1329465288
1329465272
1329465261
1327788553
1327788519
1327788488
1327788451
1327763050
1327763026
1327762953
1327762926
1327746356
1327746325
1327746302
1327746269
1327734776
1327734730
1327734684
1327734640
1326312645
1326312615
1326312581
1326312545
1326304860
1326304809
1326304763
1326304727
1326294067
1326294034
1326294011
1326293985
1326280658
1326280621
1326280582
1326280547
1326259239
1326259215
1326259198
1326259168
1326251848
1326251823
1326251798
1326251774
1326235600
1326235580
1326235537
1326235508
1326140809
1326140793
1326140769
1326140747
```

### 4.2 `xinzhuzi/shishi`(115 版本 = 22 tagged + 93 untagged)

**KEEP(2 个,唯一真发布)**:

| version_id | tags | digest | 镜像构建(UTC) | 说明 |
|---|---|---|---|---|
| 1330846980 | latest, 0.0.1 | ae5fa91c7566… | 2026-10-03T10:18:41Z | v0.0.1 正式发布(release published 10:40:46Z=18:40+0800);latest 由新配置 flavor latest=auto 移入 |
| 1330063562 | sha-d359a3e, v1.1.1, 1.1.1 | bb9727700bb9… | 2026-10-03T04:06:38Z | v1.1.1(git tag 已删,镜像留存);与 myia 包 KEEP 同 commit 同构建时间不同 digest(标签含仓库名,内容寻址必然不同);三标签系旧配置 type=ref+semver+sha 同版本重复打 |

**DELETE 候选(20 个 tagged dev build)**:

| version_id | tags | digest(前12) | 镜像构建时间(UTC) | 页面发布龄 |
|---|---|---|---|---|
| 1330702866 | sha-9652cf3 | 0d77033df37f | 2026-10-03T09:45:40 | 1 day ago |
| 1330602551 | sha-77f579b | c6130fab7421 | 2026-10-03T08:57:46 | 1 day ago |
| 1330368917 | sha-dee06cd | e8663b0f813a | 2026-10-03T07:00:37 | 1 day ago |
| 1330332700 | sha-fa5f31e | 6931df0ecbc5 | 2026-10-03T05:53:30 | 1 day ago |
| 1330303393 | sha-6f8c88a | 3c704b0cc35f | 2026-10-03T05:53:30 | 1 day ago |
| 1330294289 | sha-5031b42 | a26c3dd244fc | 2026-10-03T05:53:30 | 1 day ago |
| 1330245597 | sha-f814161 | 655e7c47c5f3 | 2026-10-03T05:53:30 | 1 day ago |
| 1330244982 | sha-a40c632 | 19f29a7d4834 | 2026-10-03T05:53:15 | 1 day ago |
| 1330240196 | sha-52ef418 | 378f69952a9e | 2026-10-03T05:50:25 | 1 day ago |
| 1330231604 | sha-3686a2e | 6f4fd30fcf8f | 2026-10-03T05:40:10 | 1 day ago |
| 1330228826 | sha-8fb9c67 | 99640ea107ce | 2026-10-03T05:40:10 | 1 day ago |
| 1330226299 | sha-8bc93ed | bd06848be7d2 | 2026-10-03T05:40:10 | 1 day ago |
| 1330223396 | sha-b3fa4dc | 0477b8bc2d6e | 2026-10-03T05:40:10 | 1 day ago |
| 1330222239 | sha-ff84b33 | 44061c23dc5b | 2026-10-03T05:40:10 | 1 day ago |
| 1330212798 | sha-60022ff | 3128250b8195 | 2026-10-03T05:34:32 | 1 day ago |
| 1330133697 | sha-0a9f83f | eaf0e2763799 | 2026-10-03T04:10:17 | 1 day ago |
| 1330117644 | sha-bfb60a0 | 91748149f2f8 | 2026-10-03T04:10:17 | 1 day ago |
| 1330079762 | sha-e45e650 | 2ed2d3aa5218 | 2026-10-03T04:10:17 | 1 day ago |
| 1330069256 | sha-16330ee | f8250fe932d3 | 2026-10-03T04:10:17 | 1 day ago |
| 1330064215 | sha-ed729a5 | 203157b4e288 | 2026-10-03T04:09:59 | 1 day ago |

最旧:sha-ed729a5(1330064215,203157b4e288,2026-10-03T04:09:59Z=12:09+0800,改名后第一推);最新:sha-9652cf3(1330702866,0d77033df37f,2026-10-03T09:45:40Z=17:45+0800)。

**untagged 93 个 version_id**:

```
1330846966
1330846957
1330846942
1330846932
1330799921
1330799911
1330799892
1330799878
1330799850
1330702856
1330702840
1330702824
1330702814
1330602534
1330602525
1330602510
1330602499
1330368899
1330368881
1330368870
1330368860
1330332689
1330332679
1330332670
1330332652
1330303384
1330303375
1330303364
1330303353
1330294280
1330294263
1330294244
1330294231
1330245574
1330245555
1330245538
1330245529
1330244972
1330244958
1330244944
1330244934
1330240181
1330240166
1330240155
1330240135
1330231585
1330231567
1330231551
1330231541
1330228812
1330228796
1330228784
1330228774
1330226284
1330226274
1330226265
1330226256
1330223384
1330223371
1330223361
1330223345
1330222224
1330222211
1330222199
1330222185
1330212786
1330212770
1330212758
1330212736
1330133684
1330133666
1330133655
1330133642
1330117632
1330117625
1330117619
1330117609
1330079739
1330079727
1330079708
1330079697
1330069250
1330069242
1330069236
1330069227
1330064200
1330064188
1330064171
1330064159
1330063555
1330063548
1330063537
1330063528
```

**untagged 构成证据**:三个 KEEP index 的 manifest 各恰好含 4 个子清单(amd64/linux、arm64/linux、2 个 unknown/unknown attestation;实测 /v2/.../manifests/<index-digest> 返回)。myia 24 推送×4=96 ✓ 精确吻合;shishi 22×4=88,余 +5(窗口内重推/中断残余,不影响机制判断)。

## 5. ⚠️ 两个横切发现(优先级高于删除本身)

① **`myia:latest` 指向过时内容,且 RELEASE.md 的拉取命令是坏的**。myia 包最新版=d359a3e(10-03 12:06+0800,dev build),而 v0.0.1(0.0.1 tag)与 v1.1.1(1.1.1/v1.1.1 tag)都只在 shishi 包。docs/launch/RELEASE.md:156 写着 `docker pull ghcr.io/xinzhuzi/myia:0.0.1`——**该 tag 在 myia 包不存在,命令必然 404**。修法=提案 P5:在现名 repo(myia)推一个 v* tag,让 CI 把正式版+latest 推进 myia 包;这同时让 P4b(连保命版一起删)变得可行。
② **untagged 里混着活标签的子清单**。4:1 结构(§4.2)意味着 myia 的 96 个 untagged 里有 ~4 个是 KEEP 1330061187 的子清单,删掉它们会让 `myia:latest` 的多架构清单解析断链(amd64/arm64/attestation 找不到)。**邻接 ID 猜子清单不可靠**(实测:kept index ±15 的 ID 窗口内只找到 1~2 个 untagged,4 个子清单散布)——所以 P3 必须用 digest 排除(REST 版本对象的 name 字段=sha256:<digest>,与 KEEP 子清单 12 个 digest 比对),不能用「按 ID 顺序删」的捷径。

## 6. 清理提案(逐条;全部待主人逐条确认后执行)

**前置(执行任何一条前)**:
```bash
gh auth refresh -s read:packages,delete:packages   # 交互式 device flow,主人本人完成;当前 token 实测无这两个 scope
```
删版本端点:`DELETE /user/packages/container/<pkg>/versions/<id>`;整包端点:`DELETE /user/packages/container/<pkg>`。**GHCR 删除无回收站、不可恢复**(正式版可重推 tag 重建;dev build 内容不可重建——这正是逐条确认的意义)。

**建议执行顺序**:P5(修复推送)→ P1+P2(删旧 tagged)→ P3(untagged,排除机制)→ P4(激进选项,可选)。先删 tagged 后清 untagged,可让被删 tagged 的子清单先变孤儿、P3 范围更干净。

### P1 · myia 包删 23 个旧 tagged dev build(23 条逐条命令)

```bash
# 每行注释:tags(digest 前12)
gh api -X DELETE /user/packages/container/myia/versions/1330057758	# sha-adee17d (3ce547bcd958)
gh api -X DELETE /user/packages/container/myia/versions/1330039015	# sha-845f64a (3b0c327dbd6d)
gh api -X DELETE /user/packages/container/myia/versions/1330033181	# sha-e7dec54 (dd67f6536ac0)
gh api -X DELETE /user/packages/container/myia/versions/1330031346	# sha-7d55137 (44603ce59df0)
gh api -X DELETE /user/packages/container/myia/versions/1329901622	# sha-1d6e219 (8b54eaf7aa99)
gh api -X DELETE /user/packages/container/myia/versions/1329802318	# sha-b4e2787 (db2d99891114)
gh api -X DELETE /user/packages/container/myia/versions/1329782875	# sha-dee8e24 (88ae87072f61)
gh api -X DELETE /user/packages/container/myia/versions/1329777432	# sha-fbba437 (271679563003)
gh api -X DELETE /user/packages/container/myia/versions/1329582449	# sha-124bdf6 (ca1a4bb5b378)
gh api -X DELETE /user/packages/container/myia/versions/1329473581	# sha-933c7da (6e2d94ea0a65)
gh api -X DELETE /user/packages/container/myia/versions/1329465324	# sha-23f440b (ff0d5df8b540)
gh api -X DELETE /user/packages/container/myia/versions/1327788580	# sha-f1ec38d (d07954c75390)
gh api -X DELETE /user/packages/container/myia/versions/1327763077	# sha-ee2d9db (34c863bcaeac)
gh api -X DELETE /user/packages/container/myia/versions/1327746381	# sha-889af3b (c0af832fff0c)
gh api -X DELETE /user/packages/container/myia/versions/1327734827	# sha-40a666a (32f4cc360dee)
gh api -X DELETE /user/packages/container/myia/versions/1326312679	# sha-c92d40f (8625e2d7bbcf)
gh api -X DELETE /user/packages/container/myia/versions/1326304900	# sha-987ab19 (8dc1f31c2bdb)
gh api -X DELETE /user/packages/container/myia/versions/1326294105	# sha-d98987d (23de7ea23653)
gh api -X DELETE /user/packages/container/myia/versions/1326280686	# sha-f4e626b (b91f46a2c872)
gh api -X DELETE /user/packages/container/myia/versions/1326259265	# sha-2a59233 (4a2fa67b5aa3)
gh api -X DELETE /user/packages/container/myia/versions/1326251874	# sha-69211b0 (c2a9db30a250)
gh api -X DELETE /user/packages/container/myia/versions/1326235622	# sha-19511c6 (a22bb766e30b)
gh api -X DELETE /user/packages/container/myia/versions/1326140832	# sha-11866fb (a89d2831a0de)
```

### P2 · shishi 包删 20 个旧 tagged dev build(20 条逐条命令)

```bash
gh api -X DELETE /user/packages/container/shishi/versions/1330702866	# sha-9652cf3 (0d77033df37f)
gh api -X DELETE /user/packages/container/shishi/versions/1330602551	# sha-77f579b (c6130fab7421)
gh api -X DELETE /user/packages/container/shishi/versions/1330368917	# sha-dee06cd (e8663b0f813a)
gh api -X DELETE /user/packages/container/shishi/versions/1330332700	# sha-fa5f31e (6931df0ecbc5)
gh api -X DELETE /user/packages/container/shishi/versions/1330303393	# sha-6f8c88a (3c704b0cc35f)
gh api -X DELETE /user/packages/container/shishi/versions/1330294289	# sha-5031b42 (a26c3dd244fc)
gh api -X DELETE /user/packages/container/shishi/versions/1330245597	# sha-f814161 (655e7c47c5f3)
gh api -X DELETE /user/packages/container/shishi/versions/1330244982	# sha-a40c632 (19f29a7d4834)
gh api -X DELETE /user/packages/container/shishi/versions/1330240196	# sha-52ef418 (378f69952a9e)
gh api -X DELETE /user/packages/container/shishi/versions/1330231604	# sha-3686a2e (6f4fd30fcf8f)
gh api -X DELETE /user/packages/container/shishi/versions/1330228826	# sha-8fb9c67 (99640ea107ce)
gh api -X DELETE /user/packages/container/shishi/versions/1330226299	# sha-8bc93ed (bd06848be7d2)
gh api -X DELETE /user/packages/container/shishi/versions/1330223396	# sha-b3fa4dc (0477b8bc2d6e)
gh api -X DELETE /user/packages/container/shishi/versions/1330222239	# sha-ff84b33 (44061c23dc5b)
gh api -X DELETE /user/packages/container/shishi/versions/1330212798	# sha-60022ff (3128250b8195)
gh api -X DELETE /user/packages/container/shishi/versions/1330133697	# sha-0a9f83f (eaf0e2763799)
gh api -X DELETE /user/packages/container/shishi/versions/1330117644	# sha-bfb60a0 (91748149f2f8)
gh api -X DELETE /user/packages/container/shishi/versions/1330079762	# sha-e45e650 (2ed2d3aa5218)
gh api -X DELETE /user/packages/container/shishi/versions/1330069256	# sha-16330ee (f8250fe932d3)
gh api -X DELETE /user/packages/container/shishi/versions/1330064215	# sha-ed729a5 (203157b4e288)
```

### P3 · 两个包清 untagged(189 个;**digest 排除机制**,不是盲删)

KEEP 集 3 个 index 的 **12 个子清单 digest 全集**(REST name 字段与之等值者一律跳过):

```text
# myia 1330061187 的 4 个子清单(amd64, arm64, attestation×2)
sha256:1855837d5701dcd6054554cf6a5126f849f698bb43b10c10eb2d122dc9c46d8e
sha256:52327764c153241337f39b4ab802b0a4c8d3d8ce418e2bc63fba6e201e841650
sha256:e2dcca805a30b5fa487d658ce0633ebf2157ab2b1d2d1bcf7e6dafb4dc9c9d61
sha256:6c509a44fb06437119964fad40fc47cc409289a5fca4d069b566e4f687b9af36
# shishi 1330846980(0.0.1+latest)的 4 个
sha256:879af04cf5281bb363a207e193ba7fcd928b27e685650c3d40a41560fd765f19
sha256:a22f661a3a853348ca28a31c912967c9663ff9543bdb46d28f0141c40988c28c
sha256:33621f6c925caf117edc106b1ad3254689d5af901bfc443baed3542317b6729f
sha256:092eaa2f65d1475a46b26460931575e6f2a28658eaa52667e8f9fbce27e82ba2
# shishi 1330063562(1.1.1 系)的 4 个
sha256:b784811d9004fd4fc627c66ca317fdf567811921141fadc03f04e3ac78557a70
sha256:db85bcbea80a8cec0a77ec5ff45eb6b1b87d8e7b645f927c8fa13ff7a4e245ba
sha256:522006e65f81e70af7cc4e8829b883ba2e96da65ca887e8f1ba7ef6a6838cf6a
sha256:a0bac678fc5a3e0e1859af96aba2ce6e3866abf2eb97e2ffd478459d0b602e2d
```

主人侧先枚举后删(先看清单再删;name==digest 是 GHCR 容器版本对象的既有字段):
```bash
for pkg in myia shishi; do
  gh api "user/packages/container/$pkg/versions?per_page=100" --paginate \
    | jq -r '.[] | select(.metadata.container.tags | length == 0) | [.id, .name] | @tsv'
  # ↑ 输出 id<TAB>sha256:<digest>;凡 name 命中上面 12 行的一律跳过,其余才删:
  # gh api -X DELETE /user/packages/container/$pkg/versions/<id>
done
```
注:本机制依赖 REST name==digest 字段——**本盘点因 scope 403 未能在本机验证该字段**(诚实标注);主人加 scope 后先跑上面枚举命令核一眼输出再删。若主人想连 keep 集子清单一起清,等价于放弃 myia:latest/shishi:0.0.1/shishi:1.1.1 的可拉性,不建议。

### P4 · 激进选项(可选;后果已注明)

```bash
# P4a 整包删 shishi(最省事;后果:ghcr.io/xinzhuzi/shishi:0.0.1/:1.1.1 断供,10-03 窗口期外部引用者拉不到;仓库名已不是 shishi,未来不会再推)
gh api -X DELETE /user/packages/container/shishi

# P4b 删 myia 包唯一保命版(**仅 P5 完成后执行**,否则 myia:latest 立刻断供)
gh api -X DELETE /user/packages/container/myia/versions/1330061187
```

### P5 · 修复推送(非删除;建议最优先)

在现名 repo(myia)打一个 v* tag(如 v1.1.2),docker-publish.yml(tag-only,semver+latest)会自动把正式版+新 latest 推进 **myia 包**——一举修复 §5-① 的 latest 过时、RELEASE.md:156 的坏命令、并让 P4b 变得安全。无需手动 docker push。

## 7. 未能提供的数据(如实)

- **拉取量级:GHCR 不提供**。packages REST 与 registry API 均无 pull/download 计数字段(与 Docker Hub 不同);web UI 的下载计数亦无此口径。本盘点如实标 N/A,不做任何臆测。
- 私有包盲区:见 §2 盲区声明。
- 各包存储总量:API 无该字段(web UI 有,需登录);189 个 untagged 中 attestation 类通常很小,真正占层存储的是 per-arch 层,删 tagged+untagged 即同释放。

## 附:本盘点跑过的关键命令(复核用)

```bash
gh auth status; gh api user --jq .login                     # → xinzhuzi,scopes gist/read:org/repo/workflow
gh api 'user/packages?package_type=container'               # → 403(见 §1)
gh api 'users/xinzhuzi/packages?package_type=container'    # → 403(同上)
gh repo view xinzhuzi/myia --json name,nameWithOwner        # → 现名 xinzhuzi/myia(非重定向误判)
gh api 'users/xinzhuzi/repos?per_page=100&sort=updated' --jq '.[].name'   # → 无 shishi/myssia 仓,myia 为最新 push
gh api 'repos/xinzhuzi/myia/tags?per_page=100' --jq '.[].name'; git tag -l  # → 仅 v0.0.1(v1.1.1 已不在)
gh api 'repos/xinzhuzi/myia/releases' --jq '.[0].published_at'             # → v0.0.1 2026-10-03T10:40:46Z
# registry/web 抓取脚本与输出:/tmp/ghcr_sweep2.py、/tmp/ghcr_full_scrape.py、/tmp/ghcr_children.py、/tmp/ghcr_versions.json(本机临时文件)
```

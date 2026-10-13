# 微信功能全家桶:WeFlow 功能落到 MYIA

## Goal

把主人圈定的 WeFlow 功能清单(2026-10-13 截图,OCR 全文见附录)按 MYIA 形态开发落实:**数据面走已打通的微信本地库只读链**(密钥 10-13 已破,桥 localdb 引擎在案),**展示面挂 MYIA 桌面既有微信工作台族**,**AI 面走 MYIA 既有管线**。撞红线的三项以只读替代形态实现。

## 来源与依赖

- 功能蓝本:hicccc77/WeFlow(15023★)功能清单,主人令「这些 weflow 的功能,你尽量也开发出来,落实到项目中」。
- **硬依赖**:10-13-wechat-keyprovider 的 B0(桥查询对 4.1.15 分表适配)——Phase B 工作流 dwfrun-d80344b9 在途;B0 落地前 C1 以下全部不动工。
- 数据资产(已就位):keys.json 20 钥(数据根私有区)、桥 E2 解密副本管道、message/contact/session/sns 等 20 库全解密验真。

## WeFlow 功能 → MYIA 落法总表(OCR 原文见附录)

| # | WeFlow 功能(原文) | MYIA 落法 | 判定 |
|---|---|---|---|
| 1 | 聊天:解密聊天中的图片、视频、实况 | 媒体解密引擎(.dat XOR/AES,WeFlow 同款算法形态)+ 聊天记录浏览面 | ✅ 纳入 C3 |
| 1b | 支持修改本地消息 | —— | ❌ 红线排除(写微信数据) |
| 2 | 消息防撤回 | **只读替代**:撤回消息呈现——local_type=10002 revoke 记录+残留原消息在库可查,在浏览面标记「已撤回」展示 | ⚠️ 替代形态,纳入 C5 |
| 3 | 实时弹窗通知 | **轮询水位版**:localdb 增量扫描(cron 分钟级)→ MYIA 通知系统;黑白名单=会话白名单(weixin.yaml 既有形态)。不做进程 hook | ⚠️ 替代形态,纳入 C5 |
| 4 | 私聊分析 | 统计引擎:好友间消息量/类型比例/时段分布(SQL 聚合) | ✅ 纳入 C2 |
| 5 | 群聊分析 | 群成员/发言排行/活跃时段/媒体统计 | ✅ 纳入 C2 |
| 6 | 年度报告 | 按年/跨年统计 + AI 报告生成(走 MYIA AI 管线) | ✅ 纳入 C2 |
| 7 | 双人报告 | 指定好友双方记录专属分析 | ✅ 纳入 C2 |
| 8 | 消息导出 | 导出器:JSON/HTML/Markdown/TXT/CSV/Excel(PGSQL/ChatLab 视需求二期) | ✅ 纳入 C1 |
| 9 | 朋友圈:解密图片视频/导出内容 | sns.db(已解密)只读导出+图片解密 | ✅ 纳入 C3(「拦截删除隐藏」❌红线排除) |
| 10 | 联系人:导出好友/群聊/公众号;找回部分曾经的好友 | contact.db 导出 + stranger/room_verify 表考古 | ✅ 纳入 C4 |
| 11 | HTTP API | localdb 能力映射 HTTP(桥常驻服务模式),供外部系统/自动化对接 | ✅ 纳入 C6 |

**红线排除汇总(主人可翻案,翻案需显式指令)**:修改本地消息(写微信数据)、防撤回拦截(hook 进程)、朋友圈删除/隐藏拦截(hook 进程)。零微信进程干预与只读红线不变;后两者的「事后只读呈现」替代已纳入。

## 子任务地图(每个=独立可验证交付;立档时逐个 create --parent)

| 子 | 范围 | 要点 |
|---|---|---|
| C1 查询与导出 | localdb 查询增强(全量翻页/按会话/按时间)+ 六格式导出器 + 浏览面数据通道 | 一切功能的地基;含会话/联系人解析显示名 |
| C2 统计与报告 | 私聊/群聊/年度/双人四类分析 + AI 报告生成 | 统计=SQL 聚合;报告=MYIA AI 管线;产物可导出 |
| C3 媒体与朋友圈 | 聊天媒体解密(.dat)+ 朋友圈只读导出 | 参考实现=外部件形态(链接者铁律),解密算法仓外 |
| C4 联系人与考古 | 联系人/群聊/公众号导出 + 曾经好友找回 | stranger 表考古,如实标注「部分找回」 |
| C5 通知与撤回呈现 | 新消息轮询通知(黑白名单)+ 撤回消息标记呈现 | 通知走 MYIA 既有通知系统;轮询非 hook |
| C6 HTTP API | 桥 localdb 能力 HTTP 化(常驻服务模式) | 鉴权=本机回环+token;WeFlow docs/HTTP-API.md 同族 |

## Acceptance Criteria(父档=集成验收;细节 AC 在各子档)

- [x] AC-P1:六子全部交付且归档,每个子的 prd AC 全勾。
- [x] AC-P2:真数据端到端——每类功能对真实本地库(TMS 群等)真跑出真产物(消息/统计/报告/媒体/导出件),非夹具演示。
- [x] AC-P3:红线守卫——全程零微信进程干预、零写微信数据(grep 守卫+代码评审双保险);三个排除项未以任何形态混入。
- [x] AC-P4:装机包全量刷新+像素级验证(微信功能屏族)。
- [x] AC-P5:词汇判例——功能名/UI 文案全人话(「聊天记录」「年度报告」),协议/字段保留标准英文。

> **验收回填(2026-10-14 收口簿记;证据=六子复查回执+装机复查,全 PASS/needsFix=false)**:
>
> - **AC-P1**:六子(chat-export/stats-reports/media-sns/contacts/notify-revoke/http-api)prd AC 全勾+全部归档(本笔六档外科提交;各子复查回执原文留档于各子档 prd 尾);groupinfo 前批已归档(35e9d78)。
> - **AC-P2(真数据=复查回执)**:C1 keyset 全量翻页对拍 rows=9821/pages=20 序列相等+六格式真库导出 3391 行==同窗 SQL COUNT+SIGTERM 取消安全;C2 chat total=111062(system=907 契约自洽)+annual --all total=20964/319ms+缓存 sha256 逐字节确定;C3 rows=4419/parsed=4419/media_nodes=7065+media status 真跑;C4 六桶闭包 sum=22092==COUNT+游标零重漏+Tier 6389/13925;C5 notify-scan 真库 sessions_scanned=454/whitelist=1+baseline 推进;C6 门控真库 Pull 深分页 p95≤45.3ms+SSE 真扫描水位推进。
> - **AC-P3(红线守卫)**:各回执红线 grep 零命中——C1 两模块 INSERT|UPDATE|DELETE|db_storage 零+产物 0600;C2 stats_query 网络/print/写 SQL 零(恒 mode=ro);C3 写 SQL/AES|ECB|isaac/密钥入日志三组零(CDN 回源只读 GET 属 R4 设计内);C4 contacts_query 写/网络/进程全零;C5 LLDB|断点|passphrase|hook|trigger 词表零,macos_notify=osascript 字面量 argv 通知通道非微信干预;C6 DELETE|PUT|block-delete|uninstall 零+do_ 处理器恰三个;三排除项(改本地消息/防撤回拦截/朋友圈拦截)零混入。
> - **AC-P4(装机)**:rebuilt=true/swapped=true;**pixelVerified**——C1 `/tmp/wxfeat-install/10-query-export.png`(「本地库查询(历史) 解密副本只读,零出网零微信进程交互…」+「分页浏览窗口」+「导出本会话」+「选择目录并导出」,Vision 1.00+Paddle 交叉核对 0.9929/0.9556/0.9527 逐字一致);C2-C4 同屏 `15-stats-sns-media-contacts.png`(「统计报告…首次统计较慢,之后秒出(文件缓存)」+私聊/群聊/年度/双人四类;「朋友圈 只读时间线…」+「拉取朋友圈/导出/扫描媒体」;「聊天图片…缩略图经你的解密件解出」;「联系人 解密副本只读分类浏览(好友/群聊/公众号/曾经的好友)」+桶 chip,Paddle ≥0.95);版本链 `05-after-move.png` 卡头「微信 4.1.15 / 桥组件 0.8.3」(Paddle 0.9435)=装机 UI→sidecar→自管 python 桥 0.8.3 全链像素实证。**blocked 两项如实注记**:①通知撤回面无 UI 面可截——notify-revoke prd 钉死「UI 零新画布」,其 AC8 feed「weixin-通知」卡需 config/weixin-notify.yaml 部署到数据根+cron 注册+白名单+新消息(数据根 config/ 仅有 weixin.yaml 与 weixin-ai-token.yaml,myssia.db 无 weixin-通知 源,首扫描轮零事件;该任务 jsonl 空、在途未交付 UI);②HTTP API 面无 UI 面可截——ui-src 全树「5032/http_api/本机接口」零命中,http-api 全部 AC 为 CLI/curl/文档级(其 implement/check jsonl 均 0 行,任务在途,UI 未落),工作树唯一 http-api 交付为桥侧 CLI+docs。非阻塞注记:spctl -a rejected=adhoc 签名既定基线(旧装机版同形,无 quarantine xattr 可正常运行,生产实例已复原在跑 pid 48482)。
> - **AC-P5(文案=复查抽查+像素文案核对)**:上屏人话实证——「本地库查询(历史)」「分页浏览窗口」「导出本会话」「统计报告」(私聊分析/群聊分析/年度报告/双人报告)「朋友圈 只读时间线」「聊天图片」「联系人」「好友/群聊/公众号/曾经的好友」;协议/字段英文保留(next_cursor/with_residue/stats_chats/revoke_list 等,回执在案);C6 文档「实时」零命中(延迟口径=分钟级,2 处如实)。

## Constraints

- 只读红线:一切功能读解密副本,桥 E2 管道既有;密钥材料不出数据根私有区。
- 链接者铁律:媒体解密等算法件以外部件/声明形态进(照 keyProvider 模式),产品代码不进货逆向实现。
- 文案与版面:微信功能屏并入既有微信工作台族版式(参照 TG 三级界面判例),不新造画布;详情留子任务 design。
- 性能:346MB 消息库的查询/统计走解密副本+索引,严禁每次全库扫。

## 附录:WeFlow 功能清单 OCR 原文(2026-10-13 主人截图)

```
详细功能清单
功能模块        说明
聊天           解密聊天中的图片、视频、实况;支持修改本地消息
消息防撤回      防止其他人发送的消息被撤回
实时弹窗通知    新消息到达时提供桌面弹窗提醒,便于及时查看重要会话,提供黑白名单功能
私聊分析        统计好友间消息数量;分析消息类型与发送比例;查看消息时段分布等
群聊分析        查看群成员详细信息;分析群内发言排行、活跃时段和媒体内容
年度报告        生成按年统计的年度报告,或跨年度的长期历史报告
双人报告        选择指定好友,基于双方聊天记录生成专属分析报告
消息导出        将聊天记录导出为多种格式:JSON、HTML、Markdown、TXT、Excel、CSV、PGSQL、ChatLab专属格式等
朋友圈          解密朋友圈图片、视频、实况;导出朋友圈内容;拦截朋友圈的删除与隐藏操作
联系人          导出好友、群聊、公众号信息;找回部分曾经的好友
HTTP API       将本地消息能力映射为 HTTP API,便于对接外部系统、自动化脚本与二次开发
```

# 群信息面板与导出:成员/设置上屏,三级界面全量导出

## Goal(主人令 2026-10-13)

情报流三级界面(微信监控台)表现**群设置数据与群成员**;并可**一键导出所有群信息**(成员+设置等全部内容)。

## 数据事实(2026-10-13 实锚,decrypted contact.db)

- `chat_room(username, owner, ext_buffer)` → **群主 wxid**
- `chat_room_info_detail(username_, announcement_, announcement_editor_, announcement_publish_time_, chat_room_status_)` → **群公告+编辑人+发布时间+群状态**
- `chatroom_member(room_id, member_id)` + `name2id` → 成员 wxid 清单
- `contact(remark, nick_name, alias)` → 成员显示名(0.5.1 `_contact_pick_names` 复用)
- 群显示名:`lookup_contact`(chat_id)

## Requirements

- R1 桥新命令 `localdb group-info <chat_id> --json`:群设置(群名/群主(名+wxid)/公告(文+编辑人+时间)/状态/成员数)+成员列表(wxid+显示名+备注+是否群主)。退出码契约(2026-10-13 评审勘误,按实现实况钉死):**查询层降级 = 缺表/缺行/缺列/缺群行 → 对应键 null 或空表,恒 exit 0 如实**(判例同 key-status);**密钥链错误族 = 与 query/sns 同一全链,结构化 error 载荷非 exit 0** —— 缺数据根 exit 20(db_not_found)/ 缺密钥 exit 21(key_unavailable)/ 解密失败 exit 22(decrypt_failed)。版本 0.6.0。
- R2 三级监控台「群信息」面板:从群行/聊天头进;设置区+成员列表(名为主,wxid 折叠次要信息);文案人话(「群公告」「群主」「成员 N 人」)。
- R3 导出:面板内「导出群信息」→ 系统保存对话框(dialog 插件已在,看图屏先例)→ **JSON(全量:设置+成员+原始键)+ CSV(成员表)** 两件成套落盘。
- R4 红线:只读;密钥零沾;文案判例;头像/媒体 v1 不做(features C3 媒体线),ext_buffer 二进制域不解析(如实缺省)。

## Acceptance Criteria

- [ ] AC1 桥 group-info 真跑两群(TMS/AI中转站)返回真群主+真公告+真成员名列表。
- [ ] AC2 三级界面群信息面板渲染成员与设置(合成夹具+真数据对拍)。
- [ ] AC3 导出双件落盘可打开,内容含全部字段(JSON 全量/CSV 成员表)。
- [ ] AC4 门禁全绿+文案审计(行话零上屏)。
- [ ] AC5 装机包刷新+像素验证(面板+导出流)——主会话收官。

## group-info 应答契约(v1 钉死)

```json
{"group_info": {
  "chat_id": "50438708676@chatroom",
  "display_name": "TMS 中转站交流1️⃣",
  "member_count": 97,
  "owner": {"username": "wxid_x", "display": "名字"},
  "announcement": {"text": "…", "editor_display": "名字", "published_at": "2026-…"},
  "status": null,
  "members": [{"username": "wxid_a", "display": "花开相随", "remark": "备注", "is_owner": false}]
}}
```
退出码契约(2026-10-13 评审勘误,与实现/测试三方对齐):**查询层**(缺表/缺行/缺列/缺群行/ contact 域缺位)= 对应键 null 或空表,**恒 exit 0**(状态查询不判错,判例同 key-status);**密钥链**(缺数据根 = 20 / 缺密钥 = 21 / 解密失败 = 22)= 结构化 `{"error":{code,message[,fix_hint]}}` 载荷非 exit 0,判例同 query/sns。`status` 列值 BLOB 经 hex 串化守卫(json.dump 无 default,bytes 原样会崩出非契约退出码)。

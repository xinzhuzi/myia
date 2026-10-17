# 情报流 3 级聊天工作台直接渲染微信消息真图

## Goal

主人令(2026-10-16 凌晨):微信消息图片在情报流 3 级聊天工作台直接渲染。
前置已闭环(10-15-media-key-hunt):钥入库(钥匙串 16-ASCII 形态)、解密件
全链通(`localdb media decrypt` → media-cache 原子落图)、外置件通道接线。
本档 = UI 消费面:消息 → 媒体引用 → 解密/服务 → 气泡内 <img> 渲染。

## 已知弹药(承 media-key-hunt window5-result.md)

- 解密:`scripts/wechat-bridge-mediadecrypt.py`(协议 v1,系统 python3+openssl
  即可跑);桥 `localdb media decrypt <dat>` 全链通;`media.py scan_chat_media`
  已有 R2 寻径(local_type 3=图:packed_info_data 32-hex key → msg/attach/
  <dir>/<yyyy-mm>/Img/<key>[_t].dat,缩略图优先;43=视频明文)。
- 缓存:数据根 wechat-localdb/media-cache/(600/700,LRU 容量治理)。
- httpapi 有媒体下发面(R7:allowlist 目录 http-media)——与 media-cache 的
  关系待探(C6 注记说 media-cache 是指定读取落点,两目录名不一致需核)。
- UI:3 级聊天工作台(TG/微信同构双栏;气泡 data-item-key=dedup_key)。

## 待探(研究先行)

1. 微信消息怎么变成 feed 条目(localdb page/export → 何引擎消费 → store)?
   条目现在带不带媒体信息(dat key/类型)?
2. 图片怎么到 webview:桥 HTTP(httpapi+token)直连 / Tauri asset 协议 /
   sidecar IPC 转发 base64,选型(装机件约束:assetProtocol scope 现状)。
3. 3 级气泡渲染点(we Chat 消息当前渲染什么形态;TG 图怎么处理——TG 线
   是否已有图片渲染可复用)。
4. 撞面:并行会话在途的 localdb_export.py 改动(会话初 git status 有 M,
   现已提交——先读现状)。

## Acceptance Criteria

- [x] 微信图片消息在 3 级工作台渲染出真图(Phase1 引擎 29e7bb37:image 行
      出条目+media scan 解密回填 image_files;Phase2 1b147007:气泡槽
      FeedLocalImages + feed_images.rs 双授权根 images/+media-cache)
- [x] 解密失败/未配置/文件缺失 = 结构化降级(占位「[图片]」条目仍在;wxgf
      后缀放行但魔数拒授权 → UI 人话降级「图片不可预览」)
- [x] 私有数据红线:引擎日志形状级;测试全合成路径;media-cache 不进 git
- [x] 门禁全绿(tests/engines 827 + vitest 943 + tsc + cargo feed_images 5)
- [x] 打包覆盖安装(见下方执行记录)
- [ ] 主人真机看图终验(装机后开 feed 微信渠道 3 级;首轮采集解密可分钟级,
      稳态缓存秒回)

## 执行记录

- Phase1(29e7bb37):engine.py 图片行占位+media scan 回填+300s 超时地板。
- Phase2(1b147007):feed_images.rs 双授权根(canonicalize 囚禁+魔数门,
  wxgf 天然拒);气泡槽 tg|wx 通用;并行会话 5 个基线件(feed_images.rs/
  feed-local-images/main.rs 挂载/tauri.conf CSP/feed-screen)自洽入树,
  出处已在提交信息注记——若并行会话后续提交撞同文件,以内容等价收编论,
  交主人仲裁。

## 边界

- 视频渲染不在本档(视频=明文直读,后续按需);wxgf 实况容器如实占位
  「实况格式,暂不支持预览」。

# TG线健壮性吸收(TG-Manage参考批):体检按钮+扫码提示+配置档备份

## Goal

主人令(2026-10-11):参考 https://github.com/hikling/TG-Manage (BSD 3-Clause,判例同 Crawlab 可直借)吸收健壮性机制——**红线:严禁整仓/整文件拷贝**,逐件找能吸收的机制,或模仿重写贴本仓架构(注释风格/测试面/判例)。

背景:他们全套建立在常驻 Pyrogram 用户会话(api_id)上;我们三线是 bot/网页(零凭据)/休眠 Telethon。吸收评估已由主会话完成(2026-10-11),分「现在能吃」与「锁 B 线 api_id」两档。

## Requirements

- **AC1 账号体检**(TG-Manage 按需检测的模仿):Telegram 屏账号行「检测」按钮 → 复用 `web_line.check_logged_in` 无头探针(不新写浏览器逻辑)→ 结果写登录标记 `last_verified_at`/`alive` → 行态即时刷新;sidecar 新方法 `telegram.web.check {account}`;CLI `myssia telegram check --account <键>`(AI 侧重登前探活)。体检走后台线程(浏览器探针 5-45s 不许堵协议),并发体检同键幂等拒。
- **AC2 扫码提示**:登录窗与卡面指引文案补「会话失效时登录页可直接用手机 TG 扫码,免等验证码」。
- **AC3 配置档本地备份**(backup_archive 思路):登录成功时把配置档 tar.gz 到 `<数据根>/telegram-web/backups/<账号键>-<UTC时间戳>.tar.gz`(0600,目录 0700,只留最近 3 份);如实注记:本地损坏可回滚,**服务端吊销不救**。
- **红线**:不动 wechat 会话在途文件;不 git 提交(主会话收口);TG-Manage 参考件允许 gh api 只读取证,产物零直接粘贴。

## Acceptance Criteria

- [x] AC1 体检按钮+last_verified_at+CLI(pytest 协议 7 面+单测 4 例+vitest 5 用例+冒烟体检链;工作流 dwfrun-bd10743d)
- [x] AC2 扫码提示文案在登录窗回执与卡面指引(断言在测)
- [x] AC3 备份落盘+滚动保留 3 份+权限(单测 5 例:落盘/滚动/挂钩/失败不拦/回执文案)
- [x] 全量门禁绿:pytest **5146/0**+vitest+tsc+build+ruff 全绿;冒烟 14 项(扫码/体检/删除链)
- [x] 装机覆盖安装:tauri 全量重打包(17.88MiB+DMG)+备份换装+重签 strict+缓存清;**装机态真体检 telegram-alt1 一次=活**(CLI 经装机包代码跑真无头探针,exit 0,标记落 last_verified_at=20:12:37/alive=true);app 重启 web 线 6 进程恢复

## 锁下批(P1/P2,等 B 线 api_id,不做)

P1 `/code` 验证码中继(777000 近 5 分钟正则抽码/冷却 45s/零持久化);P2 设备列表/踢会话(GetAuthorizations);P3-full 按账号代理+flood 退避。不吸收已裁:聊天收发(只读红线)/TeleBox(违背唯一管控面)/外观与云备份(运营外围)/批量 200 面(我们 max 3)。

## 过程注记

- 方案经独立评审员两轮过审(第一轮 must_fix 打回,复审通过);实现偏离两处如实注记:_ACTIVE_PROBES 进程级登记表替代台账反查(依赖方向)/CLI profile_missing 单列人话分支;方法计数守卫 79→80 同步。
- 并行会话 wechat-bridge 中途落库 af4f1d0,git show 核验零涉本批 surfaces;全量 pytest 在其之后跑仍 5146/0。

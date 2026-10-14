# 收尾三件套:FIFO 竞态修复(判活后)+密钥明文文件删除+.developer 修复

## 背景(主人全清令)

三件:①`src/myssia/push/macos_notify.py` FIFO 竞态按 10-15-ocr-revive 转交注记
方案修(先判活并行线,活跃则避让);②数据根 `.migrated` 明文密钥删除(判稳后);
③`.trellis/.developer` 缺失修复。流程:探索(判活/判稳)→计划+grill→执行三域→
全量门禁回炉→深度评审→装机→簿记(先码后档再推)。

## 档案断裂说明(如实)

工作流 phase-1 的 `task.py create` 当时因 task.py「No developer set」断裂
(.developer 缺失——恰为本任务 env 域要修的病灶),任务档未建成;env 域修复后
簿记段以原参数补建本档,域内工作全程在档外完成、回执在此终局补记。

## Requirements 与终局回执(键=指派规范键,逐字)

- **R1 `fifo`**:done=true。中继 FIFO 竞态根治(转交注记最小修):先开读端
  `O_RDONLY|O_NONBLOCK` 立即成(确立读者在位),再开自持常开写端
  `O_WRONLY|O_NONBLOCK`(中继存活期持有不关)→ 读端永不 EOF,同轮第二条
  `_fifo_write` 的无读者 ENXIO 空窗消除(门禁 flaky 根因);读者线程改持常开
  fd 阻塞逐行读;宿主进程死=fd 全关,写者侧 ENXIO 回退 osascript 契约不变。
  落点:提交 `10defa11`(1 文件 45+/19-,diff 全量即此修,零夹带;gitnexus
  detect-changes staged=8 符号 0 流程 low)。域内回执 evidence 由编排线持有;
  门禁与深度评审为编排回执(门禁绿/评审过),簿记段未重跑(见下)。
- **R2 `keyfile`**:done=true。数据根明文密钥 `.migrated` 删除(判稳后:钥匙串
  迁移链证据齐、keys-unmigrate 回退通道在)。簿记段亲验:`find ~/.myia
  ~/Library/Application Support -maxdepth 4 -name 'keys.json.migrated*'` 零命中
  (2026-10-15)。
- **R3 `env`**:done=true。`.trellis/.developer` 重建(`name=xinzhuzi`,
  initialized_at=2026-10-15T06:41:08,gitignore 内文件不入册);簿记段亲验:
  `task.py list --mine` 裸跑通过(4 任务列表,无 TRELLIS_DEVELOPER workaround)。

## Acceptance Criteria(编排回执代勾判例:注记勾,不虚增亲验)

- [x] AC1 fifo:修复已提交(`10defa11`),编排回执 done=true;门禁绿/评审过为
      编排回执,簿记段未重跑(注记代勾)。
- [x] AC2 keyfile:`.migrated` 零残留(簿记段亲验 find 零命中)。
- [x] AC3 env:`.developer` 在位且 task.py 裸跑即过(簿记段亲验)。
- [x] AC4 簿记:先码(`10defa11`)后档(本档归档提交)再推(origin main),
      并行线在途件(sendmsg 档补笔/UI 屏族件/frontend-ui.md 主题档)全程未碰。

## 遗留(留主人/后线)

- 门禁(just test/check)与深度评审、装机验证回执属编排线台账,本簿记段未重跑
  未亲验;CI 推送后 fifo flaky 消面以审计员五项核验为准。
- 红线遵守:v0.0.4 tag 未打、不打。

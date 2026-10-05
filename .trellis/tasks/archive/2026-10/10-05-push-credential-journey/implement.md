# implement:推送凭据用户旅程接通

白名单(提交面):`src/myssia/push/{base,feishu_card,telegram,webhook}.py`、
`desktop/ui-src/src/screens/settings/settings-screen.tsx`、
`desktop/ui-src/src/screens/messaging/platform-overview.tsx`、
`tests/push/*`、`tests/test_schema.py`(如需)、
`desktop/ui-src/src/screens/settings/settings.test.tsx`、
`desktop/ui-src/src/screens/messaging/messaging-screen.test.tsx`、任务档、spec、journal。

## 步骤(每步后跑对应验证)

- [ ] 0.1 gitnexus impact:resolve_credential/FeishuCardChannel/TelegramChannel/
      WebhookChannel 上游面记录(detect-changes 前置基线)。
- [ ] 1 base.py:`resolve_channel_credential` helper(env 优先→kc 回退→
      env_var_missing+指引文案)+ 单测(InMemory 注入三态)。
- [ ] 2 feishu_card.py:`TOKEN_API_URL`+`_obtain_token`(async 三级:注入→
      BOT_TOKEN 回退→APP_ID/SECRET mint+缓存 120s 提前量)+`_resolve_target`
      回退 FEISHU_CHAT_ID;discover/带图路径统一切 `_obtain_token`;
      单测:MockTransport mint 成功/非零 code/缓存命中/手工 token 直用。
- [ ] 3 telegram.py / webhook.py:token/target/endpoint 解析点接 helper;
      单测:回退命中/双缺 env_var_missing 文案含「设置→推送」。
- [ ] 4 settings-screen.tsx 推送分区重做(D3)+ settings.test.tsx push
      describe 重写(预设字段保存/空跳过/测试按钮 target 组装)。
- [ ] 5 platform-overview.tsx 指南重写(D4)+ messaging-screen.test 指南
      断言改写(去 curl/zshrc,含「设置→推送」)。
- [ ] 6 门禁全量:pytest 定向(tests/push tests/test_schema.py tests/test_secrets.py)
      + ruff;npm run test 全量 + build;detect-changes staged。
- [ ] 7 提交(fix(python) 批 / feat(desktop) 批 / docs 批,pathspec)。
- [ ] 8 装机链(worktree HEAD→build→换装→exit 文件);装机版冒烟:
      secret list 零弹窗 + push.test stdout 通道回显。
- [ ] 9 勾 AC、task.json→review、journal、终报(AC7 留真机凭据步骤单)。

## 回滚点

- 每步独立可回退;解析回退(D1)单独成 commit,UI(D3/D4)单独成 commit;
  装机前 tag 不打,回滚=换回 /tmp 备份包。

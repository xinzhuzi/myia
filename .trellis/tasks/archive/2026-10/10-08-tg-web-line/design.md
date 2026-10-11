# design.md — 10-08-tg-web-line 技术设计(执行级,多账号一等能力)

## D1 目录与身份
- 配置档:`<数据根>/telegram-web/<账号键>/`(Playwright persistent context 全量落此,0700 目录/内件 0600);账号键=用户起的全称标识(规约 telegram-<标识>,如 telegram-alt1),目录名即键,引擎按键定位;
- 浏览器二进制:复用 crawl4ai 组件轨的 playwright-browsers(PLAYWRIGHT_BROWSERS_PATH 同源注入判例),零新下载;
- 每账号键一个 Host 进程内上下文(一个 Chromium instance/context),生命周期挂 serve 宿主;并发帽 `telegram_web.max_accounts`(缺省 3)。

## D2 登录流(web-login)
- `myssia telegram web-login --account <键>`:headed 启动该键配置档 → 开 web.telegram.org → 用户输手机号+验证码(TG 发手机)→ 引擎轮询登录成功标志(左栏会话列表出现)→ 收紧窗口→CLI 退出留档;
- 已有有效登录态:提示复用;`--force` 重登(会话列表未出现视为失效);
- 桌面形态:设置页「Telegram 监控」卡 → 账号列表(每行:键+状态灯+「重新登录」+删除)+「+添加账号」(起键名→拉起登录窗);登录窗=壳拉起的系统浏览器窗口(非前端内嵌),照 MYIA_SHOW_ON_START 直跑判例家族。

## D3 读消息(DOM 监听)
- 每(账号×群)一个 Watcher:页开 `web.telegram.org/k/<群id或用户名>`?群=ChatList 点进;消息容器节点到达时 MutationObserver(polyfill 经 page.evaluate 注入)→ 新消息节点 → 解析(文本/媒体标记/发送者/时间)→ telegram_update 同形 dict → **复用 bot 线 dispatch_once 全语义**(分拣/媒体组/#tg- 锚/粗筛/LLM 精筛/合并出口);
- 群定位:用户可给群链接用户名或数字 id;引擎开页后按标题/链接校验命中,未命中=结构化失败带指引;
- 哨兵:登录态丢失(被踢/会话过期页)与 DOM 选择器失配 → 结构化告警(tg_web_logged_out / tg_web_dom_stale)不装死,组件卡对应账号行翻红。

## D4 源配置与引擎
```yaml
- name: telegram-mihomo_party_group        # 源名全称律
  engine: tg_web
  url: "https://web.telegram.org"           # 锚
  engine_options:
    tg_web:
      account: telegram-alt1                # 账号键(归属声明)
      chat: mihomo_party_group              # 群用户名或 -100 id
      lookback_limit: 50
```
- schema 词表两行 hunk(ENGINES/EngineName)+registry 注册,链外判例;凭据零(登录态在档);批量档=开页读当前窗口(排程采集用),常驻档=serve 内 Watcher(实时)。

## D5 多账号治理
- 失效隔离:单键掉线仅其 Watcher 停+告警,其他键不受累;serve 重启全量拉起各键;
- 资源:每键一 context(~150-300MB),max_accounts 帽 3 缺省,超帽结构化拒;
- 风控披露(档+卡文案):同出口多账号可关联,只读低风险,建议各键专用小号;
- 审计:每键一个 web_events 账本(照 telegram events 分键判例)。

## D6 测试(全 mock 零真网)
- 登录流:成功/复用/force/超时(mock Playwright);
- Watcher:新消息节点→update 同形→管线;媒体组/幂等锚复用断言;
- 哨兵:登出页/DOM 失配两告警;多键隔离:一键失效另一键不受累;
- 组件卡:vitest 三态+账号列表+添加流(无头冒烟禁屏控);
- 装机:外科+重签+open -g+心跳。

# wechat-bridge — 微信本机桥(UI 自动化 + 本地库只读)

受管组件(task 10-11-wechat-ui-bridge,G7 命名):管「当下收发」的 **UI 自动化桥**(macOS AX 先行,Windows wxauto 备胎另启)+ 管「历史与全量」的**本地库只读通道**。不破解协议、不碰微信进程内存,外部件走受管组件链路。

- 设计与契约:`.trellis/tasks/10-11-wechat-ui-bridge/design.md`(CLI §6 / 配置 §7 / 测试 §8)
- 组件戳:`component.json`(版本 + 适用微信版本范围,真锁惯例 design §4)
- MYIA 侧接入:push 通道 `weixin-local`(Phase F;`weixin` 通道名保持归官方 Hermes 桥 `src/myssia/push/weixin.py`,该文件是本桥调用形态的蓝本)

## 运行形态

一次性子进程,stdout 恒单个 JSON 对象,exit 三段语义(0 成功 / 1 通用失败 / 2 用法;失败段按 §6 细化码值):

```console
python -m wechat_bridge --probe                        # 三态探针(ok/degraded/bridge_unavailable)
python -m wechat_bridge sessions list --json           # 会话列表(Phase C1)
python -m wechat_bridge messages read <id> -k 50       # 最近 K 条文本(Phase C2)
python -m wechat_bridge send_text <id> --file -        # 正文经 stdin(G6 硬频控;Phase D)
python -m wechat_bridge localdb query <chat> --since 7d --json   # 本地库只读(Phase E)
```

## 落点与配置

- 组件源码(本目录)经受管链路落在 `~/.myia/plugins/wechat-bridge/`(design §1);MYIA 侧 `wechat_bridge_bin` 可覆写路径(Phase F)。
- 桥配置:`<数据根>/wechat-bridge/config.json`(全部有缺省、**缺文件可用**,design §7):`domains`(G4 三域)、`limits`(AC2 参数化)、`copy_ttl_hours`/`copy_capacity_mb`(G5)。**无频控键**(G6 硬编码:单条、间隔 ≥10s、无批量、不可配置)。
- 频控状态:`<数据根>/wechat-localdb/send_state.json`(flock 防并发,design §2)。

## 骨架态(Phase B)能力边界

- `--probe` 真实现:三态判据矩阵(design §2)照跑——进程/版本/AX 权限/主窗口/本地库落盘,全只读零前台扰动;微信托盘态如实 `degraded(window_closed)`,进程不在如实 `bridge_unavailable`。
- 四子命令:前置检查门真跑(§6 码序 fail-fast),实现层落位 Phase C/D/E,未落地时结构化应答 `not_implemented`(exit 1 过渡码,不谎报 §6 具名族);`localdb query` 可真跑到「定位 db_storage」,密钥途径待 D4 裁决,如实 `key_unavailable`(exit 21)。
- 频控落盘模块(G6)已实现并可单测(时间注入,不真等 10 秒)。

## 红线(违者返工)

1. 静默后台:不抢前台焦点、不合成鼠标点击、不激活微信窗口;UI 侧只走 AX 通道。
2. 不破解协议:禁逆向、禁 hook 注入;内存密钥搜索默认关且禁止真跑。
3. 私有数据:聊天内容/密钥材料不入 git/日志/报告;证据只留形状。
4. 依赖纪律:临时依赖一律独立 venv,勿入仓库 `.venv`。

## 测试

```console
uv run --no-sync python -m pytest tests/wechat_bridge -q      # 全 mock,CI 全绿
MYIA_WECHAT_E2E=1 uv run --no-sync python -m pytest tests/wechat_bridge -q  # 加跑真机探针(design §8)
```

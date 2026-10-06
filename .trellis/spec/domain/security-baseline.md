# 安全底线(铁律,规划 v1.7 定案)

## 凭据

- LLM key / 代理 key / 推送 token / 源 cookie 一律进系统钥匙链(macOS Keychain / Windows DPAPI)
- YAML 只许 `keychain:` / `env:` 引用;**配置文件出现明文凭据 = 启动即报错拒跑**
- 三态:`env:VAR` / `keychain:name` / CLI 首跑录入(`myia secret set`)后入钥匙链
- 钥匙串既有项更新被拒(macOS -25244 需 GUI 授权)时回落「删旧建新」重建:写前探测保留旧值、重建失败尽力回写(`set_secret`,10-03-image-fix-followups)
- 凭据**名**探测零弹窗:macOS 系统缺省路径 `list_secrets` 走 attributes-only 枚举(`security dump-keychain` 元数据,零数据读取=零授权框);注入 backend/枚举不可用回落索引+存在性核对;值读取的 ACL 授权语义不变(10-05-keychain-silent-listing)
- 推送通道凭据解析顺序=显式引用原样(`env:`/`keychain:`)→ env 缺失回退钥匙链规范名 `myia/push/<ENV_KEY>`(叶名=环境变量名;设置→推送 表单与 `resolve_channel_credential` 同口径);飞书 tenant token 优先手工 token,缺则 app_id/secret 自动 mint+进程缓存;双缺报 `env_var_missing` 指引设置→推送(10-05-push-credential-journey)
- 仓库红线(2026-10-01 grill Q8 提级):**仓库即公开,含 `.trellis/` 全部任务/PRD/research**——任何凭据、内网地址(127.0.0.1 例外)、生产语料、私有系统痕迹零容忍;任务文档自下笔起按公开标准撰写,验证记录只写「验证通过+日期」;唯一例外是标注「仅本地」的外部规划文档路径引用

## 网络

- 默认尊重 robots.txt;限速礼貌(qps/jitter/backoff)是默认行为不是选项
- 「真人验证+手机号」类源无解也不碰——结构化报错,不做绕过
- ingest/回调 API 默认关闭;开启强制 token 鉴权且仅绑本机/内网

## Plugin

- **任何 plugin 装不上,核心流水线必须照常跑通**(桌面工具的生死线)
- plugin remote 凭据入钥匙链(设置页 remote 配置面板:endpoint 落数据根 `<home>/remote-plugins.json`,明文 token 只经 `secret.set` 入钥匙串,面板与配置零明文);~~compose 文件零明文凭据~~(插件 docker 模式 2026-10-06 已全删,compose 面不复存在,条款随删归档;判例 10-06-native-plugin-components)
- **插件源码远取链完整性门**(判例 2026-10-06 10-06-plugin-src-remote-fetch):锁=内容寻址事实源(`plugins.lock.json`:url+sha256+size,载入即 pydantic 自洽校验,坏锁 `plugin_lock_invalid` 拒不静默降级);远取资产过**双门**——先 `len(payload)==size` 前置对账再 sha256 逐字符严格比对(digest 不归一化,大写/带空白变体一律拒,与锁/manifest `SHA256_HEX_RE` 口径统一);tar 解包成员白名单(相对路径/无 `..`/无反斜杠/拒符号·硬链接·设备件/唯一 `plugins/<id>/` 顶层前缀剥壳/py≥3.12 `filter="data"`+老版本手工双保险);暂存解包在 `<安装根>/.staging/<id>-<短随机>/` 成败 finally 清残零半装;sha256 校验语义参考 runtime-manifest 判例(同构:url+sha256+archive)

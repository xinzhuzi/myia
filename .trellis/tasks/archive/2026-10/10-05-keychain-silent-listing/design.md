# design:钥匙串凭据名探测零弹窗

## 现状与缺陷机制

`list_secrets()`(`src/myssia/secrets.py:345`)两步都是**数据读取**:

1. `_read_index`:读 `__index__` 条目的 JSON 数据(keyring 无枚举 API,
   名字索引存钥匙串内的设计抉择);
2. 存在性核对:对索引里每个名字 `get_password` 判活。

macOS 钥匙串 ACL 只作用于**数据读取**;attributes 查询不触发授权(当轮
实跑 `security find-generic-password` 不带 `-w`、`security dump-keychain`
均零弹窗)。条目 ACL 只含创建者二进制(.venv python)时,装机版 myssia-core
读数据 → 授权框;拒绝不记忆 → 每次开屏重弹。

## 方案定向(取舍记录)

- **D1 枚举机制= `security dump-keychain` attributes-only**:
  `security dump-keychain`(无参=默认钥匙串)输出全部条目元数据;按
  条目块(`keychain:` 行起)配对 `"svce"<blob>="myia"` / `"acct"<blob>=…`,
  命中即名。备选否决:ctypes `SecItemCopyMatching`(kSecReturnAttributes)
  零子进程但复杂度高一个量级;`security find-generic-password` 逐名探测
  仍需先有名单(索引读取照样弹)——dump 一次拿全量名单是唯一「零数据读」
  的简单路径。
- **D2 触发条件=系统缺省路径 only**:`backend is None` 且 darwin 时先试
  枚举,**成功即返回(连 get_backend() 都不调用,零 keyring 触碰)**;
  枚举返回 None(非 darwin/CLI 缺失/非零退出/OSError/超时 10s)回落
  既有路径。注入 backend(全部既有测试)永不走枚举 → 测试套零漂移。
- **D3 名单纪律**:过滤 svce==myia、剔 `__index__`、`_SECRET_NAME_RE`
  校验、`sorted(set(...))`;名字以钥匙串实况为准(天然自愈,无需索引)。
  索引的维护面(set/delete 的 `_update_index`)原样保留——非 macOS 与
  回落路径仍依赖。
- **D4 值语义不动**:`get_secret`/`set_secret`/`delete_secret`/backend
  协议零改动;真用凭据的授权框是 macOS 正确行为。
- **D5 拒绝记忆不做**:枚举路径零弹窗后探测已无授权框,拒绝记忆失去
  存在场景;回落路径的弹窗属平台限制(R3 如实接受)。

## 变更面

- `src/myssia/secrets.py`:新增 `_dump_macos_service_accounts(service)`
  (darwin 门卫+subprocess+块解析,失败 None)+ `list_secrets` 头部插
  枚举分支;模块 docstring Listing 节同步。
- `tests/test_secrets.py`:新增 describe——枚举采用(AC1)、过滤纪律
  (AC2)、回落等价(AC4);AC3=既有文件零改动。
- 装机:worktree 检出 HEAD → sidecar+tauri 构建 → 静默换装(备份在
  /tmp)→ exit 文件回执;装机版开消息屏零弹窗由主人目验终裁(AC7)。

## 风险

- dump 解析格式漂移(macOS 大版本改输出):解析失败仅回落旧路径
  (可能弹窗),不炸功能;`returncode≠0` 一律 None。
- 多钥匙串用户的非默认钥匙串条目枚举不到:罕见配置,docstring 注明,
  值读取路径仍可用(get_secret 按名直读不受影响)。
- 并行会话在途:secrets.py 无并行脏件(git status 核过),提交按 path
  白名单。

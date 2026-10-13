# 微信取钥器协议 v1(外部可执行件)

> 本文定义 MYIA 微信桥(wechat-bridge)调用**外部取钥器**(key provider)的子进程协议。
> MYIA 产品代码零取钥实现:取钥能力整体外包给用户自备的外部可执行件,桥只认协议——
> 不校验来源与签名、不内置降级。第三方凭本文即可写出合规取钥器,**无须阅读桥源码**。
>
> - 协议版本:v1
> - 必选动作:仅 `get_db_key`
> - 词汇约定:配置项/UI 文案用「取钥器」;协议名与 JSON 字段保留标准英文

## 1. 概述

- **触发时机**:桥执行本地库查询(`localdb query`)时发现密钥缓存缺失或失效,且已配置
  取钥器路径(`key_provider_path`),则按本协议 spawn 取钥器子进程取钥。
- **取钥器形态**:任意可执行文件(Python/Shell 脚本、编译二进制均可),须可直接执行
  (有可执行位;脚本须带 shebang,如 `#!/usr/bin/env python3`)。
- **职责边界**:取钥器只负责「给出密钥」;密钥验真与缓存归属桥侧(§7)。
- **无降级**:未配置取钥器或取钥失败时,桥直接报人话错误,绝不静默回退到任何内置取钥实现。
- **无来源校验**:桥不校验取钥器的签名/来源/实现方式——风险件用户自备、自行担责。
- **无状态**:取钥器可被并发拉起,应可重入、不落锁文件、不依赖桥内文件布局。

## 2. 调用模型

桥 spawn 取钥器为子进程,三条标准流各司其职:

| 流 | 方向 | 用途 |
|---|---|---|
| stdin | 桥 → 取钥器 | 承载**单行 JSON 请求**;桥写完该行后即关闭 stdin |
| stdout | 取钥器 → 桥 | **唯一协议通道**:NDJSON(每行一个 JSON 对象) |
| stderr | 取钥器 → 桥 | 调试旁路,不承载协议;仅失败场景被桥取尾部 500 字符附入错误信息(§6) |

时序:

```text
桥                                        取钥器
│  spawn(可执行文件)                       │
│── stdin:{"action":"get_db_key",...}\n ─▶│  读一行请求
│── 关闭 stdin                            │
│◀─ stdout:{"type":"progress",...}\n ─────│  progress 行,0..N 次
│◀─ stdout:{"type":"result",...}\n ───────│  result 行,恰一次(终态)
│◀─ 子进程退出(退出码)                    │
│  判定(§6)→ 逐 key 页 1 HMAC 验真(§7)     │
│  → 全量通过才落密钥缓存 → 继续查询        │
```

协议 v1 不定义工作目录、环境变量注入等额外约定——取钥器不应依赖这些,只可假定
stdin/stdout/stderr 三件套与 120 秒执行预算。

## 3. 请求(stdin,单行 JSON)

桥写入**一行** JSON(UTF-8,末尾换行),写后关闭 stdin:

```json
{"action":"get_db_key","db_path":"/abs/path/to/db_dir","account_id":"wxid_xxx"}
```

### 动作 `get_db_key` 参数表

| 字段 | 类型 | 必含 | 语义 |
|---|---|---|---|
| `action` | string | 是 | 动作名;v1 唯一动作 = `"get_db_key"` |
| `db_path` | string | 是 | 微信加密库根目录(`db_storage`)的**绝对路径**;其下各 `.db` 文件即待解密的 SQLCipher 库 |
| `account_id` | string | 是 | 当前登录账号标识(`wxid_xxx` 形态);供多账号场景选择密钥材料 |

收到未知 `action` 时,取钥器应回应 `result`(`success:false` + 人话 `error`)并以退出码 0
退出,或直接以非 0 退出码退出——两种形态桥都判失败(§6)。v1 的桥只会发送 `get_db_key`。

## 4. 响应(stdout,NDJSON)

每行一个 JSON 对象(UTF-8),写行后应 flush。两种行类型:

### progress 行(0..N 次,可选)

```json
{"type":"progress","message":"人类可读进度","level":0}
```

| 字段 | 类型 | 语义 |
|---|---|---|
| `type` | string | 固定 `"progress"` |
| `message` | string | 人类可读进度文本(面向用户展示) |
| `level` | int | 进度级别;v1 取 `0` 即可 |

progress 行纯供人读与过程展示;协议的机器语义只在 result 行。

### result 行(恰一次,终态)

**成功形态**:

```json
{"type":"result","success":true,"keys":{"<salt_hex>":"<key_hex>","<salt_hex>":"<key_hex>"},"account_id":"wxid_xxx","logs":["..."]}
```

| 字段 | 类型 | 语义 |
|---|---|---|
| `type` | string | 固定 `"result"` |
| `success` | bool | `true` |
| `keys` | object | `{salt_hex: key_hex}` 密钥映射,见 §5;成功形态必含 |
| `account_id` | string | 回显请求的 `account_id` |
| `logs` | string[] | 人话过程日志行,便于排查;可为空数组 `[]` |

**失败形态**:

```json
{"type":"result","success":false,"error":"人话错误","logs":["..."]}
```

| 字段 | 类型 | 语义 |
|---|---|---|
| `type` | string | 固定 `"result"` |
| `success` | bool | `false` |
| `error` | string | 人话错误原因(最终用户可读;桥会透传进自身错误信息) |
| `logs` | string[] | 同上 |

### 行序硬约束

- `progress` 0..N 次;`result` **恰一次**,且必须是最后一条输出。
- `result` 之后不得再输出任何行;输出多条 `result` 属协议违例(v1 未定义桥的取舍,实现必须避免)。桥侧实现注(如实披露):违例时取**首条** `result` 为终态,其后各行读空丢弃——不报错、不重试。
- stdout 不得混入任何非协议输出(调试信息一律走 stderr)。`progress` 行桥不透传不上屏,仅计入失败时的诊断计数(progress N 行)。

## 5. `keys` 映射与 `"*"` 通配

微信 4.1+ 各数据库独立加密(每库各自的 salt 与派生密钥),因此 `keys` 是映射而非单值。

- **键 = `salt_hex`**:目标库的 SQLCipher salt,即**该库文件前 16 字节**的 hex 编码(32 字符)。
  取钥器可从 `db_path` 下枚举 `.db` 文件、逐个读前 16 字节得到。
- **值 = `key_hex`**:该库的 32 字节原始 SQLCipher 密钥的 hex 编码(64 字符;桥按 hex 解码,
  大小写均可,建议统一小写)。
- **`"*"` 通配键**:单钥形态的取钥器可用 `"*": "<key_hex>"` 表达「全域同钥」——这一把密钥
  适用桥侧全部待解密库。面向单钥场景(旧版微信、或全域同钥的取钥机制);微信 4.1+ 每库
  独立密钥,应逐 salt 给钥。避免同一响应混用 `"*"` 与逐 salt 键(桥的取舍已定义:`"*"` 铺底
  在前、逐 salt 键后到覆盖;仍建议不混用,混用形态排查成本高)。
- **多给安全,但门槛是全量**:桥对返回的每个 key 逐把验真;多给的不匹配候选(盐对不上任何
  在场库、或验真不过的)会被弃用、不污染缓存——因此「多给」本身不会导致失败,**缺给才会**。
  落缓存的门槛是全量:`keys` 须覆盖全部在场库且逐把验真通过;部分覆盖或部分验真不过 =
  **整体失败**(exit 21,一把都不落缓存,§6/§7)。宁可多给候选,不要只给一把没把握的钥。

## 6. 退出码、超时与 stderr

桥侧判定矩阵:

| 取钥器终局 | 桥判定 |
|---|---|
| 输出 `result`(`success:true`),退出码 0 | 取钥成功 → 逐 key 页 1 HMAC 验真 → **全量通过才落缓存**;部分覆盖或部分验真不过 = 整体失败(exit 21,不落缓存,§7) |
| 输出 `result`(`success:false`),任意退出码 | 失败;`error` 透传进桥错误信息 |
| 未输出 `result`,退出码非 0 | 失败;stderr 尾部 500 字符附入错误信息 |
| 退出码 0 但无 `result` | 失败(「未返回结果」) |
| 120 秒内未结束 | 桥 kill 子进程,失败(超时) |

- **退出码语义**:非 0 = 失败;0 但无 result 同样 = 失败(「未返回结果」)。
- **超时**:120 秒为 spawn 起全程硬上限,与是否持续输出 progress 无关;v1 无延长协商机制。
  预计耗时的步骤应尽早输出 result 或主动失败,不要挂满 120 秒。
- **stderr**:仅失败场景被消费(取尾部 500 字符附入桥错误信息);成功时桥不读。
  stdout 才是协议通道——密钥、进度、结果只走 stdout 的协议行。
- **推荐姿势**:正常路径 = progress… → 恰一条 result → 退出码 0;未捕获异常尽量 catch 后
  发 `result`(`success:false`)再退 0;catch 不住就非 0 退出,由桥兜底判失败。

## 7. 密钥验真与缓存归属

- 桥对返回的**每个 key** 做页 1 HMAC 离线验真(SQLCipher 4 原始密钥语义,纯离线、零进程
  接触);验不过的 key 弃用,并如实计入桥侧日志与错误信息。
- **验真是全量门槛**:`keys` 须覆盖全部在场库且逐把验真通过。部分覆盖(有库没给到钥)或
  部分验真不过(任一在场库的钥验真失败)= **整体失败**(`key_unavailable`,exit 21),
  **一把都不落缓存**——不存在「部分通过落部分」。
- 只有全量验真通过的密钥才整体落桥管理的密钥缓存 `keys.json`(数据根私有区,权限 600)——
  **缓存由桥独占写,全量验真通过后才落**。
- 因此取钥器**无状态、不写 `keys.json`**、不依赖桥内任何文件布局;它每次调用都被期待
  独立给出当前有效的密钥材料。

## 8. 桥侧错误与人话文案

本表是「桥对各种情形的呈现语义」。所有取钥器侧失败最终收敛为桥既有具名错误
`key_unavailable`(exit 21,现状语义不变)——取钥器故障不会伪装成其他错误族。
除标注的法定文案外,错误措辞以桥实装为准;判定语义以本表为准。

| 情形 | 桥侧行为 | 错误信息 |
|---|---|---|
| 未配置取钥器(`key_provider_path` 为空) | 不 spawn,直接失败 | **「未配置外部取钥器,请在设置中指定可执行文件路径」**(法定文案) |
| 配置路径的文件不存在 | spawn 失败 | 人话报错,含所配路径 |
| 文件不可执行 | `key-provider set` 阶段拒绝;运行期 spawn 失败如实报 | 人话报错 |
| `result` `success:false` | 失败 | 透传取钥器 `error` 字段(人话) |
| 退出码非 0、无 `result` | 失败 | 附 stderr 尾部 500 字符 |
| 退出码 0、无 `result` | 失败 | 「取钥器未返回结果」 |
| 超过 120 秒 | kill 子进程,失败 | 超时说明(含时限) |
| 密钥部分覆盖 / 部分验真不过 | **整体失败**(exit 21) | 如实说明覆盖与验真计数(给出/覆盖/通过各多少)、未入缓存 |
| 密钥全部验真不过 | 失败 | 如实说明验真未通过、未入缓存 |

## 9. 实现者指南:写一个最小取钥器

完整流程只有四步:读 stdin 一行 → 解析请求 → (可选)输出 progress → 输出恰一条
result 后以退出码 0 退出。参考实现见
[`plugins/wechat-bridge/examples/keyprovider_ref.py`](../plugins/wechat-bridge/examples/keyprovider_ref.py)
(读密钥缓存 + 协议包装,零扫描逻辑,可直接改造成你自己的取钥器)。

最小可用示例(单钥 `"*"` 通配形态):

```python
#!/usr/bin/env python3
"""最小取钥器:从固定文件读单钥,以 "*" 通配形态应答。"""
import json
import sys

KEY_FILE = "/path/to/my/key.txt"  # 换成你的密钥来源(缓存文件/钥匙串/你的取钥机制)


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main() -> int:
    line = sys.stdin.readline()  # 桥写一行后关 stdin,不会有更多输入
    try:
        req = json.loads(line)
    except ValueError:
        emit({"type": "result", "success": False,
              "error": "请求不是合法 JSON", "logs": []})
        return 0
    if req.get("action") != "get_db_key":
        emit({"type": "result", "success": False,
              "error": f"未知动作: {req.get('action')!r}", "logs": []})
        return 0
    emit({"type": "progress", "message": "正在读取密钥…", "level": 0})
    try:
        with open(KEY_FILE, encoding="utf-8") as fh:
            key_hex = fh.read().strip()
    except OSError as exc:
        emit({"type": "result", "success": False,
              "error": f"读取密钥文件失败: {exc}", "logs": []})
        return 0
    emit({"type": "result", "success": True,
          "keys": {"*": key_hex},
          "account_id": req.get("account_id", ""),
          "logs": ["单钥通配形态"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

逐 salt 形态只需换 `keys` 的构造——枚举 `db_path` 下各库的 salt(文件前 16 字节):

```python
from pathlib import Path


def salt_keys(db_path: str, key_for_salt) -> dict[str, str]:
    """枚举 db_path 下各库 salt,组 {salt_hex: key_hex}。"""
    keys: dict[str, str] = {}
    for db in sorted(Path(db_path).rglob("*.db")):
        with db.open("rb") as fh:
            salt_hex = fh.read(16).hex()  # SQLCipher salt = 库文件前 16 字节
        keys[salt_hex] = key_for_salt(salt_hex)
    return keys
```

手动联调(不经过桥,取钥器作者的冒烟测试):

```bash
echo '{"action":"get_db_key","db_path":"/abs/path/to/db_dir","account_id":"wxid_xxx"}' | ./my_provider
```

预期:stdout 逐行输出 NDJSON(最后一条是 `result`),退出码 0。

实现清单(自查):

- [ ] stdout 只输出协议 NDJSON 行;调试信息走 stderr
- [ ] 每行一个 JSON 对象 + 换行,写后 flush(流式可被桥即时读到)
- [ ] `result` 恰一条且是最后一条输出
- [ ] 成功形态含 `keys` 并回显 `account_id`;失败形态含人话 `error`
- [ ] 逐 salt 形态时 `keys` 覆盖 `db_path` 下**全部**在场库(部分覆盖 = 整体失败,§7)
- [ ] 发完 `result` 后以退出码 0 退出
- [ ] 不写 `keys.json`、不依赖桥内文件布局;可并发重入
- [ ] 全程 ≤ 120 秒
- [ ] 不等待 stdin 后续输入(桥已关闭 stdin)
- [ ] 输出编码 UTF-8

## 10. 配置挂点

取钥器的配置面(用户/集成者视角):

| 面 | 说明 |
|---|---|
| 桥配置 | `config.json` 键 `key_provider_path`(缺省空 = 现状行为:不 spawn、不取钥) |
| 桥管理命令 | `wechat-bridge localdb key-provider set <path>` / `get` / `clear`;`set` 校验文件存在且可执行 |
| 设置页 | 微信/桥分区「取钥器」行:路径输入 + 三态(已配/未配/文件缺失);未配置态引导文案指向本文档 |
| MYIA 引擎 | 零改动:取钥闭环在桥内,失败语义即既有 `key_unavailable`(exit 21) |

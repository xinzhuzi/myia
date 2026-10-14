# 微信库密钥钥匙串化与取钥路径归拢

## Goal

方案1:keys.json 整体入 macOS 钥匙串(桥读 keychain 优先文件兜底+CLI migrate 命令原子迁移);取钥蓝本工作路径经包装层 HOME 钉归拢数据根(不改上游蓝本,链接者铁律);重取产物 passphrase 由包装搬钥匙串后清明文

## Requirements

- R1 桥读取两级化:`resolve_keys` 以 macOS 钥匙串条目 `myia/wechat/db-keys`(值=完整 keys.json 的 JSON 外壳 `{migrated_at, keys}`)为首选源、文件 keys.json 兜底(兼容),两者都无=现既有空态;验真门(HMAC 全量)对两源同判。
- R2 桥内最小钥匙串通道(零新 pip 依赖、不 import myssia):`security find/add/delete-generic-password` 子进程;条目与既有 `myia/*` 命名族同位(service=`myia` + account=`myia/<scope>/<name>`);token 零外显(读=find -w stdout 管道;写=`security -i` 内联命令行经 stdin 管道——裸 -w 提示形态管道 stdin 128B 截断、-i 解析器不认非 ASCII,均 2026-10-14 本机实测,故值钉 ASCII/无换行)。
- R3 acquired_at 语义不谎:钥匙串条目无 mtime,取外壳 `migrated_at`(写入即刷新);文件源仍文件 mtime;`key-status` 增 `source` 字段(keychain|file|None)且源选择镜像 resolve 消费序(首个抽样通过源=如实态)。
- R4 CLI 命令族:`localdb keys-migrate`(读文件→HMAC 重验→写钥匙串→回读逐字节一致→文件改名 `keys.json.migrated-<ts>` 保留,断电安全不删→人话回执;回读不一致回滚旧值)与 `localdb keys-unmigrate`(钥匙串→文件 600,回读一致才删条目;回退用)。
- R5 取钥路径归拢(只动 MYIA 包装,上游蓝本零改动):keyprovider_wrap.py 把 root 段 HOME 钉 `<数据根>/wechat-localdb/work/`(700,项目自己的辖区,蓝本 ~/.wcdb-key-tool 落此);root 段 chown 归还照旧(引用 $HOME 即 work);passphrase 跑前从钥匙串条目 `myia/wechat/passphrase` 复水进 work(蓝本第2级缓存命中,重试链不断)、跑后(finally,成败/取消都跑)搬回钥匙串后删 work 明文;搬失败保留明文(可用性优先)+形状级 stderr 注记。
- R6 探针两源化:`localdb_key_available` 兼看文件与钥匙串条目(迁移后明文件改名不在场,单看文件会系统性谎报 missing;条目读取不做 HMAC,验真门仍在消费侧)。
- R7 write_key_cache 迁移态分流:条目在场时重取的新钥刷新钥匙串(外壳时间随写刷新)、明文件不重建(主人令:密钥本地保存应加密,轮换后明文不回流);钥匙串写失败/euid==0 回落明文件(可用性;判例同 _restore_owner_for_sudo)。
- R8 红线:密钥值/passphrase 零回显到日志/回执/argv(掩码或只报计数);生产迁移原子性(先写钥匙串验证成功才动文件,任何一步失败保持原状);wcdb_key_tool_macos.py 与 keyscanner 零改动。

## Acceptance Criteria

- [x] AC1 R1/R2:桥新增 `wechat_bridge/keychain.py`(条目/外壳/读写/删)+ `resolve_keys` 两级 + `read_db_keys_from_keychain`;三态(钥匙串有/仅文件/都无)单测全绿(代码锚:`plugins/wechat-bridge/wechat_bridge/keychain.py`、`localdb.py:resolve_keys`)
- [x] AC2 R3:`key_status` 增 `source` 字段,钥匙串源 acquired_at=外壳 migrated_at;既有测试同步更新,全绿(`localdb.py:key_status`)
- [x] AC3 R4:`localdb keys-migrate`/`keys-unmigrate` 落地(验真门+回读逐字节+改名保留+回滚+回退;`localdb.py:keys_migrate/keys_unmigrate` + `cli.py` 注册/分支)
- [x] AC4 R5:数据根 bin/ 三 MYIA 件更新(wrap:HOME 钉 work/+复水/清扫;root sh:注释随 WXKEY_HOME 语义更新;上游蓝本与 keyscanner 零改动——`git status` 无其改动);wrap 复水/清扫真钥匙串功能验证通过(测试值,验后即删)
- [x] AC5 R6/R7:探针两源化(`system_checks.py:localdb_key_available`)+ write_key_cache 迁移态分流(`localdb.py:write_key_cache/_write_key_cache_file`),单测覆盖
- [x] AC6 测试门禁:`uv run --no-sync pytest tests/wechat-bridge tests/desktop -q` = **1257 passed, 12 skipped**(新增 `tests/wechat-bridge/test_localdb_keys_keychain.py` 33 用例:三态/往返/回退/验真门/回滚/明文不回流/security argv-stdin 纪律/ASCII 外壳);`ruff check` 全过
- [x] AC7 生产热修:改动桥 4 件(keychain/localdb/cli/system_checks)cp 进装机 bundle `/Applications/世事.app/Contents/Resources/components/wechat-bridge/wechat_bridge/`,`diff -rq` 全同步;数据根 bin/ 直接更新
- [x] AC8 生产迁移真跑:`localdb keys-migrate` exit 0,回执 `{db_count:20, migrated_at:"2026-10-14T21:16:26+08:00", keychain_account:"myia/wechat/db-keys", file_renamed:"keys.json.migrated-20261014-211626", verified:true}`;明文件改名保留(600)
- [x] AC9 解密链活性:`localdb key-status` = ready/20/源 keychain/抽样 3 库验真通过;`sessions list -n 3` exit 0 返回 3 会话(钥匙串钥→HMAC→E2 副本→查询全链);装机 bundle 自身 launcher `key-status` 同报 ready/20/keychain;`--probe` state=ok 且 localdb_key=ok
- [x] AC10 回执纪律:密钥值/passphrase 零回显(本 prd 只记计数/时间戳/条目名);首次生产迁移踩中 128B 截断 → 回滚生效(条目删、文件未动)→ 修正写形态后重迁成功——原子性经生产实跑验证

## Notes

- 首次生产迁移失败回放(有价值的安全实证):裸 `-w` 双行 stdin 形态对长值 **128 字节截断**(500/1000/2000/4000B 实测全落 128B),回读逐字节验证门当场拦截,回滚恢复原状(条目删、keys.json 未动)——验真门与原子性纪律在生产路径真实生效。
- `security -i` 内联形态约束(实测):认 JSON 式引号/反斜杠转义;不认 U 转义序列与裸多字节 UTF-8(mojibake)→ 外壳 `ensure_ascii=True` 钉死 ASCII 面(非 ASCII 库名 JSON 层转义,parse 无损)。
- 钥匙串条目与 myssia 命名族同位(service=myia),`myssia secret list` 的 dump 枚举天然可见 `myia/wechat/db-keys`(Keychain Access 同组)。
- 未做版本号 bump(判例:cp 热修免重打包;__version__ 0.8.4 维持,下轮发版随组件戳走)。
- 未跑生产 keys-unmigrate(单测已覆盖往返;回退通道在位,需要时一步可退)。
- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

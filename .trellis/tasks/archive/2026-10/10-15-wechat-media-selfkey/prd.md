# 微信媒体解密自供钥件内自理通道

## Goal

主人裁决(10-15):自供钥走件内自理。现状:env/--key-file 仅手动联调形态(桥 spawn 链 argv 恒空收不到,件头已注);本次落地件内固定路径取钥——钥匙串 myia/wechat/media-keys + 数据根 wechat-bridge/media-keys.json 双通道,MYIA 零落盘纪律照守;另收编漏提交的 tests/scripts/test_wechat_bridge_mediadecrypt.py(26 测,176c7d82 只进了脚本本体)

## Requirements

- TBD

## Acceptance Criteria

- [x] AC1 件内自理双通道落地:钥匙串 myia/wechat/media-keys + 数据根 wechat-bridge/media-keys.json,load_keys 三序合并(手动显式覆盖);WX_MEDIA_SKIP_COMPONENT 调试旁路(提交 5bb039c1)
- [x] AC2 测试 33 绿(26 旧+7 新,含漏提文件收编);零命中/坏 JSON 静默降级、值零回显面全测
- [x] AC3 文档:件头供钥命令(短载荷内联避 -w 截断坑)+docs §2/§4 具体通道+V2 缺钥人话报错带三通道

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

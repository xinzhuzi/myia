# 镜像说明

- 源:`~/Downloads/微信反编译/sendmsg-勘察-1014/tools/`(cap.py v2.1 / tools README v2.1,Phase 0 门 1 绿,干跑 23/23);`ghidra-scripts/` 源=`~/Downloads/rea-wechat-decompile/ghidra_scripts/`(DecompileTargets 系+DisableSlowAnalyzers+QuerySendPath)+ `.agents/skills/ghidra-headless/.../Export*.java/SendMsgHunt.java`(注:.agents 为 git 追踪正本但 10-14 新增件未提交;`.zcode/skills/*` 是其符号链接运行位 gitignore——本镜像=git 内 13 件全量正本)
- 镜像时点:2026-10-14 晚;目的:工具随 git 永生,使 Downloads 产物目录在原则上可弃(总账见 `.trellis/spec/guides/wechat-reverse-playbook.md`)
- **Downloads 侧 tools/ 仍是唯一演进源**(并行会话在途);本镜像落后时以源为准整体重镜像,勿在此双向编辑;`__pycache__`/dryrun 产物不镜像

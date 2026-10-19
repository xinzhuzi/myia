# 运行日志升级标题级——采集条目标题进 run 日志

## 背景(主人令 2026-10-19「按照你的建议做完」)

主人在运行历史详情页(run #6403,weixin-notify)提出:「这个日志还是不知道获取了什么东西呀,为啥?没有详细写入吗?」

排查结论(当日对话已核实):

1. 该轮真实零采集(events=0 items=0 全链),不是漏写;
2. 更根本的:采集日志是**形状级契约**——`src/myssia/wechat/notify.py:532` 等 9 处明写「(形状级,不记内容)」,只记计数不记内容;所有引擎(TG 系同款)如此;
3. 「取到了什么」现行答案位=运行详情页「采集成果」区(标题预览,仅新入库条目)+ 信息流屏;**取到但未入库(全旧/被滤)的条目在任何日志里都无迹可查**。

上一轮建议:「把形状级契约升级成标题级,可以做——要做的话说一声,我立个 Trellis 任务再动手」。主人令「按照你的建议做完」即授权本任务。

## 决议(设计方向,实施时按仓库惯例细化)

- **改动点**:`src/myssia/pipeline.py:1908` 采集完成日志处(每源收口,pipeline 级单一咽喉,覆盖全部引擎——wechat notify/sns/localdb、telegram、tg_web、RSS 全系),不在 9 处引擎级形状级日志逐个改;
- **形态**:该源 items>0 时追加一行标题级日志,形如 `采集条目标题 source=%s items=%s(标题级,前K条):1.xxx 2.xxx …`;K 上限(约 10)+ 单标题截断(约 60 字)+ 折叠空白,防 64KB 行帽;零条目不加行(零噪音);
- **边界**:只记标题,不记正文/URL——隐私与日志体积的折中,与「永不标题指纹」(dedup 禁 title 键,schema.py:1022)无冲突(日志≠去重键);
- **配套**:`.trellis/spec/python/logging.md` 增「标题级采集日志」节记录契约变更与理由;测试用 caplog 断言(有 items 出标题行、零 items 无此行);
- **文案**:遵守 UI/日志文案判例——人话,无行话。

## 验收(AC)

- [x] AC1 pipeline.py 标题级日志落地:多源各自成行、前 K 条、单条截断、零条目无行
- [x] AC2 pytest 新增用例绿(有/零/截断/多源四形态),全量测试不新增红(并行树既有红须归因豁免并留证)
- [x] AC3 ruff(锁 0.16.10)对改动 py 零告警
- [x] AC4 `.trellis/spec/python/logging.md` 契约节落地
- [x] AC5 窄路径提交(git add 仅本任务文件;gitnexus detect-changes 过并留档),中文规约提交信息
- [x] AC6 `just build-desktop` 出装机件,包内 `myssia-src/myssia/pipeline.py` 字节级含新日志标记
- [x] AC7 换装(备份旧 .app→替换→清 WKWebView 缓存→open -g 复原)+ 装机实证:沙箱 MYIA_HOME 真跑一轮有采集的品类,数据根日志见标题行
- [x] AC8 任务档三件套齐(task.json/prd.md/context),收官转 review

## 边界与纪律

- 不动 9 处引擎级形状级日志本身(它们答「窗口形状」,新行答「取到了什么」,分工不同);
- 不改 UI(运行详情页日志区原样渲染新行);
- 共享树提交纪律:绝不 `git add -A`,绝不碰并行会话脏文件;
- 装机数据根真实库不用于验证(沙箱 MYIA_HOME)。

## 实录(2026-10-19 收官)

- 提交 99260e228d(7 文件:pipeline.py+37 / tests/pipeline/test_pipeline.py+118 / logging.md+8 / 任务档四件);detect-changes:5 files 6 symbols,0 processes,risk=low。
- 门禁:全量 pytest 6532 passed / 2 failed(基线即 2,零新增,系并行树既有红);ruff 0.16.10 过;换眼复查 3 条 low 全非阻塞。
- 打包:tauri build exit=0,产物 target/release/bundle/macos/世事.app(0.0.6);包内 pipeline.py:1948 字节级含「采集条目标题」。(工作流脚本 glob 不匹配目录致误报"未找到产物",主会话人工核正——glob 只回收文件,.app 是目录。)
- 换装:旧包备份 /Applications/世事.app.old-20261019-093837;ditto 替换;com.myssia.app 与 myssia-desktop 两组 WKWebView 缓存全清;open -g 复跑(pid 39028+sidecar)。
- 装机实证(AC7):沙箱 MYIA_HOME=/tmp/myia-runlog-verify 用装机件 myssia-src 真跑 stocks(yahoo-chart,5 条),沙箱日志见「采集条目标题 source=yahoo-chart items=5 titles=1.NVIDIA Corporation 2.Apple Inc. 3.Tesla, Inc. 4.Tencent Holdings Limited 5.Kweichow Moutai Co., Ltd.」。
- 副作用如实记:沙箱轮因 stocks.yaml 自带 feishu 推送多发一张 digest 卡(与日常 cron 同内容);今后沙箱验证带推送的品类须先剥推送配置。
- 复查 3 条 low 处置:①spec「两个数量级」措辞偏乐观(实测最坏 2534B,25.9 倍,仍安全)——留档不改;②测试 docstring 引 AC6 包内验证(验证在工作流/主会话非仓内测试)——如实,不改;③spec「9 处」计数复核:grep 形状级 src/myssia 恰 9 处(wechat/notify.py 4 + wechat/engine.py 5),准确,不改。
- 未推 origin(推送为显式动作,留主人)。

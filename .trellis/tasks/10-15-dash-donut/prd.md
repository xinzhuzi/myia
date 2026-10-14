# 仪表盘概览条紧凑化(recharts 四色环)

## 背景

主人令(10-15,带截图):「这个站位过于大了,可以做成饼状图,使用相关的插件去做,不要自己造 [$find-skills] 一定要查GitHub,根据代码」——截图为仪表盘概览条:四张 1/4 屏宽等宽大卡(今日采集/活跃源/推送成功/告警)。

## 方案(find-skills 核验)

- **库选型 recharts**:27,627★ / MIT / 当日活跃(gh api 实核);Chart.js(67k★ MIT)canvas 系与 Tailwind token 割裂落选。「用插件不自己造」判例覆盖旧 sparkline 自绘决议的**图表域**(趋势折线仍自绘不动)。
- **形态**:四张 1/4 宽大卡 → 单卡紧凑行(divide-x):活跃源 = 56px 四色环(recharts PieChart 定尺寸,innerRadius 18/outer 27/paddingAngle 2,动画关)+ 环心「32/48」;其余三格行内数字块(text-xl tnum,降自 text-2xl)。
- **环图四段 = 源健康度** ok/退化/失效/未知(与源健康度卡同源数据 sourceCards 聚合,占比恒一致);段色 SVG fill 直取 :root token(--ok/--warning/--dead/--unknown),色彩单源。
- **契约保真**:四 testid、注记词面、alert 明文/meta ⓘ 说明钮(HintButton)全部原样(测试钉死);doctor 不可达时环图缺席走「—」旧形态。

## 验收

- [x] AC1 dashboard 75/75 + 全量 vitest 949/949 + tsc 过(零断言改动——75 个既有用例原样通过)。
- [x] AC2 recharts ^3.10.1 入 package.json(MIT)。
- [ ] AC3 装机像素终验:随在途扫尾工作流的打包覆盖安装段捎带(同树构建);主人屏上一眼。

## 非目标

- 趋势折线 sparkline 不动(自绘既有形态);告警清单/品类区零涉。

# grill 定案(2026-10-19;依据=VL 两轮独立评审+原四条概括+代码实锚三源交叉)

## 重建 finding 与原概括映射

| 原概括 | 重建 finding | 定案 |
|---|---|---|
| 卡片下半留白 | F1 平台总览左栏下半大空白(平台网格 3-4 行后空到卡底) | **修:详情面板限高** |
| l2 垂直失衡 | F1 同源(左栏 ~400px vs 右栏详情 ~700px,items-start 双栏高度差悬殊) | 同上(右栏 max-h 后整体收短,失衡量消) |
| 图标三种风格 | F2 brand 品牌色/monogram/generic 灰混用+TG 状态灯 | **豁免**:platform-icons.tsx 头注释明言三态体系照 Hermes 蓝本(「品牌色与状态色两套语言互不混用,与上游一致」);状态三色(绿/黄/灰)是功能性语义。统一化反而背离蓝本(模仿优先铁律) |
| 绿色提示句悬浮 | F3 TG 卡回执 note 段:①actionError/note 双空时仍渲染空容器 div(p-4)→ 上方留白;②note 无视觉锚孤立卡尾 | **修:空段零渲染 + note 加 border-l ok 色视觉锚** |
| (附加) | F4 顶部说明句/CardDescription 悬浮 | **豁免**:Card/CardDescription 是全 app 统一卡片规范(shadcn 系),改一则背全规范 |
| (附加) | F5 详情面板底部留白+f-03 指南行对齐/行距 | F5 随 F1 同治;f-03 **豁免**(键名行 vs 有序列表缩进差=列表语义本身,gap-1 在 2xs 字号密度合理,避免过度整形) |

## 修法拷问记录

- F1 反方质询「限高滚动治标,真问题是左栏内容少」→ 应辩:平台卡数量=产品事实(实装+波次排期),不可为填充造卡;右栏限高是对内容长度的正确布局响应;Kestra 类控制台右栏限高滚动为常见形态;窄屏(<lg)折叠上下布局不受影响。通过。
- F3 反方质询「空段零渲染会不会破坏测试断言」→ 应辩:测试断言的是 note 文本出现与 data-testid,不是空容器存在;note 出现时容器照常渲染。通过。
- 回滚:两处均为 className/条件渲染级改动,单文件单点,git revert 即回。

## 实施点

1. platform-overview.tsx platform-detail 容器:`max-h-[36rem] overflow-y-auto`(全局细滚动条 index.css:345 已在,自动生效)
2. telegram-card.tsx 回执尾段:`{actionError || note ? <div/> : null}` + note 加 `border-l-2 border-ok/50 pl-2.5`

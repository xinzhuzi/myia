# 采集日志 run 瀑布流行高塌缩修复

## Goal

日志屏 50 轮行数超视口时,run 组行被 flex 均匀压扁成 ~6.5px 细条、内容被 overflow-hidden 裁没、滚动条永不出现;补 shrink-0 根治并以无头 Chromium 布局哨兵冒烟固证。

## 背景(实机报障,10-11)

主人报「采集日志界面表现好像有问题」,截图(1685×1057 逻辑分辨率)显示:
运行历史 50 轮的列表区整片变成 ~40 条细黑条,行内内容(#id/品类/时间/
耗时/状态芯片)全部不可见,无滚动条。顶栏过滤条/节头/状态分布条渲染正常。

## 根因(已实证)

`logs-screen.tsx` 的 run 瀑布流容器(10-04-ui-kestra-anchor e17a046 引入
「列表内滚」)是 `flex min-h-0 flex-1 flex-col gap-grid overflow-y-auto`;
子行(run 组)是 `overflow-hidden rounded-lg border` 的普通块。

flex 列子项默认 `flex-shrink:1`;而 **`overflow-hidden` 使 flex 子项的
自动最小尺寸(content-based minimum size)归零**(CSS flexbox 规范:该
保护仅适用于 `overflow: visible` 的子项)。于是当 50 行总高超过容器高:
- 每行被 flex 均匀压扁(实测 44px → **6.5px**,无头 Chromium 复现);
- 行内容被自身 `overflow-hidden` 裁没 → 黑条;
- 容器 `scrollHeight == clientHeight`,滚动条永不出现。

三个条件缺一不塌:同款 flex+内滚容器里,file-list 的 `<li>`、feed 时间线
wrapper、test-result-dialog 的 section 均为 `overflow: visible`,受自动
最小尺寸保护,不会塌——修复面收敛在日志屏 run 组行这一处。

## Requirements

1. run 组行容器补 `shrink-0`(塌缩根治;展开体随行自然撑高,容器恢复
   溢出滚动)。
2. 布局哨兵冒烟固证:`desktop/scripts/logs-screen-smoke.py`(无头
   Chromium + 50 轮历史行夹具),断言组行高 ≥40px、容器溢出可滚;先以
   当前构建复现(FAIL:6.5px),修后必须全绿。

## Acceptance Criteria

- [ ] AC1 冒烟:`.venv/bin/python desktop/scripts/logs-screen-smoke.py` 退出码 0
  (50 组行直出 / 行高 ≥40px / scrollHeight > clientHeight / 首组展开)。
- [ ] AC2 组件回归:`npm --prefix desktop/ui-src run test` 零新红(logs 屏
  既有测试不回退;jsdom 无真实布局,布局断言由 AC1 冒烟承担)。
- [ ] AC3 装机件:tauri build 重打包并静默换装;`desktop/ui` 构建产物与装机
  件同链,冒烟截图(`/tmp/myssia-logs-screen-smoke.png`)为像素证据。

## 边界

- 不动数据面(api.ts/协议零改动)、不动其他屏幕(排查过无同款暴露面)。
- 冒烟脚本入册 `desktop/scripts/`(与 feed-card-smoke 同族,可复跑)。

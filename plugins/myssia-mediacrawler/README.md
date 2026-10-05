# myssia-mediacrawler — 多平台内容采集(MediaCrawler)⚠️ 警示型文档桩

> **⚠️ 非商业学习许可:上游 MediaCrawler 采用 NON-COMMERCIAL LEARNING
> LICENSE 1.1(自定义许可,gh api LICENSE 原文核 2026-10-05)——非 OSI
> 开源,禁止商业使用。** 使用前你必须自行阅读上游 LICENSE 原文并确认你的
> 用途合规;法律边界由你自负。

官方场景件(desktop 分级,**最薄 = 警示型文档桩**):上游
[MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 是小红书/快手/
B站/微博/贴吧的多平台内容采集工具(2026-10 仍活跃)。**MYIA 不调用、不
集成、不捆绑**——本目录只有 manifest 与本 README(市场知识面:收录 =
知道它存在 + 知道边界),零 adapter、零 compose、零 CLI、零 lane 接线,
不声明 gate(无程序面即无开关可执法)。

## 桌面路径(用户自行部署)

无 remote endpoint、无服务形态、无 MYIA 程序面。要用它,自行 clone 上游
并按其 README 部署(登录态/风控/频控全在上游侧,授权与合规边界由你自负):

```
git clone https://github.com/NanmiCoder/MediaCrawler
```

## 为什么是警示桩(不是 adapter)

1. **许可**:非商业学习许可 1.1,MYIA 做成程序面(自动调用/捆绑分发)
   会让仓库使用场景越权;收录为知识面 + 醒目警示是许可纪律下的最薄形态;
2. **零复制**:上游任何代码不进本仓库(manifest 只声明存在与来源);
3. **同场景已有正规通道**:平台采集需求走官方件 myssia-douyin(remote
   桩)+ 品类 YAML 的 direct_api/static_html 源,不依赖本件。

## 边界声明

- 你对上游的使用(采集目标授权、登录态、频控、商用与否)完全由你自负;
- MYIA 不对本件的任何上游使用行为提供支持或担保;
- 上游许可条款变化以 LICENSE 原文为准,本 README 快照日期 2026-10-05。

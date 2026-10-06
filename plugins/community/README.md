# plugins/community/ — 社区插件发行目录

本目录收纳**社区场景件的发行文件**(manifest + 文档 [+ 适配器] 的插件包),
核心仓库只托管这些声明性文件,**不托管插件实现** —— 重依赖与代码全部留在
作者自己的仓库(与官方六件 `plugins/myssia-*/` 同一套市场规范,manifest 校验
见 `src/myssia/plugins/manifest.py`)。

v1.1 起插件层桌面优先:**源码/进程内能力优先,零 docker**;插件不提供
docker 模式(终裁 2026-10-06)——MYIA 仓库不携带任何插件部署配方,
上游服务的部署按上游官方文档操作,部署好的任意实例按 remote 接入。

## 铁律(与全市场一致)

**任何 plugin 装不上、配置坏、remote 不可达,核心流水线照常跑通。**
插件问题只降级为结构化 warning finding(`myssia doctor --json` /
`myssia plugin list --json` 可见),绝不拦 run。

## 收录规范

1. **一个插件一个目录**,目录名 == `plugin.yaml` 的 `id`;根下必备:
   - `plugin.yaml`(manifest,过 `myssia plugin install` 的 fail-fast 校验);
   - `README.md`(桌面路径优先:源码/进程内或 remote(endpoint+token);
     server-only 分级须写明移出桌面默认集的原因与接入方式);
   - `adapter.py`(可选,MYIA 侧适配器:进程内 import 或子进程调用上游;
     与 manifest `adapter:` 节配套,规范见 manifest.py)。
2. **分级**:`tier` 声明插件分级(缺省 `desktop` 桌面默认集);
   `remote` = 桌面可选(需自备已部署实例);`server-only` = 桌面默认集
   移出(仅服务端可选部署)。`myssia plugin list` 按 tier 展示。
3. **命名**:社区插件不得占用官方保留前缀 `myssia-`;惯例
   `<作者/组织>-<用途>`(如 `acme-price-tracker`)。id 规则:小写字母/数字/
   连字符/下划线,字母数字开头,2-64 字符。
4. **凭据红线**(仓库即公开):
   - token/cookie/口令零明文,manifest 里只允许
     `keychain:myia/<scope>/<name>` 引用;
   - endpoint/地址一律用占位域(`example.com`);内网地址零容忍
     (127.0.0.1 作为回环端点示例除外);
   - 生产语料、私有系统痕迹零入库。
5. **许可**:上游项目按其 license 以「声明依赖 + 文档引用(源码型另加
   git submodule 指针)」接入;GPL/AGPL 类上游**不复制其源码进本仓库**;
   插件一律不携带 docker 部署文件(部署配方归上游官方文档,我方不复刻,
   收录 PR 里也不放部署配方),插件目录内不出现任何 docker 部署内容。
6. **版本矩阵**:`compatible` 声明兼容的 myssia 版本范围(如 `">=0.0.1,<0.1"`,
   与根 pyproject 依赖窗同款);不兼容在 install 期结构化拒绝,已装的降级为 warning。

## 索引

| 插件 id | 一句话 | tier | 许可 | 上游 |
| ------- | ------ | ---- | ---- | ---- |
| (暂无收录) | | | | |

收录流程:提交 PR,把插件目录放进本目录并在上表加一行;维护者按上述
规范核验 manifest 与红线后合并。

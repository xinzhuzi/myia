# 装机包 YAML 编辑器空白:CSP 拦截 CodeMirror 运行时样式

## 现象(主人 2026-10-05 22:29 截图报障)

源管理屏行「编辑」弹窗 / 配置编辑屏打开任意品类 YAML:行号逐行渲染、正文一字不见、无滚动条、无报错;磁盘文件完好(169 行 8.6KB),sidecar `yaml.read` 应答逐字节完整。

## 根因(像素+DOM 探针双证)

tauri.conf.json 生产 CSP(v1.1 40a666a 10-02 23:15 一次性引入,`csp: null` → 严格版,此后未动):

```
style-src 'self'   ← 无 'unsafe-inline'
```

CodeMirror 6 的全部编辑器样式(基础布局+oneDark 语法配色+前景色)是**运行时注入的内联 `<style>` 元素**(StyleModule 机制),被 `style-src-elem` 拦截。内嵌装机态探针实证(外探针 js/css 烘进 bundle 亲测):

- `securitypolicyviolation` 事件实锤:`style-src-elem~inline`
- 文档 `<style>` 元素仅 1 个(vite 外链包),CM 注入样式为零
- `.cm-content` white-space=normal(CM 基础样式缺失)、行色=纯白继承、行内文字仍在 DOM(len=73)但样式链塌陷后不可见
- 无滚动条/行号可见=外层 tailwind 类(外部 CSS,CSP 放行)与内联样式(被拦)各管一半的撕裂形态

**为什么一直没发现**:dev/无头冒烟全部走 vite http(devUrl 模式无 CSP)→ 永远正常;装机件此前从未对编辑器做过像素验证(编辑器 10-03 落地,装机包自落地起即坏,今天主人首次真实使用撞上)。

## 修复

`style-src 'self' 'unsafe-inline'`(script-src 保持 `'self'` 锁死不动;CodeMirror 6 + Tauri 的标准放行面,桌面本地应用风险面可接受)。

## AC

- [x] AC1 装机包(生产 CSP 态)打开 ai-news.yaml:正文+注释+语法配色可见(沙箱 bundle 与生产数据根装机件双验,像素>9.8 万+VL 逐行读回 `id: ai-news`/`name: AI资讯`/`schedule` 与磁盘行号一致)
- [x] AC2 修复前后同机同流程复现对照:修复前 bundle 3/3 空白、修复后 98050 亮像素
- [x] AC3 换装判例全流程:退旧实例→删旧包→ditto 新包(hash 核对 f59b1b49)→清 WKWebView 缓存→重启生产实例验证
- [x] AC4 根因证据入档(evidence/ 含主人原截图、探针 CSP 违规横幅、装机验证截图)

## 诊断方法学(可复用)

1. 排除链:磁盘文件→Python sidecar(手跑 serve 复核)→Rust 壳分帧(app stderr 无非 JSON 行)→前端(Chromium dev/prod 均正常)→**WKWebView 装机态**(空白)
2. 决定性分离:Safari(同 WebKit 引擎)正常 ⇒ 非引擎问题;devUrl/dev 一切正常 ⇒ 内嵌态特有
3. 探针烘进内嵌包(外链 js+css 绕开 script-src/style-src 对探针自身拦截;内联探针会被 CSP 吞)
4. 坑:裸 `cargo build --release` 产物=devUrl 模式(连 5173),**不代表装机行为**;装机验证必须 `cargo tauri build` 产物
5. 坑:cargo 指纹可漏判 ui/ 单文件改动,重嵌前 touch src-tauri/src/main.rs 强制

## 归档会话注记(2026-10-06,「余量全清」收口段)

- AC1-4 全勾在档(装机包双验 98050 亮像素/前后对照/换装判例全流程/
  根因证据入档);提交 6f60904+装机换装 f59b1b49 判例链完整。
- 统一批门禁亲跑绿(pytest 4461/40/0+vitest 523 等)+CI 绿(run
  37352272165,success,headSha ff3e4a9)复核;无留主人项。

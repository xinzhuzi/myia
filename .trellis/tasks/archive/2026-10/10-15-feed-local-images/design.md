# 安全预览设计

缩略图沿用微信媒体组件的同屏展开模式与现有 tokens；每图保留路径、加载状态与失败文案，原尺寸通过可滚动区域查看。按钮原生可聚焦、aria-expanded，图像有 alt。FeedCard 展开区与 FeedItemDetail 共用独立组件。

路径不能由前端猜数据根：新增仅用于此目的的 Rust 命令 `feed_image_path(path)`，从现有 data_root 解析当前根（含 MYIA_HOME），canonicalize 后仅允许真实 images 子目录内的 png/jpg/jpeg/gif/webp 常规文件。拒绝根目录本身被符号链接到外部、文件软链逃逸、相对路径、父目录段及非图片后缀。校验成功后 asset_protocol_scope.allow_file 只授权该规范化文件，再返回给前端 convertFileSrc；不新增任意读文件 IPC，也不新增 sidecar 方法。

静态 tauri.conf scope 保持原微信媒体规则；动态逐文件授权比跨平台硬编码 $APPDATA/MYIA 更窄，亦支持用户自定义数据根。CSP 加入 Tauri Windows 资产 origin http://asset.localhost，其他策略保持原值。

参考本仓 wechat-media.tsx 与已安装 tauri 2.12.1 的 scope/fs.rs allow_file（escaped_pattern，防路径中的 glob 字符扩大权限）；资产处理先 canonicalize 再核对 scope。无新依赖。

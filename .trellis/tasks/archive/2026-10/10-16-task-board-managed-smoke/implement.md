# 实施与检查

1. 看板隔离测试先覆盖筛选、十列、逃逸、坏 JSON、层级与循环容错；再实现只读工具。
2. 定点核验统计池元数据，明确标记排除原因；运行真实看板并检查计数。
3. 读取现有 package_smoke 与 Rust managed runtime 解析；查清解释器/manifest/入口实际形状后实现隔离验收。
4. 隔离验证安装件 RPC、缺失运行时与超时路径；不执行旧 GUI preflight。
5. Python 定向 pytest + 静态检查，保存真实输出与未覆盖项；仅置 review，不归档、不执行 Git。

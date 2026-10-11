"""数据根配置目录命名与一次性迁移(config/ 布局,2026-10-11)。

品类/账号/凭据 YAML 是**配置**,不是插件 —— 数据根目录从 ``plugins/``
更名为 ``config/``(同批:仓库种子目录与随包资源目录同步拆分;真插件
安装根 ``plugins/`` 名实相符,保持不变)。本模块承载:

- 目录名常量(新名 ``config`` / 旧名 ``plugins``,唯一事实源);
- :func:`migrate_legacy_plugins_dir` —— 旧数据根的一次性无损迁移:
  平铺配置文件整体搬入 ``config/``(绝不覆盖)、cron jobs.json 里指向
  旧目录的 category 路径原位改写、搬空后的旧目录移除。可重入(幂等),
  任何失败只记日志不上抛 —— 迁移是增强,不是依赖(与首跑补种同哲学)。

宿主接线点:sidecar ``serve`` 启动序列(entry.py)与 CLI ``cron serve``
(home 模式常驻宿主)各调一次;dev 形态(home=None)零动作。
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

#: 数据根配置目录名(品类/账号/凭据 YAML;home 模式 = ``<home>/config``)。
CONFIG_DIR_NAME = "config"

#: 旧布局的配置目录名(2026-10-11 前;与市场插件安装根同名混用即改名动机)。
LEGACY_CONFIG_DIR_NAME = "plugins"

#: cron 账本文件名(jobs.py 同款;路径改写只认这份文件)。
_CRON_JOBS_FILENAME = Path("cron") / "jobs.json"


@dataclass
class MigrationReport:
    """迁移动作回执(测试断言面;字段全自明)。"""

    moved: list[str] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)
    jobs_rewritten: int = 0
    legacy_dir_removed: bool = False

    @property
    def did_anything(self) -> bool:
        return bool(self.moved or self.jobs_rewritten or self.legacy_dir_removed)


def migrate_legacy_plugins_dir(home: Path) -> MigrationReport:
    """旧 ``<home>/plugins`` 平铺配置一次性迁入 ``<home>/config``。

    语义(逐条):

    - 只搬**平铺文件**(旧布局里配置文件恒平铺;子目录 = 市场插件安装件,
      属安装根语义,原地保留绝不触碰);
    - 目标同名文件已存在 → 跳过不覆盖(用户在 config/ 已有同名件时,
      旧件留在原地,不静默丢数据);
    - cron ``jobs.json`` 的 job ``category`` 字段指向旧目录平铺 YAML 的
      绝对路径 → 原位改写为新目录(create 时解析为绝对路径存储,grill Q5);
      只改前缀命中旧目录且后缀为 .yaml/.yml 的值,其余字段零触碰;
    - 旧目录搬空(无残留子目录/文件)→ 移除;留有安装件 → 原样保留;
    - 幂等:新目录已存在时逐件按「不覆盖」继续,重跑零动作。

    失败处理:单文件搬移/账本改写失败不中断整体(能迁多少迁多少),
    异常原样上抛给调用方日志包装 —— 调用方(entry.py/cli.py)负责
    「失败只留痕不拦服务」。
    """
    report = MigrationReport()
    home = Path(home)
    legacy = home / LEGACY_CONFIG_DIR_NAME
    target_root = home / CONFIG_DIR_NAME
    if legacy.is_dir():
        target_root.mkdir(parents=True, exist_ok=True)
        for source in sorted(legacy.iterdir()):
            if not source.is_file():
                continue  # 子目录 = 市场插件安装件,原地保留
            target = target_root / source.name
            if target.exists():
                report.skipped_existing.append(source.name)
                continue
            shutil.move(str(source), str(target))
            report.moved.append(source.name)
        if not any(legacy.iterdir()):
            legacy.rmdir()
            report.legacy_dir_removed = True
    report.jobs_rewritten = _rewrite_cron_job_paths(
        home / _CRON_JOBS_FILENAME, legacy_root=legacy, new_root=target_root
    )
    return report


def _rewrite_cron_job_paths(jobs_file: Path, *, legacy_root: Path, new_root: Path) -> int:
    """jobs.json 内指向旧配置目录的 category 路径原位改写,返回改写条数。

    只认 ``jobs`` 数组内 dict 的 ``category`` 字段(D2 载荷契约);文件缺席
    / JSON 解析失败 / 结构不符 → 0 条(账本可能正被并发写,宁可放过不可
    写坏;下次启动重跑补齐)。
    """
    if not jobs_file.is_file():
        return 0
    try:
        payload = json.loads(jobs_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    jobs = payload.get("jobs") if isinstance(payload, dict) else payload
    if not isinstance(jobs, list):
        return 0
    legacy_prefix = str(legacy_root)
    rewritten = 0
    for job in jobs:
        if not isinstance(job, dict):
            continue
        category = job.get("category")
        if not isinstance(category, str) or not category.startswith(legacy_prefix + str(Path("/"))):
            continue
        if not category.lower().endswith((".yaml", ".yml")):
            continue
        job["category"] = str(new_root / Path(category).name)
        rewritten += 1
    if rewritten:
        try:
            jobs_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        except OSError:
            return 0  # 写失败按未改算,下次启动重跑
    return rewritten

"""config_layout:数据根 plugins/ → config/ 一次性迁移单测(2026-10-11)。

迁移语义逐条钉死:平铺文件搬移不覆盖 / 市场插件子目录原地保留 / cron
jobs.json category 路径原位改写 / 搬空后旧目录移除 / 幂等重跑零动作 /
账本缺席与坏 JSON 放过不炸。
"""

from __future__ import annotations

import json
from pathlib import Path

from myssia.config_layout import (
    CONFIG_DIR_NAME,
    LEGACY_CONFIG_DIR_NAME,
    migrate_legacy_plugins_dir,
)


def _make_home(tmp_path: Path) -> tuple[Path, Path, Path]:
    home = tmp_path / "home"
    legacy = home / LEGACY_CONFIG_DIR_NAME
    config = home / CONFIG_DIR_NAME
    legacy.mkdir(parents=True)
    return home, legacy, config


def test_moves_flat_files_and_removes_empty_legacy_dir(tmp_path: Path) -> None:
    home, legacy, config = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    (legacy / "telegram-web.yaml.bak-20261009").write_text("old\n", encoding="utf-8")

    report = migrate_legacy_plugins_dir(home)

    assert report.moved == ["ai-news.yaml", "telegram-web.yaml.bak-20261009"]
    assert (config / "ai-news.yaml").read_text(encoding="utf-8") == "id: ai-news\n"
    assert report.legacy_dir_removed is True
    assert not legacy.exists()


def test_never_overwrites_existing_target(tmp_path: Path) -> None:
    home, legacy, config = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: old\n", encoding="utf-8")
    config.mkdir()
    (config / "ai-news.yaml").write_text("id: user-edited\n", encoding="utf-8")

    report = migrate_legacy_plugins_dir(home)

    assert report.skipped_existing == ["ai-news.yaml"]
    assert (config / "ai-news.yaml").read_text(encoding="utf-8") == "id: user-edited\n"
    assert (legacy / "ai-news.yaml").exists()  # 旧件留在原地,不静默丢
    assert report.legacy_dir_removed is False


def test_market_subdirs_stay_in_legacy_dir(tmp_path: Path) -> None:
    home, legacy, _ = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    installed = legacy / "myssia-proxy"
    installed.mkdir()
    (installed / "plugin.yaml").write_text("id: myssia-proxy\n", encoding="utf-8")

    report = migrate_legacy_plugins_dir(home)

    assert installed.is_dir() and (installed / "plugin.yaml").is_file()
    assert report.legacy_dir_removed is False  # 留有安装件,原样保留


def test_rewrites_cron_job_category_paths(tmp_path: Path) -> None:
    home, legacy, config = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    jobs_file = home / "cron" / "jobs.json"
    jobs_file.parent.mkdir()
    jobs_file.write_text(
        json.dumps(
            {
                "jobs": [
                    {"id": "a", "category": str(legacy / "ai-news.yaml")},
                    {"id": "b", "category": "/elsewhere/keep.yaml"},
                    {"id": "c", "category": str(legacy) + "/not-yaml.txt"},
                    {"id": "d", "category": 42},
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    report = migrate_legacy_plugins_dir(home)

    assert report.jobs_rewritten == 1
    payload = json.loads(jobs_file.read_text(encoding="utf-8"))
    assert payload["jobs"][0]["category"] == str(config / "ai-news.yaml")
    assert payload["jobs"][1]["category"] == "/elsewhere/keep.yaml"
    assert payload["jobs"][2]["category"] == str(legacy) + "/not-yaml.txt"


def test_missing_or_corrupt_jobs_file_is_tolerated(tmp_path: Path) -> None:
    home, legacy, _ = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    # jobs.json 缺席
    assert migrate_legacy_plugins_dir(home).jobs_rewritten == 0
    # jobs.json 坏 JSON
    (home / "cron").mkdir()
    (home / "cron" / "jobs.json").write_text("{not json", encoding="utf-8")
    assert migrate_legacy_plugins_dir(home).jobs_rewritten == 0


def test_idempotent_rerun_is_noop(tmp_path: Path) -> None:
    home, legacy, config = _make_home(tmp_path)
    (legacy / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    first = migrate_legacy_plugins_dir(home)
    assert first.did_anything

    second = migrate_legacy_plugins_dir(home)

    assert not second.did_anything
    assert (config / "ai-news.yaml").exists()


def test_fresh_home_without_legacy_dir_is_noop(tmp_path: Path) -> None:
    home = tmp_path / "fresh"
    home.mkdir()

    report = migrate_legacy_plugins_dir(home)

    assert not report.did_anything
    assert not (home / CONFIG_DIR_NAME).exists()  # 无旧目录不凭空建新目录

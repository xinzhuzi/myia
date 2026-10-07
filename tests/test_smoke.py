"""Stdlib-only smoke tests: they must pass in a dependency-free environment."""

import myssia


def test_version():
    assert myssia.__version__ == "0.0.3"


def test_pipeline_stages():
    from myssia.pipeline import STAGES

    assert STAGES == ["fetch", "classify", "dedup", "analyze", "enrich", "push"]
    assert len(STAGES) == 6


def test_cli_entrypoint_callable():
    from myssia.cli import main

    assert callable(main)


def test_dedup_registry_importable():
    from myssia.dedup import DedupRegistry

    assert callable(DedupRegistry)


def test_seven_categories():
    from myssia.classify.builtin import SEVEN_CATEGORIES

    assert len(SEVEN_CATEGORIES) == 7

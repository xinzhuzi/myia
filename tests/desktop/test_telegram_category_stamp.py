"""telegram 三线落库的源→品类盖戳映射单测(10-09-tg-category-entry)."""

from types import SimpleNamespace

from desktop import entry


def _config(config_id: str, *source_names: str):
    return SimpleNamespace(
        id=config_id,
        sources=[SimpleNamespace(name=name, engine="tg_web") for name in source_names],
    )


def test_source_categories_maps_main_and_web_files():
    main = _config("telegram-groups", "telegram-mihomo_party_group", "telegram-other")
    web = _config("telegram-web", "telegram-web_only_channel")
    mapping = entry._telegram_source_categories(main, web)
    assert mapping == {
        "telegram-mihomo_party_group": "telegram-groups",
        "telegram-other": "telegram-groups",
        "telegram-web_only_channel": "telegram-web",
    }


def test_source_categories_none_config_and_blank_ids_skipped():
    main = _config("telegram-groups", "telegram-a")
    web = _config("", "telegram-b")  # id 空的坏档:整文件不入映射
    assert entry._telegram_source_categories(main, None, web) == {"telegram-a": "telegram-groups"}


def test_source_categories_first_config_wins_on_duplicate_source():
    main = _config("telegram-groups", "telegram-dupe")
    web = _config("telegram-web", "telegram-dupe")
    # 主品类在前:同名源主品类侧优先(与装配「同一群只跑一线」判例同序)
    assert entry._telegram_source_categories(main, web)["telegram-dupe"] == "telegram-groups"

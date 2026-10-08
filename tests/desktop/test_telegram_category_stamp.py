"""telegram 三线落库的源→品类盖戳映射单测(10-09-tg-category-entry)."""

from types import SimpleNamespace

from desktop import entry


def _config(config_id: str, *source_names: str):
    return SimpleNamespace(
        id=config_id,
        sources=[SimpleNamespace(name=name, engine="tg_web") for name in source_names],
    )


def test_source_categories_maps_main_and_web_files():
    # AC6 归一后实况:三文件 id 统一 telegram,映射随之全出「telegram」
    # (映射无写死词表,纯随 config.id —— 文件仍各自持源)
    main = _config("telegram", "telegram-mihomo_party_group", "telegram-other")
    web = _config("telegram", "telegram-web_only_channel")
    mapping = entry._telegram_source_categories(main, web)
    assert mapping == {
        "telegram-mihomo_party_group": "telegram",
        "telegram-other": "telegram",
        "telegram-web_only_channel": "telegram",
    }


def test_source_categories_none_config_and_blank_ids_skipped():
    main = _config("telegram", "telegram-a")
    web = _config("", "telegram-b")  # id 空的坏档:整文件不入映射
    assert entry._telegram_source_categories(main, None, web) == {"telegram-a": "telegram"}


def test_source_categories_first_config_wins_on_duplicate_source():
    # 先到先得契约:id 异构夹具钉死保序(归一后恒同值;若未来拆档不回退)
    main = _config("telegram-main", "telegram-dupe")
    web = _config("telegram-web", "telegram-dupe")
    assert entry._telegram_source_categories(main, web)["telegram-dupe"] == "telegram-main"

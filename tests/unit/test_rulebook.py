from icehockey_rules.rulebook import get_rulebooks


def test_get_rulebook() -> None:
    assert get_rulebooks()

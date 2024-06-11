from icehockey_rules.chat import _rule_number_to_prompt


def test_rule_number_to_prompt() -> None:
    # WHEN
    prompt = _rule_number_to_prompt("67")

    # THEN
    assert prompt
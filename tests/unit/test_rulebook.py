from icehockey_rules.rulebook import (
    get_rulebooks,
    _replace_list_elements_with_lists,
    get_chunked_iihf_rulebook_records,
)


def test_get_rulebook() -> None:
    assert get_rulebooks()


def test_get_chunked_iihf_rulebook_records() -> None:
    # GIVEN
    rulebooks = get_rulebooks()
    iihf_rulebook = rulebooks["iihf"]

    # WHEN
    iihf_rulebook_records = get_chunked_iihf_rulebook_records(iihf_rulebook)

    # THEN
    boarding_minor_penalty_subsection = iihf_rulebook_records[793]
    assert boarding_minor_penalty_subsection["metadata"]["title"] == "MINOR PENALTY"
    assert (
        boarding_minor_penalty_subsection["metadata"]["parsed_title"]
        == "BOARDING - MINOR PENALTY"
    )
    assert len(iihf_rulebook_records) == 1126


def test_replace_list_elements_with_lists() -> None:
    # GIVEN a list and two sublists
    original_list = [0, 1, 2, 3, 4]
    index_list_map = {1: ["a", "b"], 3: ["c", "d", "e"]}

    # WHEN
    updated_list = _replace_list_elements_with_lists(
        original_list=original_list, index_list_map=index_list_map
    )

    # THEN
    assert updated_list == [0, "a", "b", 2, "c", "d", "e", 4]

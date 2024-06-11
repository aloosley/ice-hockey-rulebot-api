__version__ = "v1"

from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from icehockey_rules.config import get_config
from langchain_text_splitters import RecursiveCharacterTextSplitter

config = get_config()


def get_rulebooks(
    rulebooks_filepath: Path = config.rulebooks_filepath,
) -> dict[str, Any]:
    with rulebooks_filepath.open("r") as f:
        rulebooks = yaml.load(f, yaml.loader.FullLoader)

    _validate_rulebooks(rulebooks)
    return rulebooks


def _validate_rulebooks(rulebook: dict[str, Any]) -> None:
    ids = []
    for rule in rulebook["iihf"]["rules"]:
        if "query" in rule:
            for situation in rule["query"]:
                ids.append(situation["number"])

        for subsection in rule["subsections"]:
            ids.append(subsection["number"])

    assert len(ids) == len(set(ids))


def get_iihf_situations_df(
    rulebooks_filepath: Path = config.rulebooks_filepath,
) -> pd.DataFrame:
    rulebooks = get_rulebooks(rulebooks_filepath)

    iihf_situations = []
    for rule in rulebooks["iihf"]["rules"]:
        iihf_situations += rule.get("situations", [])

    iihf_situations_df = pd.DataFrame(iihf_situations)
    iihf_situations_df["char_count"] = iihf_situations_df.apply(
        lambda situation: len(situation["question"]) + len(situation["answer"]), axis=1
    )
    iihf_situations_df.char_count.hist(bins=50)

    return iihf_situations_df


def get_iihf_subsections_df(
    rulebooks_filepath: Path = config.rulebooks_filepath,
) -> pd.DataFrame:
    rulebooks = get_rulebooks(rulebooks_filepath)

    iihf_subsections = []
    for rule in rulebooks["iihf"]["rules"]:
        iihf_subsections += rule["subsections"]

    iihf_subsections_df = pd.DataFrame(iihf_subsections)
    iihf_subsections_df["char_count"] = iihf_subsections_df["rule"].map(
        lambda rule: len(rule)
    )
    iihf_subsections_df.char_count.hist(bins=50)

    return iihf_subsections_df


def _parse_subsection_title(subsection: dict[str, Any], rule: dict[str, Any]) -> str:
    parsed_subsection_title = subsection["title"]

    # If rule is a penalty rule, title the subsections more informatively - "{RULE_TITLE} - {PENALTY TYPE}"
    if (
        rule["subsections"][0]["title"] == (rule_title := rule["title"])
        and (subsection_title := subsection["title"]) != rule["title"]
    ):
        parsed_subsection_title = f"{rule_title} - {subsection_title}"

    return parsed_subsection_title


SOURCE = "iihf-2022-2024-customparsed-for-qa"


def _get_iihf_subsection_records(
    rule: dict[str, Any], source: str = SOURCE
) -> list[dict[str, Any]]:
    subsections = rule["subsections"]

    return [
        dict(
            id=str(subsection["number"]),
            metadata=dict(
                type="subsection",
                title=subsection["title"],
                parsed_title=_parse_subsection_title(subsection, rule),
                text=subsection["rule"],
                rule_references=[],
                rule_number=str(rule["number"]),
                rule_title=rule["title"],
                source=f"{source}__{rule['number']}",
                tags=rule["tags"] if "tags" in rule else [],
            ),
        )
        for subsection in subsections
    ]


def _get_iihf_situation_records(
    rule: dict[str, Any], source: str = SOURCE
) -> list[dict[str, Any]]:
    if "situations" not in rule:
        return []

    return [
        dict(
            id=str(situation["number"]) + "-QA",
            metadata=dict(
                type="query",
                title=rule["title"],
                parsed_title=rule["title"],
                text=f"SITUATION:\n{situation['question']}\n\nRESPONSE:\n{situation['answer']}",
                rule_references=[str(ref) for ref in situation["rule references"]],
                rule_number=str(rule["number"]),
                rule_title=rule["title"],
                source=f"{source}__{situation['number']}",
                tags=rule["tags"] if "tags" in rule else [],
            ),
        )
        for situation in rule["situations"]
    ]


def get_chunked_iihf_rulebook_records(
    iihf_rulebook: dict[str, Any]
) -> list[dict[str, Any]]:
    iihf_rulebook_records = []

    for rule in iihf_rulebook["rules"]:
        iihf_rulebook_records += _get_iihf_subsection_records(rule)
        iihf_rulebook_records += _get_iihf_situation_records(rule)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.splitter.max_chunk_size,
        chunk_overlap=config.splitter.chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    return _splitsert_iihf_rulebook_records(
        iihf_rulebook_records=iihf_rulebook_records,
        text_splitter=text_splitter,
    )


def _splitsert_iihf_rulebook_records(
    iihf_rulebook_records: list[dict[str, Any]],
    text_splitter: RecursiveCharacterTextSplitter,
) -> list[dict[str, Any]]:
    """Split using text_splitter and insert new records."""
    rule_record_chunks: dict[int, list[dict[str, Any]]] = {}
    for rule_record_idx, rule_record in enumerate(iihf_rulebook_records):
        text = rule_record["metadata"]["text"]
        if len(text) > text_splitter._chunk_size:
            rule_record_chunks[rule_record_idx] = [
                dict(
                    id=rule_record["id"] + f"-{split_idx}",
                    metadata=dict(
                        type=rule_record["metadata"]["type"] + "-chunk",
                        title=rule_record["metadata"]["title"],
                        parsed_title=rule_record["metadata"]["parsed_title"],
                        text=split_text,
                        rule_references=rule_record["metadata"]["rule_references"],
                        rule_number=rule_record["metadata"]["rule_number"],
                        rule_title=rule_record["metadata"]["rule_title"],
                        source=rule_record["metadata"]["source"],
                        tags=rule_record["metadata"]["tags"],
                    ),
                )
                for split_idx, split_text in enumerate(text_splitter.split_text(text))
            ]

    return _replace_list_elements_with_lists(
        original_list=iihf_rulebook_records, index_list_map=rule_record_chunks
    )


def _replace_list_elements_with_lists(
    original_list: list[Any], index_list_map: dict[int, list[Any]]
) -> list[Any]:

    list_size_diff = 0

    for replacement_index, list_to_insert in index_list_map.items():
        # List grows in size, so find the actual replacement index
        updated_replacement_index = replacement_index + list_size_diff
        del original_list[updated_replacement_index]
        original_list[
            updated_replacement_index:updated_replacement_index
        ] = list_to_insert
        list_size_diff += len(list_to_insert) - 1

    return original_list


@lru_cache
def get_inmem_chunked_iihf_rulebook_index() -> dict[str, Any]:
    """IIHF rulebook chunks keyed by chunk id"""
    return {
        rule_chunk["id"]: rule_chunk["metadata"]
        for rule_chunk in get_chunked_iihf_rulebook_records(get_rulebooks()["iihf"])
    }


@lru_cache
def get_inmem_iihf_rulebook_index() -> dict[str, Any]:
    """IIHF rulebook rules keyed by rule number"""
    return {str(rule["number"]): rule for rule in get_rulebooks()["iihf"]["rules"]}

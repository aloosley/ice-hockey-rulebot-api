from pathlib import Path
from typing import Any

import pandas as pd
import tqdm
import yaml


def get_rulebooks(structured_rulebook_filepath: Path = Path("../../data/iihf-qa.yaml")) -> dict[str, Any]:
    with structured_rulebook_filepath.open("r") as f:
        rulebooks = yaml.load(f, yaml.loader.FullLoader)

    _validate_rulebooks(rulebooks)
    return rulebooks


def _validate_rulebooks(rulebook: dict[str, Any]) -> None:
    ids = []
    for rule in rulebook["iihf"]["rules"]:
        if "situation" in rule:
            for situation in rule["situation"]:
                ids.append(situation["number"])

        for subsection in rule["subsections"]:
            ids.append(subsection["number"])

    assert len(ids) == len(set(ids))


def get_iihf_situations_df(structured_rulebook_filepath: Path = Path("../../data/iihf-qa.yaml")) -> pd.DataFrame:
    rulebooks = get_rulebooks(structured_rulebook_filepath)

    iihf_situations = []
    for rule in rulebooks["iihf"]["rules"]:
        iihf_situations += rule.get("situations", [])

    iihf_situations_df = pd.DataFrame(iihf_situations)
    iihf_situations_df["char_count"] = iihf_situations_df.apply(
        lambda situation: len(situation["question"]) + len(situation["answer"]), axis=1)
    iihf_situations_df.char_count.hist(bins=50)

    return iihf_situations_df


def get_iihf_subsections_df(structured_rulebook_filepath: Path = Path("../../data/iihf-qa.yaml")) -> pd.DataFrame:
    rulebooks = get_rulebooks(structured_rulebook_filepath)

    iihf_subsections = []
    for rule in rulebooks["iihf"]["rules"]:
        iihf_subsections += rule["subsections"]

    iihf_subsections_df = pd.DataFrame(iihf_subsections)
    iihf_subsections_df["char_count"] = iihf_subsections_df["rule"].map(lambda rule: len(rule))
    iihf_subsections_df.char_count.hist(bins=50)

    return iihf_subsections_df


def _parse_subsection_title(subsection: dict[str, Any], rule: dict[str, Any]) -> str:
    parsed_subsection_title = subsection["title"]

    # If rule is a penalty rule, title the subsections more informatively - "{RULE_TITLE} - {PENALTY TYPE}"
    if rule["subsections"][0]["title"] == (rule_title := rule["title"]) and (subsection_title := subsection["title"]) != rule["title"]:
        parsed_subsection_title = f"{rule_title} - {subsection_title}"

    return parsed_subsection_title


SOURCE = "iihf-2022-2024-customparsed-for-qa"


def _get_iihf_subsection_records(rule: dict[str, Any], source: str = SOURCE) -> list[dict[str, Any]]:
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
        ) for subsection in subsections
    ]


def _get_iihf_situation_records(rule: dict[str, Any], source: str = SOURCE) -> list[dict[str, Any]]:
    if "situations" not in rule:
        return []

    return [
        dict(
            id=str(situation["number"]) + "-QA",
            metadata=dict(
                type="situation",
                title=rule["title"],
                parsed_title=rule["title"],
                text=f"SITUATION:\n{situation['question']}\n\nRESPONSE:\n{situation['answer']}",
                rule_references=[str(ref) for ref in situation["rule references"]],
                rule_number=str(rule["number"]),
                rule_title=rule["title"],
                source=f"{source}__{situation['number']}",
                tags=rule["tags"] if "tags" in rule else [],
            )
        ) for situation in rule["situations"]
    ]


def get_iihf_rulebook_records(iihf_rulebook: dict[str, Any]) -> list[dict[str, Any]]:
    iihf_rulebook_records = []

    for rule in tqdm(iihf_rulebook["rules"]):
        iihf_rulebook_records += _get_iihf_subsection_records(rule)
        iihf_rulebook_records += _get_iihf_situation_records(rule)

    return iihf_rulebook_records

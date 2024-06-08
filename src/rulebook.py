from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def get_rule_book(structured_rulebook_filepath: Path = Path("../data/iihf-qa.yaml")) -> dict[str, Any]:
    with structured_rulebook_filepath.open("r") as f:
        rulebook = yaml.load(f, yaml.loader.FullLoader)

    _validate_rulebook(rulebook)
    return rulebook


def _validate_rulebook(rulebook: dict[str, Any]) -> None:
    ids = []
    for rule in rulebook["iihf"]["rules"]:
        if "situation" in rule:
            for situation in rule["situation"]:
                ids.append(situation["number"])

        for subsection in rule["subsections"]:
            ids.append(subsection["number"])

    assert len(ids) == len(set(ids))


def get_rule_situations_df(structured_rulebook_filepath: Path = Path("../data/iihf-qa.yaml")) -> pd.DataFrame:
    rulebook = get_rule_book(structured_rulebook_filepath)

    rule_situations = []
    for rule in rulebook["iihf"]["rules"]:
        rule_situations += rule.get("situations", [])

    rule_situations_df = pd.DataFrame(rule_situations)
    rule_situations_df["char_count"] = rule_situations_df.apply(
        lambda situation: len(situation["question"]) + len(situation["answer"]), axis=1)
    rule_situations_df.char_count.hist(bins=50)

    return rule_situations_df


def get_rule_subsections_df(structured_rulebook_filepath: Path = Path("../data/iihf-qa.yaml")) -> pd.DataFrame:
    rulebook = get_rule_book(structured_rulebook_filepath)

    rule_subsections = []
    for rule in rulebook["iihf"]["rules"]:
        rule_subsections += rule["subsections"]

    rule_subsections_df = pd.DataFrame(rule_subsections)
    rule_subsections_df["char_count"] = rule_subsections_df["rule"].map(lambda rule: len(rule))
    rule_subsections_df.char_count.hist(bins=50)

    return rule_subsections_df

from typing import Iterable

import pandas as pd

from icehockey_rules.retrieve import retrieve, chunk_matches_to_rules_df
from icehockey_rules.rulebook import (
    get_inmem_iihf_rulebook_index,
    _parse_subsection_title,
)


inmem_iihf_rulebook_index = get_inmem_iihf_rulebook_index()


SYSTEM_PROMPT = """You are an ice hockey rule assistant.
Given a question or situation, describe what the rules indicate should happen using only the context provided.
Always source the associated rule number and title in the context.
If you cannot answer based on the context, respond with "I couldn't come up with an answer, but here are
some potentially relevant rules:" followed by a list the RULE numbers and titles found in the context.
"""


def query_to_rag_prompt(
    query: str,
    top_k_chunks: int = 10,
    top_k_rules: int = 6,
    rule_score_threshold: float = 0.3,
) -> str:

    chunk_matches = retrieve(query=query, top_k=top_k_chunks).matches
    rule_matches_df: pd.DataFrame = chunk_matches_to_rules_df(
        matches=chunk_matches,
        top_k_rules=top_k_rules,
        rule_score_threshold=rule_score_threshold,
    )
    rule_numbers = rule_matches_df.index
    return get_rag_prompt(query=query, rule_numbers=rule_numbers)


def get_rag_prompt(query: str, rule_numbers: Iterable[str]) -> str:
    rag_prompt = f"""
CONTEXT:
    """
    for rule_number in rule_numbers:
        rag_prompt += _rule_number_to_prompt(rule_number)

    rag_prompt += f"""
SITUATION: {query}

RESULT:
    """
    return rag_prompt


def _rule_number_to_prompt(rule_number: str) -> str:
    rule = inmem_iihf_rulebook_index[rule_number]

    rule_prompt = f"""
    RULE {rule_number}. {rule["title"]}:
    """
    for subsection in rule["subsections"]:
        rule_prompt += f"""
        {subsection["number"]}. {_parse_subsection_title(rule=rule, subsection=subsection)}:
        {subsection["rule"]}"""

    situations = rule.get("situations", [])
    if len(situations):
        rule_prompt += f"""
    RULE {rule_number} SITUATIONS:
        """
    for situation in situations:
        rule_prompt += f"""
        SITUATION {situation["number"]}:

            QUESTION: {situation["question"]}
            ANSWER: {situation["answer"]}"""

    return rule_prompt

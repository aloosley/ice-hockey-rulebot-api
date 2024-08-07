import json

from icehockey_rules.chat import query_to_retrieved_rules_and_rag_prompt, SYSTEM_PROMPT
from icehockey_rules.retrieve import openai_client

from openai.types.chat import ChatCompletionMessage


def one_off_question_answer(
    query: str,
    llm_model: str,
    llm_temperature: float,
    top_k_chunks: int,
    top_k_rules: int,
    rule_score_threshold: float,
    system_prompt: str = SYSTEM_PROMPT,
) -> ChatCompletionMessage:
    rule_matches_df, rag_prompt = query_to_retrieved_rules_and_rag_prompt(
        query,
        top_k_chunks=top_k_chunks,
        top_k_rules=top_k_rules,
        rule_score_threshold=rule_score_threshold,
    )
    completion = openai_client.chat.completions.create(
        model=llm_model,
        messages=[
            dict(role="system", content=system_prompt),
            dict(role="user", content=rag_prompt),
        ],
        temperature=llm_temperature,
    )
    message = completion.choices[0].message
    message.rule_matches_df = json.loads(rule_matches_df.to_json(orient="index"))
    return message

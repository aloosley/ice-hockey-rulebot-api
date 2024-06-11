from icehockey_rules.chat import query_to_rag_prompt, SYSTEM_PROMPT
from icehockey_rules.retrieve import openai_client

from openai.types.chat import ChatCompletionMessage


def one_off_question_answer(
    query: str,
    model: str = "gpt-4-turbo",
    temperature: float = 0.0,
    top_k_chunks: int = 10,
    top_k_rules: int = 6,
    rule_score_threshold: float = 0.4,
    system_prompt: str = SYSTEM_PROMPT,
) -> ChatCompletionMessage:
    rag_prompt = query_to_rag_prompt(
        query,
        top_k_chunks=top_k_chunks,
        top_k_rules=top_k_rules,
        rule_score_threshold=rule_score_threshold,
    )
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            dict(role="system", content=system_prompt),
            dict(role="user", content=rag_prompt),
        ],
        temperature=temperature,
    )
    return completion.choices[0].message

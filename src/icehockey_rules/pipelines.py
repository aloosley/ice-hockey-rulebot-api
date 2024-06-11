from icehockey_rules.chat import query_to_rag_prompt, SYSTEM_PROMPT
from icehockey_rules.retrieve import openai_client

from openai.types.chat import ChatCompletionMessage


def one_off_question_answer(
    query: str,
    model: str = "gpt-4-turbo",
    temperature: float = 0.0,
    system_prompt: str = SYSTEM_PROMPT,
) -> ChatCompletionMessage:
    rag_prompt = query_to_rag_prompt(query)
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            dict(role="system", content=system_prompt),
            dict(role="user", content=rag_prompt),
        ],
        temperature=temperature,
    )
    return completion.choices[0].message

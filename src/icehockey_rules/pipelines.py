from icehockey_rules.chat import query_to_rag_prompt, SYSTEM_PROMPT
from icehockey_rules.retrieve import openai_client


def one_off_question_answer(query: str) -> str:
    rag_prompt = query_to_rag_prompt(query)
    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            dict(role="system", content=SYSTEM_PROMPT),
            dict(role="user", content=rag_prompt),
        ],
        temperature=0.0
    )
    return completion.choices[0].message.content

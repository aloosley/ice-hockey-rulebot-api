from typing import Any

from fastapi import Depends, APIRouter

from icehockey_rules.config import Config, get_config
from icehockey_rules.pipelines import one_off_question_answer

chat_router = APIRouter()


@chat_router.post(path="/completions", status_code=200)
async def one_off_situation(
    query: str,
    config: Config = Depends(get_config),
) -> dict[str, Any]:
    return dict(one_off_question_answer(query=query, model=config.llm.model, temperature=config.llm.temperature))

from typing import Any

from fastapi import Depends, APIRouter
from icehockey_rules.config import Config, get_config
from icehockey_rules.pipelines import one_off_question_answer
from icehockey_rules.retrieve import retrieve, chunk_matches_to_rules_df

chat_router = APIRouter()


config = get_config()
DEFAULT_LLM_MODEL = config.llm.model
DEFAULT_TOP_K_RULES = config.retriever.top_k_rules


@chat_router.post(path="/completions", status_code=200)
async def one_off_situation(
    query: str,
    llm_model: str = DEFAULT_LLM_MODEL,
    top_k_rules: int = DEFAULT_TOP_K_RULES,
    config: Config = Depends(get_config),
) -> dict[str, Any]:
    return dict(
        one_off_question_answer(
            query=query,
            llm_model=llm_model,
            top_k_rules=top_k_rules,
            top_k_chunks=config.retriever.top_k_chunks,
            llm_temperature=config.llm.temperature,
            rule_score_threshold=0.4,
        )
    )


context_router = APIRouter()


@context_router.post(path="/vector_search/retrieve/v1", status_code=200)
async def rule_retrieval(
    query: str,
    top_k_rules: int = DEFAULT_TOP_K_RULES,
    rule_score_threshold: float = 0.4,
    config: Config = Depends(get_config),
) -> dict[str, Any]:
    chunk_matches = retrieve(query=query, top_k=config.retriever.top_k_chunks).matches
    return chunk_matches_to_rules_df(
        chunk_matches,
        top_k_rules=top_k_rules,
        rule_score_threshold=rule_score_threshold,
    ).to_dict()

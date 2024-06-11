import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Index, QueryResponse
from pinecone.grpc import PineconeGRPC as Pinecone

from icehockey_rules.config import get_config
from icehockey_rules.rulebook import (
    get_inmem_chunked_iihf_rulebook_index,
    __version__ as parsing_version,
    get_inmem_iihf_rulebook_index,
)

_ = load_dotenv()
config = get_config()


inmem_chunked_iihf_rulebook_index = get_inmem_chunked_iihf_rulebook_index()
inmem_iihf_rulebook_index = get_inmem_iihf_rulebook_index()


openai_api_key = os.getenv("OPENAI_API_KEY") or "OPENAI_API_KEY"
openai_client = OpenAI(api_key=openai_api_key)

pinecone_api_key = os.getenv("PINECONE_API_KEY") or "PINECONE_API_KEY"
pinecone_client = Pinecone(api_key=pinecone_api_key)

INDEX_NAME = f"rulebook--{parsing_version}--{config.embedder.model}"
PINECONE_INDEX = pinecone_client.Index(INDEX_NAME)

if PINECONE_INDEX.describe_index_stats()["total_vector_count"] != len(
    inmem_chunked_iihf_rulebook_index
):
    raise IndexError(
        f"Pinecone index with name {INDEX_NAME} has {PINECONE_INDEX.describe_index_stats()['total_vector_count']} "
        f"vectors, but loaded and chunked rulebook has {len(inmem_chunked_iihf_rulebook_index)} entrys. Something is wrong. "
        f"If the parsing or rulebook structure was changed, you might have to re-embed and index (see notebooks)."
    )


def retrieve(query: str, top_k: int, index: Index = PINECONE_INDEX) -> QueryResponse:
    query_vector = (
        openai_client.embeddings.create(input=[query], model=config.embedder.model)
        .data[0]
        .embedding
    )

    return index.query(vector=query_vector, top_k=top_k, include_values=False)


def chunk_matches_to_rules_df(
    matches: list[str, Any], top_k_rules: int = 10, rule_score_threshold: float = 0.53
) -> pd.DataFrame:
    """Input QueryResponse.matches list of chunk records, and get rules and scores back."""
    df = (
        pd.DataFrame(
            [
                (
                    inmem_chunked_iihf_rulebook_index[match["id"]]["rule_number"],
                    match["score"],
                )
                for match in matches
            ],
            columns=["rule_number", "score"],
        )
        .groupby(["rule_number"])
        .agg(dict(score=["sum", "count"]))
        .sort_values(("score", "sum"), ascending=False)
    )
    df = df[:top_k_rules]
    df = df[df["score"]["sum"] > rule_score_threshold]
    df["title"] = df.index.map(
        lambda rule_number: inmem_iihf_rulebook_index[rule_number]["title"]
    )
    return df

import os

import pandas as pd
from numpy import array

os.environ["OPENAI_API_KEY"] = "dummy"
from icehockey_rules.retrieve import chunk_matches_to_rules_df


def test_chunk_matches_to_rules_df() -> None:
    # GIVEN
    matches = [
        {
            "id": "24.7-1",
            "metadata": None,
            "score": 0.67032886,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
        {
            "id": "24.7.0-QA-2",
            "metadata": None,
            "score": 0.66933966,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
        {
            "id": "70.7",
            "metadata": None,
            "score": 0.65272295,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
        {
            "id": "24.29.0-QA",
            "metadata": None,
            "score": 0.54033234,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
        {
            "id": "24.7.0-QA-1",
            "metadata": None,
            "score": 0.34033234,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
        {
            "id": "67.1",
            "metadata": None,
            "score": 0.34033234,
            "sparse_values": {"indices": [], "values": []},
            "values": [],
        },
    ]

    expected_rules_df = pd.DataFrame(
        data={
            ("score", "sum"): {
                "24": 2.22033,
                "70": 0.65272295,
            },
            ("score", "count"): {
                "24": 4,
                "70": 1,
            },
            ("chunk_id", "unique"): {
                "24": array(
                    ["24.7", "24.7.0-QA", "24.29.0-QA"],
                    dtype=object,
                ),
                "70": array(["70.7"], dtype=object),
            },
            ("title", ""): {
                "24": "PENALTY SHOT",
                "70": "LEAVING THE PLAYERS' BENCH OR PENALTY BOX",
            },
        },
    )
    expected_rules_df.index.name = "rule_number"

    # WHEN
    rules_df = chunk_matches_to_rules_df(
        matches=matches, top_k_rules=10, rule_score_threshold=0.4
    )

    # THEN
    pd.testing.assert_frame_equal(rules_df, expected_rules_df)

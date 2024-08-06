import os

import pytest
from starlette.testclient import TestClient


@pytest.mark.cha_ching
@pytest.mark.integration
def test_one_off_situation(app_test_client: TestClient) -> None:
    # GIVEN a rule question
    query = "What happens if a player comes off while another player is taking revenge for a dirty hit?"

    # WHEN calling the one-off situation endpoint
    response = app_test_client.post(
        url="/context/chat/completions",
        params=dict(query=query),
        headers=dict(access_token=os.getenv("API_KEY")),
    )

    # THEN
    response.raise_for_status()
    assert True

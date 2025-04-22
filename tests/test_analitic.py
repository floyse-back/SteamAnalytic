from httpx import AsyncClient

import pytest

host = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_get_best_sallers(session:AsyncClient):
    async with AsyncClient(base_url=host) as client:
        client.get("")

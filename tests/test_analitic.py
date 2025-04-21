from httpx import AsyncClient

import pytest



@pytest.mark.asyncio
async def test_get_best_sallers(session:AsyncClient):
    print("Hello World")

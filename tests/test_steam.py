import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUsersFullStats:

    async def test_correct_request(self,client:AsyncClient):
        response_1 = await client.get("/api/v1/steam/users_full_stats/floysefake")
        response_2 = await client.get("/api/v1/steam/users_full_stats/76561199054741771")

        #Test User floysefake
        assert response_1.status_code == 200
        assert response_1.json() != {}

        assert response_2.status_code == 200
        assert response_2.json() != {}

    async def test_not_found_user(self,client:AsyncClient):
        response_1 = await client.get("/api/v1/steam/users_full_stats/ytgfdbltootpphrhtrhltfbflgf")
        response_2 = await client.get("/api/v1/steam/users_full_stats/765611990544643434")

        #Test User
        assert response_1.status_code == 404
        assert response_1.json() == {"detail": "Steam user not found"}

        assert response_2.status_code == 404
        assert response_2.json() == {"detail": "Steam user not found"}

    async def test_private_user(self,client:AsyncClient):
        response_1 = await client.get("/api/v1/steam/users_full_stats/76561198061916691")

        assert response_1.status_code == 403
        assert response_1.json().get("detail")
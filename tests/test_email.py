import pytest



class TestEmail:
    @pytest.mark.parametrize(
        "type,status_code,email",
        [
            ("forgot_password",202,"new@gmail.com"),
            ("verify_email",202,"new@gmail.com"),
            ("delete_user",202,"new@gmail.com"),
         ]
    )
    async def test_send_email(self,login,type,users,status_code,email):
        new_client = login["client"]
        response = await new_client.post(
            url=f"/api/v1/send_email/{type}",
            params={"email": email}
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "type,status_code,email",
        [
            ("forgot_password",404,"badmail"),
            ("verify_email",404,"fsdfregregrgrdfdfrgrbfdvcvccas@gmail.com"),
            ("verify_email", 404, "test@@dep.cm"),
            ("delete_user",404,"floyse.fake@dxs.com"),
            ("delete_user",404,"@##@dscscsdc"),
         ]
    )
    async def test_not_valid_email(self,type,users,login,status_code,email):
        new_client = login["client"]
        response = await new_client.post(
            url=f"/api/v1/send_email/{type}",
            params={"email": email}
        )

        assert response.status_code == status_code
        assert response.json()["detail"] == "User Not Found"

    @pytest.mark.parametrize(
        "type,status_code,email,excepted",
        [
            ("forgot_password", 202, "ivan.admin@example.com",None),
            ("verify_email", 401, "ivan.admin@example.com","Token not found"),
            ("delete_user", 401, "olena.admin@example.com","Token not found"),
        ]
    )
    async def test_send_email_not_auth(self,client,users, type, status_code, email,excepted):
        response = await client.post(
            url=f"/api/v1/send_email/{type}",
            params = {"email": email}
        )

        assert response.status_code == status_code

        if excepted:
            assert response.json()["detail"] == excepted

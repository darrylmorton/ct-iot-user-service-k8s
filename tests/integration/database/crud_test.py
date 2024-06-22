import crud


class TestCrud:
    username = "foo@home.com"
    password = "barbarba"

    async def test_find_users(self, db_cleanup):
        result = await crud.find_users()

        assert len(result) == 0

    async def test_find_user_by_username(self, db_cleanup):
        result = await crud.find_user_by_username(self.username)

        assert not result

    async def test_add_user(self, db_cleanup):
        result = await crud.add_user(_username=self.username, _password=self.password)

        assert result

    async def test_authorise(self, db_cleanup):
        expected_result = await crud.add_user(_username=self.username, _password=self.password)

        actual_result = await crud.authorise(self.username, self.password)

        assert actual_result.id == expected_result.id
        assert actual_result.username == expected_result.username
        assert actual_result.enabled is False

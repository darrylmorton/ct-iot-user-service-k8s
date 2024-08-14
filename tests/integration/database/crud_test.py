from database.crud import Crud


class TestCrud:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    user_id = "00000000-0000-0000-0000-000000000000"
    username = "foo@home.com"
    password = "barbarba"
    first_name = "Foo"
    last_name = "Bar"

    async def test_find_users(self, db_cleanup):
        result = await Crud().find_users()

        assert len(result) == 0

    async def test_find_user_by_id(self, db_cleanup):
        result = await Crud().find_user_by_id(self.id)

        assert not result

    async def test_find_user_by_id_and_enabled(self, db_cleanup):
        result = await Crud().find_user_by_id_and_enabled(self.id)

        assert not result

    async def test_find_user_by_username(self, db_cleanup):
        result = await Crud().find_user_by_username(self.username)

        assert not result

    async def test_add_user(self, db_cleanup):
        result = await Crud().add_user(_username=self.username, _password=self.password)

        assert result

    async def test_find_user_details(self, db_cleanup):
        result = await Crud().find_user_details()

        assert len(result) == 0

    async def test_user_details_by_user_id(self, db_cleanup):
        result = await Crud().find_user_details_by_user_id(self.user_id)

        assert not result

    async def test_add_user_details(self, db_cleanup):
        expected_result = await Crud().add_user(
            _username=self.username, _password=self.password
        )

        actual_result = await Crud().add_user_details(
            _user_id=expected_result.id,
            _first_name=self.first_name,
            _last_name=self.last_name,
        )

        assert actual_result.user_id == expected_result.id
        assert actual_result.first_name == self.first_name
        assert actual_result.last_name == self.last_name

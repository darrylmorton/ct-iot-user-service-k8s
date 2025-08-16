import pytest

from database.admin_crud import AdminCrud
from database.user_crud import UserCrud
from database.user_details_crud import UserDetailsCrud
import tests.config as test_config
from tests.helper import user_helper
from utils.validator_util import ValidatorUtil


class TestCrud:
    id = "848a3cdd-cafd-4ec6-a921-afb0bcc841dd"
    user_id = "00000000-0000-0000-0000-000000000000"
    username = test_config.USERNAME
    password = "barbarba"
    first_name = "Foo"
    last_name = "Bar"

    async def test_find_users(self, db_cleanup):
        result = await AdminCrud().find_users()

        assert len(result) == 0

    async def test_find_user_by_id(self, db_cleanup):
        result = await UserCrud().find_user_by_id(self.id)

        assert not result

    async def test_find_user_by_username(self, db_cleanup):
        result = await UserCrud().find_user_by_username(self.username)

        assert not result

    async def test_add_user(self, db_cleanup):
        result = await UserCrud().add_user(
            _username=self.username, _password=self.password
        )

        assert result

    async def test_user_details_by_user_id(self, db_cleanup):
        result = await UserDetailsCrud().find_user_details_by_user_id(self.user_id)

        assert not result

    async def test_add_user_details(self, db_cleanup):
        expected_result = await UserCrud().add_user(
            _username=self.username, _password=self.password
        )

        actual_result = await UserDetailsCrud().add_user_details(
            _user_id=expected_result.id,
            _first_name=self.first_name,
            _last_name=self.last_name,
        )

        assert actual_result.user_id == expected_result.id
        assert actual_result.first_name == self.first_name
        assert actual_result.last_name == self.last_name

    @pytest.mark.parametrize(
        "add_test_user",
        [[user_helper.create_signup_payload()]],
        indirect=True,
    )
    async def test_update_confirmed(self, db_cleanup, add_test_user):
        actual_result = await UserCrud().update_confirmed(
            _username=self.username, _confirmed=True
        )

        assert ValidatorUtil.validate_uuid4(str(actual_result[0])) is True
        assert actual_result[1] == test_config.USERNAME
        assert actual_result[2] is True

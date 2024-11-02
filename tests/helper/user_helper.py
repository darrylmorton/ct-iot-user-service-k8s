import uuid

import tests.config as test_config
from database.models import UserDetailsModel
from tests.database import async_session


def create_signup_payload(
    _username=test_config.SES_TARGET,
    _password="barbarba",
    _confirmed=False,
    _enabled=True,
    _is_admin=False,
    _first_name="Foo",
    _last_name="Bar",
):
    return {
        "username": _username,
        "password": _password,
        "confirmed": _confirmed,
        "enabled": _enabled,
        "is_admin": _is_admin,
        "first_name": _first_name,
        "last_name": _last_name,
    }


def create_login_payload(_username=test_config.SES_TARGET, _password="barbarba"):
    return {
        "username": _username,
        "password": _password,
    }


async def add_test_user_details(_user_id: uuid, _first_name="Foo", _last_name="Bar"):
    user_details = UserDetailsModel(
        user_id=_user_id,
        first_name=_first_name,
        last_name=_last_name,
    )

    async with async_session() as session:
        async with session.begin():
            session.add(user_details)
            await session.commit()

        await session.refresh(user_details)
        await session.close()

    return user_details

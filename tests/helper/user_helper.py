import uuid

from database.models import UserDetailsModel
from tests.database import async_session


def create_signup_payload(
    _username="foo@home.com",
    _password="barbarba",
    _enabled=False,
    _first_name="Foo",
    _last_name="Bar",
):
    return {
        "username": _username,
        "password": _password,
        "enabled": _enabled,
        "first_name": _first_name,
        "last_name": _last_name,
    }


def create_login_payload(_username="foo@home.com", _password="barbarba"):
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

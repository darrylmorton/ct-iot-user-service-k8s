from src.database import async_session
from src.models import UserDetailsModel


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


async def add_test_user_details(_user_id: int, _first_name="Foo", _last_name="Bar"):
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

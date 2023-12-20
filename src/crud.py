import bcrypt

from sqlalchemy import select
from starlette.responses import JSONResponse

from .config import get_logger
from .schemas import User, UserAuthenticated, UserDetails
from .database import async_session
from .models import UserModel, UserDetailsModel

logger = get_logger()


async def find_users(offset=0) -> list[User]:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).limit(25).offset(offset)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def find_user_by_username(username: str) -> User:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).where(UserModel.username == username)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().first()


async def add_user(_username: str, _password: str) -> JSONResponse | User:
    password = _password.encode("utf-8")

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode(encoding="utf-8")

    async with async_session() as session:
        user = UserModel(username=_username, password_hash=password_hash)

        async with session.begin():
            session.add(user)
            await session.commit()

        await session.refresh(user)
        await session.close()

        return User(id=user.id, username=user.username)


async def authorise(_username: str, _password: str) -> UserAuthenticated:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).where(UserModel.username == _username)
            result = await session.execute(stmt)

            user = result.scalars().first()

            if user:
                password = _password.encode("utf-8")
                password_hash = user.password_hash.encode("utf-8")

                password_match = bcrypt.checkpw(password, password_hash)

                if password_match:
                    return UserAuthenticated(
                        id=user.id, username=user.username, enabled=user.enabled
                    )

            return UserAuthenticated(enabled=False)


async def find_user_details(offset=0) -> list[UserDetails]:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserDetailsModel).limit(25).offset(offset)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def find_user_details_by_user_id(user_id: int, offset=0) -> UserDetails:
    async with async_session() as session:
        async with session.begin():
            stmt = (
                select(UserDetailsModel)
                .where(UserDetailsModel.user_id == user_id)
                .limit(25)
                .offset(offset)
            )
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().first()


async def add_user_details(
    _user_id: int, _first_name: str, _last_name: str
) -> JSONResponse | UserDetails:
    async with async_session() as session:
        user_details = UserDetailsModel(
            user_id=_user_id, first_name=_first_name, last_name=_last_name
        )

        async with session.begin():
            session.add(user_details)
            await session.commit()

        await session.refresh(user_details)
        await session.close()

        return UserDetails(
            id=user_details.id,
            user_id=user_details.id,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
        )

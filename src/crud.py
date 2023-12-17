import logging
import bcrypt

from sqlalchemy import select
from starlette.responses import JSONResponse

from .config import SERVICE_NAME
from .schemas import User, UserAuthenticated
from .database import async_session
from .models import UserModel

LOGGER = logging.getLogger(SERVICE_NAME)


async def find_users(offset=0) -> list[User]:
    async with async_session() as session:
        async with session.begin():
            stmt = select(UserModel).limit(25).offset(offset)
            result = await session.execute(stmt)
            await session.close()

            return result.scalars().all()


async def find_by_username(username: str) -> User:
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
            stmt = select(UserModel).where(
                UserModel.username == _username
            )
            result = await session.execute(stmt)

            user = result.scalars().first()
            # print(f"*** crud authorise user: {user.enabled}")

            if user:
                password = _password.encode("utf-8")
                password_hash = user.password_hash.encode("utf-8")

                password_match = bcrypt.checkpw(password, password_hash)
                print(f"*** crud authorise password_match: {password_match}")

                if password_match:
                    LOGGER.info(f"*** crud authorise password_match: {password_match}")

                    return UserAuthenticated(
                        id=user.id, username=user.username, enabled=user.enabled
                    )

            LOGGER.info(f"*** crud authorise FALSE")

            return UserAuthenticated()


# async def get_user_details(db: AsyncSession):
#     async with database.async_session() as db:
#         async with db.begin():
#             stmt = select(
#                 models.UserDetails.id,
#                 models.UserDetails.user_id,
#                 models.UserDetails.first_name,
#                 models.UserDetails.last_name,
#             )
#
#             result = await db.execute(stmt)
#
#             await db.close()
#
#             return result

import datetime

from ..config import JWT_TOKEN_EXPIRY_SECONDS


def create_token_expiry() -> datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        seconds=JWT_TOKEN_EXPIRY_SECONDS
    )

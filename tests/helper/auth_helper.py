import datetime

from src.config import JWT_TOKEN_EXPIRY_SECONDS


def create_token_expiry(_seconds=JWT_TOKEN_EXPIRY_SECONDS) -> datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        seconds=_seconds
    )

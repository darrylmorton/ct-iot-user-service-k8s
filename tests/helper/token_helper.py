from datetime import datetime, timedelta, timezone
from jose import jwt

import tests.config as test_config


def create_token_expiry(_seconds=test_config.JWT_TOKEN_EXPIRY_SECONDS) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=_seconds)


def create_token(data: dict, token_expiry: datetime = create_token_expiry()):
    to_encode = data.copy()

    to_encode.update({"exp": token_expiry})
    encoded_jwt = jwt.encode(to_encode, test_config.JWT_SECRET, algorithm="HS256")

    return encoded_jwt

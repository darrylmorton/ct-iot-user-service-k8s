import json


def create_user_payload(_username: str, _password: str):
    return json.dumps({"username": _username, "password": _password})

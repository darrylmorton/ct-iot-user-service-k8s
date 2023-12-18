import json


def create_user_payload(_username="foo@home.com", _password="barbarba", _enabled=False):
    if _enabled:
        return json.dumps({"username": _username, "password": _password, "enabled": _enabled})
    else:
        return json.dumps({"username": _username, "password": _password})

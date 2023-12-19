import json


# def create_test_user(
#     _username="foo@home.com",
#     _password="barbarba",
#     _enabled=False,
#     _first_name="Foo",
#     _last_name="Bar",
# ):
#     if _enabled:
#         return {
#             "username": _username,
#             "password": _password,
#             "enabled": _enabled,
#             "first_name": _first_name,
#             "last_name": _last_name,
#         }
#     else:
#         return {
#             "username": _username,
#             "password": _password,
#             "first_name": _first_name,
#             "last_name": _last_name,
#         }

def create_signup_payload(
    _username="foo@home.com",
    _password="barbarba",
    _enabled=False,
    _first_name="Foo",
    _last_name="Bar",
):
    if _enabled:
        return {
            "username": _username,
            "password": _password,
            "enabled": _enabled,
            "first_name": _first_name,
            "last_name": _last_name,
        }
    else:
        return {
            "username": _username,
            "password": _password,
            "first_name": _first_name,
            "last_name": _last_name,
        }

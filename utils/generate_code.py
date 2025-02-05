import time
from steampy.guard import generate_one_time_code


def generate_auth_code():
    print(time.time())
    print(generate_one_time_code(
        "DxRC7aka9y06OOyujTHhGdZC6NM/5NQw=", int(time.time())))


generate_auth_code()

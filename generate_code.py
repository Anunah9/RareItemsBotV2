import time
from steampy.guard import generate_one_time_code


def generate_auth_code():
    print(time.time())
    print(generate_one_time_code("HJXEBEq1x7L7EzFjFFUHrJ/5NQw=", int(time.time())))


generate_auth_code()

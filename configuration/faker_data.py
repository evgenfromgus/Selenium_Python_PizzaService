import time

from faker import Faker

fake = Faker()


class FakerData:
    username = fake.name().replace(" ", "")[:7]
    email = f"{username}@{int(time.time())}.com"[:20]
    password = fake.password()[:20]

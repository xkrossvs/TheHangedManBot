from datetime import datetime
from typing import TypedDict
from dotenv import load_dotenv
import os

import pymongo
from pymongo.collection import Collection

load_dotenv()

TEST = 0

MONGO_URL = os.getenv('MONGO_URL')
cluster = pymongo.MongoClient(MONGO_URL)

if TEST:
    TOKEN = os.getenv('TEST_TOKEN')
    users: Collection = cluster.the_hanged_man.users_test
    hangs: Collection = cluster.the_hanged_man.hangs_test
else:
    TOKEN = os.getenv('TOKEN')
    users: Collection = cluster.the_hanged_man.users
    hangs: Collection = cluster.the_hanged_man.hangs

LOG_GROUP_ID = -1002324422338
ADMINS = [618805465, 241322552]


class StatesData(TypedDict):
    word: str
    chat_id: int
    text_word: list
    hang_state: int
    wrong_letters: list
    message_id: int
    theme: str
    start_time: datetime

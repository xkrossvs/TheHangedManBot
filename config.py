from datetime import datetime
from typing import TypedDict

import pymongo
from pymongo.collection import Collection

TOKEN = '7441827338:AAHJPp1FieBS8oAL6HDmveneZzOJPjX2rVY'
MONGO_URL = 'mongodb+srv://ivankblintsov:0FDeYNh9HDqBEsQJ@cluster.6pua1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster'
cluster = pymongo.MongoClient(MONGO_URL)
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

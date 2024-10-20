from typing import TypedDict

import pymongo
from pymongo.collection import Collection

TOKEN = '7441827338:AAHJPp1FieBS8oAL6HDmveneZzOJPjX2rVY'
MONGO_URL = 'mongodb+srv://ivankblintsov:0FDeYNh9HDqBEsQJ@cluster.6pua1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster'
cluster = pymongo.MongoClient(MONGO_URL)
users: Collection = cluster.the_hanged_man.users


class StatesData(TypedDict):
    word: str
    chat_id: int
    text_word: list
    hang_state: int
    wrong_letters: str
    message_id: int

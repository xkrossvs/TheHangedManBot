from config import users


users.update_many(filter={},
                  update={'$set': {'min_time': None}})

from config import users


class MongoUnits:

    @staticmethod
    def wl_and_mws_update(user_id: int | str) -> None:
        """Изменяет КД и макс. винстрик в базе данных."""
        info = users.find_one({'user_id': user_id})

        if info['losses'] != 0:
            wl = round(info['wins'] / info['losses'], 2)
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'WL': wl if wl != int(wl) else int(wl)}})

        if info['max_win_streak'] < info['win_streak']:
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'max_win_streak': info['win_streak']}})

    @staticmethod
    def win_count_increase(user_id: int | str) -> None:
        users.update_one(filter={'user_id': user_id},
                         update={'$inc': {'wins': 1, 'win_streak': 1}})

    @staticmethod
    def lose_count_increase(user_id: int | str) -> None:
        users.update_one(filter={'user_id': user_id},
                         update={'$inc': {'losses': 1},
                                 '$set': {'win_streak': 0}})

    @staticmethod
    def wl_negative_update(user_id: int | str) -> None:
        """Изменяет КД в негативную сторону."""
        info = users.find_one({'user_id': user_id})

        wl = round(info['wins'] / info['losses'], 2)
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {'WL': wl if wl != int(wl) else int(wl)}})
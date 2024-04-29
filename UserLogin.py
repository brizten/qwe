class UserLogin():
    def fromDb(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_auth(self):
        return  True

    def is_active(self):
        return True

    def is_anon(self):
        return True

    def get_id(self):
        return str(self.__user['id'])
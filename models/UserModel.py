import datetime
import json

class User:
    def __init__(self, name, email, password, avatar, created=datetime.datetime.utcnow()):
        self.name = name
        self.email = email
        self.password = password
        self.avatar = avatar
        self.created = created
    
    def get_dict(self):
        user_dict = {
            "name" : self.name,
            "email" : self.email,
            "password" : self.password,
            "avatar" : self.avatar,
            "created" : self.created
        }

        return user_dict
    
    def get_json(self):
        return json.dump(self.get_dict(), indent=4)
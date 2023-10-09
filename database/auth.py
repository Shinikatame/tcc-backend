from json import load, dump

from models.user import UserCreate

class AuthModel:
    def __init__(self):
        self.data: [UserCreate] = self.get_data()
    
    def create(self, user: UserCreate):
        self.write_data(user)
    
    def get_data(self) -> [UserCreate]:
        with open('data.json', 'r', encoding = 'UTF-8') as file:
            return load(file)
        
    def write_data(self, user: UserCreate):
        with open('data.json', 'w+', encoding = 'UTF-8') as file:
            self.data.append(user.dict())
            dump(self.data, file, indent = 4)


auth = AuthModel()
import json


USERS_DATA_FILE_PATH = "./users_data.json"


class User:
    def __init__(self, user_id, user_name, date_stamp, language_code):
        
        # user settings
        self.id = user_id
        self.name = user_name
        self.date_stamp = date_stamp
        self.language_code = language_code
        
        # lifecell user settings
        self.tariff_name = None
        self.tariff_price = None #  UAH
        self.internet_left = 0 # megabytes
        self.minutes_left = 0
        self.sms_left = 0
    
    def update_user(self, user_id=None, user_name=None, language_code=None):
        self.id = user_id
        self.user_name = user_name
        self.language_code = language_code

class Database:
    def __init__(self, data_path):
        self.data_path = data_path
        
        with open(data_path, 'r+') as file:
            file_content = file.read()
            if len(file_content) == 0 or file_content.isspace():
                self.data = {}
                file.write(json.dumps(self.data))
            else:
                self.data = json.loads(file_content)
    
    def UpdateUserData(self, user: User):
        print(self.data[user.id])
    
    def IsNewbie(self, user_id):
        if user_id in self.data:
            return False
        
        return True

if __name__ == "__main__":
    db = Database(USERS_DATA_FILE_PATH)
    
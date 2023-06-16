import json


USERS_DATA_FILE_PATH = "./users_data.json"


class User:
    def __init__(self, user_id, user_name, date_stamp, language_code, tariff_name=None, tariff_price=None, internet_left=0, minutes_left=0, sms_left=0):
        
        # user settings
        self.id = str(user_id)
        self.name = user_name
        self.date_stamp = date_stamp
        self.language_code = language_code
        
        # lifecell user settings
        self.tariff_name = tariff_name
        self.tariff_price = tariff_price #  UAH
        self.internet_left = internet_left # megabytes
        self.minutes_left = minutes_left
        self.sms_left = sms_left

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
    
    def Update(self):
        
        with open(self.data_path, "w+") as file:
            json.dump(self.data, file)
    
    def IsNewbie(self, user_id):
        if str(user_id) in self.data:
            return False
        
        return True
    
    def UpdateUser(self, user):                
        self.data[user.id] = {"name":user.name,
                              "date_stamp":user.date_stamp,
                              "language_code":user.language_code,
                              "tariff_name":user.tariff_name,
                              "tariff_price":user.tariff_price,
                              "internet_left":user.internet_left,
                              "minutes_left":user.minutes_left,
                              "sms_left":user.sms_left}
        self.Update()
    
    def LoadUser(self, user_id):
        user_data = self.data[str(user_id)]
        
        return User(user_id,
                    user_data["name"],
                    user_data["date_stamp"],
                    user_data["language_code"],
                    user_data["tariff_name"],
                    user_data["tariff_price"],
                    user_data["internet_left"],
                    user_data["minutes_left"],
                    user_data["sms_left"])

class Customer:
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email
        self.package_id = "UNKNOWN" # default package id is unknown, Package sets id

    def set_package_id(self, id:int): # set package id
        if type(id) != int:
            raise ValueError("Id must be an integer!")
        self.package_id = id
# Класс который описывает таблицу OWNER_DETAILS
class OwnerDetails:
    def __init__(self, owner_lastname, owner_name, owner_patronymic, owner_phone, owner_email, id = None):
        self.id = id
        self.owner_lastname = owner_lastname
        self.owner_name = owner_name
        self.owner_patronymic = owner_patronymic
        self.owner_phone = owner_phone
        self.owner_email = owner_email
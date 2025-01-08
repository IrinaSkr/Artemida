# Класс который описывает таблицу PET_LIST
class PetList:
    def __init__(self, owner_id, pet_name, owner_fio, id = None):
        self.id = id
        self.owner_id = owner_id
        self.pet_name = pet_name
        self.owner_fio = owner_fio
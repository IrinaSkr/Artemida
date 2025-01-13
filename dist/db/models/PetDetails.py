# Класс который описывает таблицу PET_DETAILS
class PetDetails:
    def __init__(self, owner_id, pet_name, pet_type, pet_sex, pet_birthday, pet_age,
                 pet_breed, pet_color, pet_weight, pet_features, pet_visit = None, visit_id = None, id = None):
        self.id = id
        self.owner_id = owner_id
        self.pet_name = pet_name
        self.pet_type = pet_type
        self.pet_sex = pet_sex
        self.pet_birthday = pet_birthday
        self.pet_age = pet_age
        self.pet_breed = pet_breed
        self.pet_color = pet_color
        self.pet_weight = pet_weight
        self.pet_features = pet_features
        self.pet_visit = pet_visit
        self.visit_id = visit_id

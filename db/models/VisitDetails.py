# Класс который описывает таблицу VISIT_DETAILS
class VisitDetails:
    def __init__(self, pet_visit, pet_complaints, pet_diagnosis, pet_analyses, pet_treatment, id = None):
        self.id = id
        self.pet_visit = pet_visit
        self.pet_complaints = pet_complaints
        self.pet_diagnosis = pet_diagnosis
        self.pet_analyses = pet_analyses
        self.pet_treatment = pet_treatment

from faker import Faker
from medicine import diagnosis, treatment, test_result, profession, gender
import random

class CustomFaker(Faker):
    def __init__(self, lan:str, consistency:int):
        super().__init__(lan)
        super().seed_instance(consistency)  # Set data consistency

    def diagnosis(self):
        return random.choice(diagnosis())
    
    def treatment(self):
        return random.choice(treatment())
    
    def test_result(self):
        return random.choice(test_result())
    
    def profession(self):
        return random.choice(profession())
    
    def gender(self):
        return random.choice(gender())
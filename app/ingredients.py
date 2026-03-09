from enum import StrEnum


class IngredientType(StrEnum):
    MEAT = "Meat"
    BRAN = "Bran"
    FISH = "Fish"
    FRUIT = "Fruit"
    VEGGIE = "Veggie"
    DAIRY = "Dairy"
    DRINK = "Drink"


class Ingredient:
    def __init__(self, name: str, chef_number_id: int, ingredient_type_id: IngredientType):
        self.name = name
        self.chef_number_attr = int(chef_number_id)
        self.ingredient_type_attr = ingredient_type_id

    def is_of_type(self, ingredient_type_to_check: IngredientType):
        return self.ingredient_type_attr == ingredient_type_to_check

    def is_at_chef_number(self, chef_number_to_check: int):
        return self.chef_number_attr == chef_number_to_check

    def __str__(self):
        return f"{self.name} : {self.ingredient_type_attr}, {self.chef_number_attr}"

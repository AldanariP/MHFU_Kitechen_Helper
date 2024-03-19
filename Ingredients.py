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
    def __init__(self, name: str, chefNumber: int, ingredientType: IngredientType):
        self.name: str = name
        self.chefNumber: int = int(chefNumber)
        self.ingredientType: IngredientType = ingredientType

    def isOfType(self, ingredientType: IngredientType):
        return self.ingredientType == ingredientType

    def isAtChefNumber(self, chefNumber: int):
        return self.chefNumber == chefNumber

    def __str__(self):
        return f"{self.name} : {self.ingredientType}, {self.chefNumber}"

import json

from Bonus import *
from Ingredients import *


class Model:

    def __init__(self):
        self.ingredientList: list[Ingredient] = []
        self.bonusList: list[Bonus] = []

    def getBonus(self, chefNumber: int,
                 ingredientList: list[IngredientType],
                 orderBy: BuffType = None,
                 showNoEffect: bool = False) -> list[Bonus]:

        resultBonuses = [bonus for bonus in self.bonusList
                         if bonus.chefNumber == chefNumber and bonus.isCookableWith(ingredientList)]

        if not showNoEffect:  # if show effect is True -> filter No Effect
            resultBonuses = [bonus for bonus in resultBonuses if not bonus.isOfBuffType(BuffType.NOEFFECT)]

        if orderBy is not None:
            for bonus in resultBonuses:
                bonus.setComparator(orderBy)  # because the bonus need to know the type of the comparison in the __lt__
            resultBonuses.sort(key=lambda bonus: (bonus.isOfBuffType(orderBy), bonus))

        resultBonuses.reverse()  # because it's somehow displayed in the wrong way

        return resultBonuses

    def getIngredients(self, chefNumber: int) -> dict[str, list[str]]:  # pretty clear rigth ?
        return {ingredientType: [ingredient.name for ingredient in self.ingredientList
                                 if ingredient.isAtChefNumber(chefNumber)
                                 and ingredient.isOfType(IngredientType(ingredientType))]
                for ingredientType in IngredientType}

    def ingredientTypeOf(self, name: str) -> IngredientType:
        return next(ingredient.ingredientType for ingredient in self.ingredientList
                    if ingredient.name == name)

    def loadIngredientFrom(self, path) -> bool:  # Python is readable they say...
        with open(path, "r") as file:
            data = json.load(file)
            for chefNumber in data:
                for ingredientType in data[chefNumber]:
                    if ingredientType in IngredientType:
                        # Ingredient
                        for ingredientName in data[chefNumber][ingredientType]:
                            self.ingredientList.append(Ingredient(ingredientName, chefNumber, ingredientType))
                    else:
                        # Bonuses
                        for ingr1Bonnus in data[chefNumber]['Bonus']:
                            for ingr2Bonnus in data[chefNumber]['Bonus'][ingr1Bonnus]:
                                self.bonusList.append(
                                    Bonus(chefNumber,
                                          ingr1Bonnus,
                                          ingr2Bonnus,
                                          data[chefNumber]['Bonus'][ingr1Bonnus][ingr2Bonnus]))
        return True

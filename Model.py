import json
from Bonus import *
from Ingredients import *


class Model:

    def __init__(self):
        self.ingredientList: list[Ingredient] = []
        self.bonusList: list[Bonus] = []

    def getBonus(self, chefNumber: int, orderBy: BuffType = None, showNoEffect: bool = False) -> list[Bonus]:
        resultBonuses = [x for x in self.bonusList if x.chefNumber == chefNumber]

        if not showNoEffect:  # if show effect is True -> filter No Effect
            resultBonuses = [x for x in resultBonuses if not x.isOfBuffType(BuffType.NOEFFECT)]

        if orderBy is not None:
            resultBonuses.sort(key=lambda bonus: (bonus.isOfBuffType(orderBy), bonus))

        resultBonuses.reverse()  # because somehow displayed in the wrong way

        return resultBonuses

    def loadIngredientFrom(self, path):  # Python is readable they say...
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
                                self.bonusList.append(Bonus(chefNumber, ingr1Bonnus, ingr2Bonnus,
                                                            data[chefNumber]['Bonus'][ingr1Bonnus][ingr2Bonnus]))

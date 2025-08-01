from app.bonus import *
from app.ingredients import *


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
            resultBonuses.sort(key=lambda bonus: bonus.get_score(orderBy))

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

    def loadIngredientFrom(self, data) -> bool:  # Python is readable they say...
        for chefNumber in data:
            chef_number_data = data[chefNumber]
            for ingredientType in chef_number_data:
                if ingredientType in IngredientType:
                    # Ingredient
                    for ingredientName in chef_number_data[ingredientType]:
                        self.ingredientList.append(Ingredient(ingredientName, chefNumber, ingredientType))
                else:
                    # Bonuses
                    bonus = chef_number_data['Bonus']
                    for ingr1Bonnus in bonus:
                        for ingr2Bonnus in bonus[ingr1Bonnus]:
                            self.bonusList.append(Bonus(chefNumber, ingr1Bonnus, ingr2Bonnus, bonus[ingr1Bonnus][ingr2Bonnus]))
        return True

from app.ingredients import *


class BuffType(StrEnum):
    NOEFFECT = "No Effect"
    DEFENSE = "Defense"
    ELEMENTALRES = "Elemental Res"
    ATTACK = "Attack"
    STAMINA = "Stamina"
    HEALTH = "Health"


def bonusFromString(string: str):  # kinda stupid but it works
    return {
        "No Effect": BuffType.NOEFFECT,
        "Defense": BuffType.DEFENSE,
        "Elemental Res": BuffType.ELEMENTALRES,
        "Attack": BuffType.ATTACK,
        "Stamina": BuffType.STAMINA,
        "Health": BuffType.HEALTH
    }.get(string)


class Bonus:
    buffKeyMap = {
        "Health": BuffType.HEALTH,
        "Stamina": BuffType.STAMINA,
        "Attack": BuffType.ATTACK,
        "Res": BuffType.ELEMENTALRES,
        "Defense": BuffType.DEFENSE,
        "No": BuffType.NOEFFECT
    }

    def __init__(self, chefNumber: int, ingredient1: IngredientType, ingredient2: IngredientType, effect: str):
        self.chefNumber: int = int(chefNumber)
        self.ingredient1 = ingredient1
        self.ingredient2 = ingredient2
        self.effect: str = effect
        self.sortedBy = None
        # parse buff type
        if '&' in self.effect:
            buff1, buff2 = effect.split("&")
            self.buffType1 = next((value for key, value in Bonus.buffKeyMap.items() if key in buff1), None)
            self.buffType2 = next((value for key, value in Bonus.buffKeyMap.items() if key in buff2), None)
        else:
            self.buffType1 = next((value for key, value in Bonus.buffKeyMap.items() if key in effect), None)

        # parse buff value
        match self.buffType1:
            case BuffType.NOEFFECT:
                self.buffValue1 = 0
            case BuffType.ATTACK:
                self.buffValue1 = 30 if "Small" in self.effect else 50
            case BuffType.ELEMENTALRES:
                self.buffValue1 = int(self.effect[-1])
            case _:  # HEALTH, STAMINA, DEFENSE
                self.buffValue1 = int(self.effect[0:3])

        if self.hasDoubleEffect():
            match self.buffType2:
                case BuffType.NOEFFECT:
                    self.buffValue2 = 0
                case BuffType.ATTACK:
                    self.buffValue2 = 30 if "Small" in self.effect else 50
                case BuffType.ELEMENTALRES:
                    self.buffValue2 = int(self.effect[-1])
                case _:
                    self.buffValue2 = int(self.effect.split("& ")[1][0:3])

        if self.buffType1 is None or (self.hasDoubleEffect() and self.buffType2 is None):
            raise ValueError(f"Failed to Parse the effect : '{effect}'")

    def hasDoubleEffect(self):
        return hasattr(self, "buffType2")

    def isOfBuffType(self, buffType: BuffType) -> bool:
        return self.buffType1 == buffType or (self.hasDoubleEffect() and self.buffType2 == buffType)

    def valueOfBuffType(self, buffType: BuffType) -> int:
        if not self.isOfBuffType(buffType):
            raise ValueError(f"Can't retreive BuffValue for Bonus : {buffType} in {self.effect}")
        if self.hasDoubleEffect():
            return self.buffValue1 if self.buffType1 == buffType else self.buffValue2
        else:
            # not the intended way of using this function
            # but since the condition is evaluated anyway if we return or raise ValueError, migth as well return
            return self.buffValue1

    def totalValue(self) -> int:
        return self.buffValue1 + (self.buffValue2 if self.hasDoubleEffect() else 0)

    def setComparator(self, buffType: BuffType):
        self.sortedBy = buffType

    def isAvailableForChefNumber(self, chefNumber: int) -> bool:
        return self.chefNumber == chefNumber

    def toDisplayList(self) -> tuple[str, str, str]:
        return self.ingredient1, self.ingredient2, self.effect

    def isCookableWith(self, ingredientList: list[IngredientType]) -> bool:
        if self.ingredient1 == self.ingredient2:
            return ingredientList.count(self.ingredient1) >= 2
        else:
            return self.ingredient1 in ingredientList and self.ingredient2 in ingredientList

    def __str__(self):
        return (f"{self.chefNumber} : {self.ingredient1} + {self.ingredient2} => {self.effect} ({self.buffType1}"
                + (f", {self.buffType2})" if self.hasDoubleEffect() else ')'))

    def __eq__(self, other):
        if not isinstance(other, Bonus):
            return False
        return (self.chefNumber == other.chefNumber
                and {self.ingredient1, self.ingredient2} == {other.ingredient1, other.ingredient2})

    def __lt__(self, other) -> bool:
        if not isinstance(other, Bonus):
            return False
        if self.hasDoubleEffect() or self.hasDoubleEffect():

            if self.isOfBuffType(self.sortedBy) and other.isOfBuffType(self.sortedBy):  # 1 1
                return self.valueOfBuffType(self.sortedBy) < other.valueOfBuffType(self.sortedBy)

            elif self.isOfBuffType(self.sortedBy):                                      # 1 0
                return self.valueOfBuffType(self.sortedBy) < other.buffValue1

            elif other.isOfBuffType(self.sortedBy):                                     # 0 1
                return self.buffValue1 < other.valueOfBuffType(self.sortedBy)

            else:                                                                       # 0 0
                return self.totalValue() < other.totalValue()
        else:
            return self.buffValue1 < other.buffValue1

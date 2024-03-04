from Ingredients import *


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
        self.ingredient1: IngredientType = ingredient1
        self.ingredient2: IngredientType = ingredient2
        self.effect: str = effect
        # parse buff type
        try:
            buff1, buff2 = effect.split("&")
            self.buffType1: BuffType = next((value for key, value in Bonus.buffKeyMap.items() if key in buff1), None)
            self.buffType2: BuffType = next((value for key, value in Bonus.buffKeyMap.items() if key in buff2), None)
        except ValueError:
            self.buffType1: BuffType = next((value for key, value in Bonus.buffKeyMap.items() if key in effect), None)

        if self.buffType1 is None or (hasattr(self, 'buffType2') and self.buffType2 is None):
            raise ValueError(f"Failed to Parse the effect : '{effect}'")

    def isOfBuffType(self, buffType: BuffType) -> bool:
        return self.buffType1 == buffType or (hasattr(self, 'buffType2') and self.buffType2 == buffType)

    def isAvailableForChefNumber(self, chefNumber: int) -> bool:
        return self.chefNumber == chefNumber

    def toDisplayList(self) -> tuple[str, str, str]:
        return self.ingredient1, self.ingredient2, self.effect

    def __str__(self):
        return (f"{self.chefNumber} : {self.ingredient1} + {self.ingredient2} => {self.effect} ({self.buffType1}"
                + (f", {self.buffType2})" if hasattr(self, 'buffType2') else ')'))

    def __eq__(self, other):
        if not isinstance(other, Bonus):
            return False
        return (self.chefNumber == other.chefNumber
                and {self.ingredient1, self.ingredient2} == {other.ingredient1, other.ingredient2})

    def __lt__(self, other):
        if not isinstance(other, Bonus):
            return False
        if self.isOfBuffType(BuffType.NOEFFECT):  # no effect has always less value
            return True
        if self.isOfBuffType(BuffType.ATTACK):  # there are no negative attack buff, compared with by small < large
            return "Small" in self.effect and "Large" in other.effect
        else:
            if self.effect[0] == other.effect[0]:  # if they are both positive or both negative
                if self.effect.startswith("+"):  # positive are sorted from best to better
                    return self.effect < other.effect  # TODO fix sorting double effect
                else:  # negative are sorted from worse to worser
                    return self.effect > other.effect
            else:  # negative buff has less value than a positive buff
                return "-" in self.effect and "+" in other.effect

from enum import StrEnum
from app.ingredients import IngredientType


class BuffType(StrEnum):
    NOEFFECT = "No Effect"
    DEFENSE = "Defense"
    ELEMENTALRES = "Elemental Res"
    ATTACK = "Attack"
    STAMINA = "Stamina"
    HEALTH = "Health"


def bonus_from_string(string: str):  # kinda stupid but it works
    return {
        "No Effect": BuffType.NOEFFECT,
        "Defense": BuffType.DEFENSE,
        "Elemental Res": BuffType.ELEMENTALRES,
        "Attack": BuffType.ATTACK,
        "Stamina": BuffType.STAMINA,
        "Health": BuffType.HEALTH,
    }.get(string)


class Bonus:
    buff_key_map = {
        "Health": BuffType.HEALTH,
        "Stamina": BuffType.STAMINA,
        "Attack": BuffType.ATTACK,
        "Res": BuffType.ELEMENTALRES,
        "Defense": BuffType.DEFENSE,
        "No": BuffType.NOEFFECT,
    }

    def __init__(
        self,
        chef_number: int,
        ingredient1: IngredientType,
        ingredient2: IngredientType,
        effect: str,
    ):
        self.chef_number: int = int(chef_number)
        self.ingredient1 = ingredient1
        self.ingredient2 = ingredient2
        self.effect: str = effect
        self.sorted_by_type = None
        # parse buff type
        if "&" in self.effect:
            buff1, buff2 = effect.split("&")
            self.buff_type_1 = next(
                (value for key, value in Bonus.buff_key_map.items() if key in buff1), None
            )
            self.buff_type_2 = next(
                (value for key, value in Bonus.buff_key_map.items() if key in buff2), None
            )
        else:
            self.buff_type_1 = next(
                (value for key, value in Bonus.buff_key_map.items() if key in effect),
                None,
            )

        # parse buff value
        match self.buff_type_1:
            case BuffType.NOEFFECT:
                self.buff_value_1 = 0
            case BuffType.ATTACK:
                self.buff_value_1 = 30 if "Small" in self.effect else 50
            case BuffType.ELEMENTALRES:
                self.buff_value_1 = int(self.effect[-1])
            case _:  # HEALTH, STAMINA, DEFENSE
                self.buff_value_1 = int(self.effect[:3])

        if self.has_double_effect():
            match self.buff_type_2:
                case BuffType.NOEFFECT:
                    self.buff_value_2 = 0
                case BuffType.ATTACK:
                    self.buff_value_2 = 30 if "Small" in self.effect else 50
                case BuffType.ELEMENTALRES:
                    self.buff_value_2 = int(self.effect[-1])
                case _:
                    self.buff_value_2 = int(
                        self.effect[self.effect.find("&") + 1 :].lstrip()[:3]
                    )

    def has_double_effect(self):
        return hasattr(self, "buff_type_2")

    def is_of_buff_type(self, buff_type: BuffType) -> bool:
        return self.buff_type_1 == buff_type or (
                self.has_double_effect() and self.buff_type_2 == buff_type
        )

    def is_available_for_chef_number(self, chef_number: int) -> bool:
        return self.chef_number == chef_number

    def is_negative(self):
        return self.buff_value_1 < 0

    def to_display_list(self) -> tuple[str, str, str]:
        return self.ingredient1, self.ingredient2, self.effect

    def is_cookable_with(self, ingredient_list: list[IngredientType]) -> bool:
        if self.ingredient1 == self.ingredient2:
            return ingredient_list.count(self.ingredient1) >= 2
        else:
            return (
                    self.ingredient1 in ingredient_list
                    and self.ingredient2 in ingredient_list
            )

    def get_score(self, buff_type: BuffType) -> int:
        if self.is_negative():
            return -1
        elif self.buff_type_1 == buff_type:
            return self.buff_value_1 * 10 + (
                self.buff_value_2 if self.has_double_effect() else 0
            )
        elif self.has_double_effect() and self.buff_type_2 == buff_type:
            return self.buff_value_2 * 10 + self.buff_value_1
        else:
            return self.buff_value_1 + (self.buff_value_2 if self.has_double_effect() else 0)

    def __str__(self):
        return (
            f"{self.chef_number} : {self.ingredient1} + {self.ingredient2} => {self.effect} ({self.buff_type_1}"
            + (f", {self.buff_type_2})" if self.has_double_effect() else ")")
        )

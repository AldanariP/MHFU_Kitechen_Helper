from app.bonus import BuffType, Bonus
from app.ingredients import Ingredient, IngredientType


class Model:
    def __init__(self):
        self.ingredient_list: list[Ingredient] = []
        self.bonus_list: list[Bonus] = []

    def get_bonus(
        self,
        chef_number: int,
        ingredient_list: list[IngredientType],
        order_by: BuffType | None = None,
        show_no_effect: bool = False,
        show_negative_bonuses: bool = False,
    ) -> list[Bonus]:

        result_bonuses = [
            bonus
            for bonus in self.bonus_list
            if bonus.chef_number == chef_number and bonus.is_cookable_with(ingredient_list)
        ]

        if not show_no_effect:  # if show effect is True -> filter No Effect
            result_bonuses = [
                bonus
                for bonus in result_bonuses
                if not bonus.is_of_buff_type(BuffType.NOEFFECT)
            ]

        if not show_negative_bonuses:
            result_bonuses = [
                bonus for bonus in result_bonuses if not bonus.is_negative()
            ]

        if order_by is not None:
            result_bonuses.sort(key=lambda bonus: bonus.get_score(order_by))

        result_bonuses.reverse()  # because it's somehow displayed in the wrong way

        return result_bonuses

    def get_ingredients(
        self, chef_number: int
    ) -> dict[str, list[str]]:  # pretty clear rigth ?
        return {
            ingredient_type: [
                ingredient.name
                for ingredient in self.ingredient_list
                if ingredient.is_at_chef_number(chef_number)
                and ingredient.is_of_type(IngredientType(ingredient_type))
            ]
            for ingredient_type in IngredientType
        }

    def ingredient_type_of(self, name: str) -> IngredientType:
        return next(
            ingredient.ingredient_type_attr
            for ingredient in self.ingredient_list
            if ingredient.name == name
        )

    def load_ingredient_from(self, data) -> bool:  # Python is readable they say...
        for chef_number_key in data:
            chef_number_data = data[chef_number_key]
            for ingredient_type in chef_number_data:
                if ingredient_type in IngredientType:
                    # Ingredient
                    for ingredient_name in chef_number_data[ingredient_type]:
                        self.ingredient_list.append(
                            Ingredient(ingredient_name, chef_number_key, ingredient_type)
                        )
                else:
                    # Bonuses
                    bonus_data = chef_number_data["Bonus"]
                    for ingr1_bonus in bonus_data:
                        for ingr2_bonus in bonus_data[ingr1_bonus]:
                            self.bonus_list.append(
                                Bonus(
                                    chef_number_key,
                                    ingr1_bonus,
                                    ingr2_bonus,
                                    bonus_data[ingr1_bonus][ingr2_bonus],
                                )
                            )
        return True

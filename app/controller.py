from customtkinter import CTkCheckBox

from app.bonus import bonus_from_string
from app.ingredients import IngredientType
from app.model import Model


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def reset_check_box_field(self, view):
        for child in view.check_box_field.winfo_children():
            if isinstance(child, CTkCheckBox):
                child.deselect()
        self.display_bonuses(view)

    def get_checked_ingredient(self, view) -> list[IngredientType]:
        return [
            self.model.ingredient_type_of(chkBox.cget("text"))
            for chkBox in view.check_box_field.winfo_children()
            if isinstance(chkBox, CTkCheckBox) and chkBox.get() == 1
        ]

    def display_bonuses(self, view):
        bonuses = self.model.get_bonus(
            chef_number=view.chef_number_var.get(),
            ingredient_list=self.get_checked_ingredient(view),
            order_by=bonus_from_string(view.sort_by_var.get()),
            show_no_effect=view.no_effect_var.get(),
            show_negative_bonuses=view.negative_bonuses_var.get(),
        )
        view.display_bonuses([bonus.to_display_list() for bonus in bonuses])

    def get_check_box_data(self, view):
        view.draw_check_box_field(
            self.model.get_ingredients(view.chef_number_var.get())
        )

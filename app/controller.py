from customtkinter import CTkCheckBox

from app.bonus import bonus_from_string
from app.ingredients import IngredientType
from app.model import Model
from app.view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def reset_check_box_field(self):
        for child in self.view.check_box_field.winfo_children():
            if isinstance(child, CTkCheckBox):
                child.deselect()
        self.display_bonuses()

    def get_checked_ingredient(self) -> list[IngredientType]:
        return [
            self.model.ingredient_type_of(chkBox.cget("text"))
            for chkBox in self.view.check_box_field.winfo_children()
            if isinstance(chkBox, CTkCheckBox) and chkBox.get() == 1
        ]

    def display_bonuses(self):
        bonuses = self.model.get_bonus(
            chef_number=self.view.chef_number_var.get(),
            ingredient_list=self.get_checked_ingredient(),
            order_by=bonus_from_string(self.view.sort_by_var.get()),
            show_no_effect=self.view.no_effect_var.get(),
            show_negative_bonuses=self.view.negative_bonuses_var.get(),
        )
        self.view.display_bonuses([bonus.to_display_list() for bonus in bonuses])

    def get_check_box_data(self):
        self.view.draw_check_box_field(
            self.model.get_ingredients(self.view.chef_number_var.get())
        )

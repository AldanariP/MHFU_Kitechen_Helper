import customtkinter as ctk

from Bonus import bonusFromString
from Ingredients import IngredientType
from Model import Model
from View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model: Model = model
        self.view: View = view

    def resetCheckBoxField(self):
        for child in self.view.checkBoxField.winfo_children():
            if isinstance(child, ctk.CTkCheckBox):
                child.deselect()
        self.displayBonuses()

    def getCheckedIngredient(self) -> list[IngredientType]:
        return [self.model.ingredientTypeOf(chkBox.cget('text'))
                for chkBox in self.view.checkBoxField.winfo_children()
                if isinstance(chkBox, ctk.CTkCheckBox) and chkBox.get() == 1]

    def displayBonuses(self):
        bonuses = self.model.getBonus(chefNumber=self.view.chefNumber.get(),
                                      ingredientList=self.getCheckedIngredient(),
                                      orderBy=bonusFromString(self.view.sortBy.get()),
                                      showNoEffect=self.view.noEffect.get())
        self.view.displayBonuses([bonus.toDisplayList() for bonus in bonuses])

    def getCheckBoxData(self):
        self.view.drawCheckBoxField(self.model.getIngredients(self.view.chefNumber.get()))

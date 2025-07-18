from customtkinter import CTkCheckBox

from app.bonus import bonusFromString
from app.ingredients import IngredientType
from app.model import Model
from app.view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def resetCheckBoxField(self):
        for child in self.view.checkBoxField.winfo_children():
            if isinstance(child, CTkCheckBox):
                child.deselect()
        self.displayBonuses()

    def getCheckedIngredient(self) -> list[IngredientType]:
        return [self.model.ingredientTypeOf(chkBox.cget('text'))
                for chkBox in self.view.checkBoxField.winfo_children()
                if isinstance(chkBox, CTkCheckBox) and chkBox.get() == 1]

    def displayBonuses(self):
        bonuses = self.model.getBonus(chefNumber=self.view.chefNumber.get(),
                                      ingredientList=self.getCheckedIngredient(),
                                      orderBy=bonusFromString(self.view.sortBy.get()),
                                      showNoEffect=self.view.noEffect.get())
        self.view.displayBonuses([bonus.toDisplayList() for bonus in bonuses])

    def getCheckBoxData(self):
        self.view.drawCheckBoxField(self.model.getIngredients(self.view.chefNumber.get()))

import customtkinter as ctk

import Bonus
from Model import Model
from View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model: Model = model
        self.view: View = view

    def resetCheckBoxField(self):
        for child in self.view.checkBoxField.winfo_children():
            if child.isinstance(ctk.CTkComboBox):
                child.deselect()

    def displayBonuses(self):
        bonuses = self.model.getBonus(self.view.chefNumber.get(),
                                      Bonus.bonusFromString(self.view.sortBy.get()),
                                      self.view.noEffect.get())
        self.view.displayBonuses([bonus.toDisplayList() for bonus in bonuses])

    def drawCheckBoxField(self):
        pass

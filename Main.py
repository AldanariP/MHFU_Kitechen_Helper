from View import View
from Model import Model
from Controller import Controller

import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MHFU Kitechen Helper")
        self.minsize(850, 400)  # TODO adjust min_heigth with check box layout when implemented
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create a model
        model = Model()
        model.loadIngredientFrom("lang/eng.json")

        # create a view and place it on the root window
        view = View(self)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()

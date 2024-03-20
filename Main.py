from customtkinter import CTk, CTkLabel
from jproperties import Properties

from Controller import Controller
from Model import Model
from View import View


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("MHFU Kitechen Helper")
        self.minsize(980, 400)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        try:
            config = Properties()

            with open('config.properties', 'rb') as configFile:
                config.load(configFile)
                configs = {item[0]: item[1].data for item in config.items()}

            model = Model()

            if model.loadIngredientFrom(configs["langDirectory"] + configs["lang"]):
                self.view = View(self, configs)
                controller = Controller(model, self.view)
                self.view.set_controller(controller)
            else:
                CTkLabel(self, text="Something went wrong while loading json data")

        except KeyError | OSError:
            CTkLabel(self, text="Something went wrong while opening proprety file, some key may be missing or the file "
                                "is not present in the root folder")

    def writeProperties(self):  # no try-except since the app is going to close, the preferences will be lost
        config = Properties()
        with open('config.properties', 'rb') as configFile:
            config.load(configFile)

        viewPrperties = self.view.getProperties()

        config["felyneNumber"] = viewPrperties["felyneNumber"]
        config["orderBy"] = viewPrperties["orderBy"]
        config["showNoEffect"] = viewPrperties["showNoEffect"]

        with open('config.properties', 'wb') as configFile:
            config.store(configFile, encoding="utf-8")


if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.writeProperties())
    app.mainloop()

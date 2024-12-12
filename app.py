from customtkinter import CTk, CTkLabel

from app import io_manager
from app.controller import Controller
from app.model import Model
from app.view import View


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("MHFU Kitechen Helper")
        self.minsize(980, 400)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.view = None

        try:
            configs = io_manager.load_config()
            data = io_manager.load_data()
            model = Model()

            if model.loadIngredientFrom(data):
                self.view = View(self, configs)
                controller = Controller(model, self.view)
                self.view.set_controller(controller)
            else:
                print("faild to json")
                error_label = CTkLabel(master=self, text_color="red",
                                       text="Something went wrong while loading json data, please ensure that it is correcly formatted")
                error_label.grid_configure(column=0, row=0, sticky='nw')

        except FileNotFoundError as e:
            error_label = CTkLabel(master=self, text=str(e), text_color="red")
            error_label.grid_configure(column=0, row=0, sticky='nw')

    def save_properties(self):
        if self.view is not None:
            io_manager.save_config(self.view.getProperties())

        app.destroy()


if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.save_properties)
    app.mainloop()

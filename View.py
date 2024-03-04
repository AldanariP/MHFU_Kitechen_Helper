import customtkinter as ctk
from tkinter import ttk
from Model import BuffType


class View(ctk.CTkFrame):
    DEFAULT_CHEF_VALUE: int = 1  # TODO remeber into preference files

    def __init__(self, parent: ctk.CTk):
        super().__init__(parent, border_color="red", border_width=5)
        self.grid_configure(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.controller = None

        # Primary Action Widgets
        self.actionFrame = ctk.CTkFrame(master=self)
        self.actionFrame.grid_configure(row=0, column=0, sticky="ew")

        self.comboLabel = ctk.CTkLabel(master=self.actionFrame, text="Number of Felynes :")
        self.comboLabel.grid_configure(row=0, column=0, padx=5, sticky="w")

        self.chefNumber: ctk.IntVar = ctk.IntVar()
        self.chefNumber.set(self.DEFAULT_CHEF_VALUE)
        self.chefNumberBox = ctk.CTkComboBox(master=self.actionFrame,
                                             values=["1", "2", "3", "4", "5"],
                                             variable=self.chefNumber,
                                             command=self.UpdateChefNumber)
        self.chefNumberBox.grid_configure(row=0, column=1, sticky="w")

        self.resetButton = ctk.CTkButton(master=self.actionFrame, text="Reset", width=50,
                                         command=self.resetCheckBoxField)
        self.resetButton.grid_configure(row=0, column=2, padx=20, sticky="w")

        # Checkbox Field
        self.checkBoxField = ctk.CTkFrame(master=self, width=350)
        self.checkBoxField.grid_configure(row=1, column=0, sticky="nsew")

        # Result Filters
        self.resultActionFrame = ctk.CTkFrame(master=self)
        self.resultActionFrame.grid_configure(row=0, column=1, sticky="ew")

        self.sortBy: ctk.StringVar = ctk.StringVar()
        self.filterBox = ctk.CTkComboBox(master=self.resultActionFrame,
                                         values=list(BuffType),
                                         variable=self.sortBy,
                                         command=self.sortBuffs,
                                         state="readonly")
        self.filterBox.grid_configure(row=0, column=1)
        self.filterBox.set('Order By')

        self.noEffect: ctk.BooleanVar = ctk.BooleanVar()
        self.noEffectCheckBox = ctk.CTkCheckBox(master=self.resultActionFrame,
                                                text="Show \"No Effect\" Buff",
                                                variable=self.noEffect,
                                                command=self.updateBonuses)
        self.noEffectCheckBox.grid_configure(row=0, column=2)

        # Result Frame
        self.resultField = ctk.CTkFrame(master=self, fg_color="gray14")
        self.resultField.grid_configure(row=1, column=1, rowspan=2, sticky="nsew")

        # Custom Treeview Style (non ckt component)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('Custom.Treeview',
                             background='gray14',
                             foreground='white',
                             fieldbackground="gray14",
                             rowheight=35)
        self.style.configure("Custom.Treeview.Heading",
                             background="gray14",
                             foreground="white",
                             relief="falt",
                             font=("roboto", 12, "bold"))

        # Treeview
        self.resultTable = ttk.Treeview(self.resultField, style="Custom.Treeview")
        self.resultTable.grid_configure(row=0, column=0, sticky="nsew")

        self.resultTable['columns'] = ("Ingredient 1", "Ingredient 2", "Effect")

        self.resultTable.column("#0", width=0, stretch=ctk.NO)  # hide first column
        self.resultTable.column("Ingredient 1", anchor=ctk.CENTER, minwidth=100)
        self.resultTable.column("Ingredient 2", anchor=ctk.CENTER, minwidth=100)
        self.resultTable.column("Effect", anchor=ctk.CENTER, minwidth=300)

        self.resultTable.heading("Ingredient 1", text="Ingredient 1", anchor=ctk.CENTER)
        self.resultTable.heading("Ingredient 2", text="Ingredient 2", anchor=ctk.CENTER)
        self.resultTable.heading("Effect", text="Effect", anchor=ctk.CENTER)

        self.resultTable.tag_configure("RobFont", font=("roboto", 12))

    def displayBonuses(self, entries: list[tuple[str, str, str]]):
        self.resultTable.delete(*self.resultTable.get_children())

        self.resultTable.configure(height=len(entries))

        for entry in entries:
            self.resultTable.insert(parent='', index='end', values=entry, tags="RobFont")

    def UpdateChefNumber(self, unused: str):  # because ctk.IntVar: self.chefNumber is used to share the value
        self.controller.drawCheckBoxField()
        self.controller.displayBonuses()

    def resetCheckBoxField(self):
        self.controller.resetCheckBoxField()

    def sortBuffs(self, unused: str):  # because ctk.IntVar: self.chefNumber is used to share the value
        self.controller.displayBonuses()

    def updateBonuses(self):
        self.controller.displayBonuses()

    def set_controller(self, controller):
        self.controller = controller
        self.controller.displayBonuses()

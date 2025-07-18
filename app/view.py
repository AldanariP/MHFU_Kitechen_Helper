from tkinter import ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel, CTk, IntVar, BooleanVar, CTkComboBox, CTkCheckBox, StringVar

from app.model import BuffType


class View(CTkFrame):

    def __init__(self, parent: CTk, config: dict):
        super().__init__(parent)
        self.grid_configure(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.controller = None

        # Primary Action Widgets
        actionFrame = CTkFrame(master=self)
        actionFrame.grid_configure(row=0, column=0, sticky="ew")

        # Chef's Number ComboBox
        comboLabel = CTkLabel(master=actionFrame, text="Number of Felynes :")
        comboLabel.grid_configure(row=0, column=0, padx=10, sticky="w")

        self.chefNumber: IntVar = IntVar()
        self.chefNumber.set(config['felyneNumber'])
        chefNumberBox = CTkComboBox(master=actionFrame,
                                    values=["1", "2", "3", "4", "5"],
                                    variable=self.chefNumber,
                                    command=self.updateChefNumber)
        chefNumberBox.grid_configure(row=0, column=1, sticky="w")

        # Reset Button
        resetButton = CTkButton(master=actionFrame,
                                text="Reset",
                                width=50,
                                command=self.resetCheckBoxField)
        resetButton.grid_configure(row=0, column=2, padx=20, sticky="w")

        # Checkbox Fields
        self.checkBoxField = CTkFrame(master=self)
        self.checkBoxField.grid_configure(row=1, column=0, sticky="nsew")

        # Result Filters
        resultActionFrame = CTkFrame(master=self)
        resultActionFrame.grid_configure(row=0, column=1, sticky="ew")

        self.sortBy: StringVar = StringVar()
        filterBox = CTkComboBox(master=resultActionFrame,
                                values=list(BuffType),
                                variable=self.sortBy,
                                command=self.sortBuffs,
                                state="readonly")
        filterBox.grid_configure(row=0, column=1)
        if config['orderBy'] is not None:
            self.sortBy.set(config['orderBy'])
        else:
            filterBox.set('Order By')

        self.noEffect: BooleanVar = BooleanVar()
        self.noEffect.set(config['showNoEffect'])
        noEffectCheckBox = CTkCheckBox(master=resultActionFrame,
                                       text="Show \"No Effect\" Buff",
                                       variable=self.noEffect,
                                       command=self.updateBonuses)
        noEffectCheckBox.grid_configure(row=0, column=2, padx=20)

        # Result Frame
        self.resultField = CTkFrame(master=self, fg_color="gray14")
        self.resultField.grid_configure(row=1, column=1, rowspan=2, sticky="nswe")
        self.resultField.bind("<Configure>", self.updateResultTableWidth)

        # Custom Treeview Style (non ckt component)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('Custom.Treeview',
                             background='gray14',
                             foreground='white',
                             fieldbackground="gray14",
                             rowheight=27)
        self.style.configure("Custom.Treeview.Heading",
                             background="gray14",
                             foreground="white",
                             relief="falt",
                             font=("roboto", 12, "bold"))

        # Treeview
        self.resultTable = ttk.Treeview(master=self.resultField, style="Custom.Treeview")
        self.resultTable.grid_configure(row=0, column=0)

        self.resultTable['columns'] = ("Ingredient 1", "Ingredient 2", "Effect")

        self.resultTable.column("#0", width=0, stretch=False)  # hide first column
        self.resultTable.column("Ingredient 1", anchor="center", minwidth=120)
        self.resultTable.column("Ingredient 2", anchor="center", minwidth=120)
        self.resultTable.column("Effect", anchor="center", minwidth=300)

        self.resultTable.heading("Ingredient 1", text="Ingredient 1", anchor="center")
        self.resultTable.heading("Ingredient 2", text="Ingredient 2", anchor="center")
        self.resultTable.heading("Effect", text="Effect", anchor="center")

        self.resultTable.tag_configure("RobFont", font=("roboto", 10))

    def updateResultTableWidth(self, _):
        self.resultTable.place(x=0, y=0, width=self.resultField.winfo_width())

    def displayBonuses(self, entries: list[tuple[str, str, str]]):
        self.resultTable.delete(*self.resultTable.get_children())

        self.resultTable.configure(height=len(entries))

        for entry in entries:
            self.resultTable.insert(parent='', index='end', values=entry, tags="RobFont")

    def drawCheckBoxField(self, ingredientDict: dict[str, list[str]]):

        for widgets in self.checkBoxField.winfo_children():
            widgets.destroy()

        dictLength = sum(len(ingredientList) for ingredientList in ingredientDict.values()) + len(ingredientDict)
        cutLength = int(dictLength / 2 if dictLength % 2 == 0 else (dictLength - 1) / 2)

        for ingredientType, ingredientList in ingredientDict.items():
            widgetCount = len(self.checkBoxField.winfo_children())
            rowIndex = widgetCount if widgetCount <= cutLength \
                else widgetCount - cutLength - (self.checkBoxField.grid_size()[1] - cutLength)  # Offset magic
            colIndex = 0 if widgetCount <= cutLength else 1

            label = CTkLabel(master=self.checkBoxField, text=ingredientType + " :")
            label.grid_configure(row=rowIndex, column=colIndex, sticky="w", padx=10)
            for index, ingredient in enumerate(ingredientList):
                checkbox = CTkCheckBox(self.checkBoxField, text=ingredient, command=self.updateBonuses)
                checkbox.grid_configure(row=rowIndex + index + 1, column=colIndex, sticky="w", padx=20)

    def updateChefNumber(self, unused: str):  # because ctk.IntVar: self.chefNumber is used to share the value
        self.controller.getCheckBoxData()
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
        self.controller.getCheckBoxData()

    def getProperties(self) -> dict[str: str]:
        return {
            "felyneNumber": str(self.chefNumber.get()),
            "orderBy": str(self.sortBy.get() if self.sortBy.get() != "Order By" else None),
            "showNoEffect": str(self.noEffect.get())
        }

from app.controller import Controller
from tkinter import ttk

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkLabel,
    CTk,
    IntVar,
    BooleanVar,
    CTkComboBox,
    CTkCheckBox,
    StringVar,
)

from app.model import BuffType


class View(CTkFrame):
    def __init__(self, parent: CTk, controller: Controller, config: dict):
        super().__init__(parent)
        self.grid_configure(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.controller = controller

        # Primary Action Widgets
        action_frame = CTkFrame(master=self)
        action_frame.grid_configure(row=0, column=0, sticky="ew")

        # Chef's Number ComboBox
        combo_label = CTkLabel(master=action_frame, text="Number of Felynes :")
        combo_label.grid_configure(row=0, column=0, padx=10, sticky="w")

        self.chef_number_var = IntVar()
        self.chef_number_var.set(config["felyneNumber"])
        chef_number_combo_box = CTkComboBox(
            master=action_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.chef_number_var,
            command=self.update_chef_number_command,
        )
        chef_number_combo_box.grid_configure(row=0, column=1, sticky="w")

        # Reset Button
        reset_button = CTkButton(
            master=action_frame, text="Reset", width=50, command=self.reset_check_box_field_command
        )
        reset_button.grid_configure(row=0, column=2, padx=20, sticky="w")

        # Checkbox Fields
        self.check_box_field = CTkFrame(master=self)
        self.check_box_field.grid_configure(row=1, column=0, sticky="nsew")

        # Result Filters
        result_action_frame = CTkFrame(master=self)
        result_action_frame.grid_configure(row=0, column=1, sticky="ew")

        self.sort_by_var = StringVar()
        filter_box_combo = CTkComboBox(
            master=result_action_frame,
            values=list(BuffType),
            variable=self.sort_by_var,
            command=self.sort_buffs_command,
            state="readonly",
        )
        filter_box_combo.grid_configure(row=0, column=1)
        if config["orderBy"] is not None:
            self.sort_by_var.set(config["orderBy"])
        else:
            filter_box_combo.set("Order By")

        self.no_effect_var = BooleanVar()
        self.no_effect_var.set(config["showNoEffect"])
        no_effect_check_box = CTkCheckBox(
            master=result_action_frame,
            text='Show "No Effect" Buff',
            variable=self.no_effect_var,
            command=self.update_bonuses_command,
        )
        no_effect_check_box.grid_configure(row=0, column=2, padx=20)

        self.negative_bonuses_var = BooleanVar()
        self.negative_bonuses_var.set(config["showNegativeBonuses"])
        negative_values_check_box = CTkCheckBox(
            master=result_action_frame,
            text="Show Negative Buffs",
            variable=self.negative_bonuses_var,
            command=self.update_bonuses_command,
        )
        negative_values_check_box.grid_configure(row=0, column=3, padx=20)

        # Result Frame
        self.result_field_frame = CTkFrame(master=self, fg_color="gray14")
        self.result_field_frame.grid_configure(row=1, column=1, rowspan=2, sticky="nswe")
        self.result_field_frame.bind("<Configure>", self.update_result_table_width_callback)

        # Custom Treeview Style (non ckt component)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(
            "Custom.Treeview",
            background="gray14",
            foreground="white",
            fieldbackground="gray14",
            rowheight=27,
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background="gray14",
            foreground="white",
            relief="falt",
            font=("roboto", 12, "bold"),
        )

        # Treeview
        self.result_table_tree = ttk.Treeview(
            master=self.result_field_frame, style="Custom.Treeview"
        )
        self.result_table_tree.grid_configure(row=0, column=0)

        self.result_table_tree["columns"] = ("Ingredient 1", "Ingredient 2", "Effect")

        self.result_table_tree.column("#0", width=0, stretch=False)  # hide first column
        self.result_table_tree.column("Ingredient 1", anchor="center", minwidth=120)
        self.result_table_tree.column("Ingredient 2", anchor="center", minwidth=120)
        self.result_table_tree.column("Effect", anchor="center", minwidth=300)

        self.result_table_tree.heading("Ingredient 1", text="Ingredient 1", anchor="center")
        self.result_table_tree.heading("Ingredient 2", text="Ingredient 2", anchor="center")
        self.result_table_tree.heading("Effect", text="Effect", anchor="center")

        self.result_table_tree.tag_configure("RobFont", font=("roboto", 10))

        self.controller.display_bonuses(self)
        self.controller.get_check_box_data(self)

    def update_result_table_width_callback(self, _):
        self.result_table_tree.place(x=0, y=0, width=self.result_field_frame.winfo_width())

    def display_bonuses(self, entries: list[tuple[str, str, str]]):
        self.result_table_tree.delete(*self.result_table_tree.get_children())

        self.result_table_tree.configure(height=len(entries))

        for entry in entries:
            self.result_table_tree.insert(
                parent="", index="end", values=entry, tags="RobFont"
            )

    def draw_check_box_field(self, ingredient_dict: dict[str, list[str]]):

        for widgets in self.check_box_field.winfo_children():
            widgets.destroy()

        dict_length = sum(
            len(ingredient_list) for ingredient_list in ingredient_dict.values()
        ) + len(ingredient_dict)
        cut_length = int(dict_length / 2 if dict_length % 2 == 0 else (dict_length - 1) / 2)

        for ingredient_type, ingredient_list in ingredient_dict.items():
            widget_count = len(self.check_box_field.winfo_children())
            row_index = (
                widget_count
                if widget_count <= cut_length
                else widget_count
                - cut_length
                - (self.check_box_field.grid_size()[1] - cut_length)
            )  # Offset magic
            col_index = 0 if widget_count <= cut_length else 1

            label = CTkLabel(master=self.check_box_field, text=ingredient_type + " :")
            label.grid_configure(row=row_index, column=col_index, sticky="w", padx=10)
            for index, ingredient in enumerate(ingredient_list):
                checkbox = CTkCheckBox(
                    self.check_box_field, text=ingredient, command=self.update_bonuses_command
                )
                checkbox.grid_configure(
                    row=row_index + index + 1, column=col_index, sticky="w", padx=20
                )

    def update_chef_number_command(
        self, unused: str
    ):  # because ctk.IntVar: self.chef_number is used to share the value
        self.controller.get_check_box_data(self)
        self.controller.display_bonuses(self)

    def reset_check_box_field_command(self):
        self.controller.reset_check_box_field(self)

    def sort_buffs_command(
        self, unused: str
    ):  # because ctk.IntVar: self.chef_number is used to share the value
        self.controller.display_bonuses(self)

    def update_bonuses_command(self):
        self.controller.display_bonuses(self)

    def set_controller(self, controller):
        self.controller = controller

    def get_properties_dict(self) -> dict[str,str]:
        return {
            "felyneNumber": str(self.chef_number_var.get()),
            "orderBy": str(
                self.sort_by_var.get() if self.sort_by_var.get() != "Order By" else None
            ),
            "showNoEffect": str(self.no_effect_var.get()),
            "showNegativeBonuses": str(self.negative_bonuses_var.get()),
        }

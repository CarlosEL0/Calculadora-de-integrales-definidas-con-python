# ui/components/control_panel.py
import customtkinter as ctk
import tkinter as tk
from ui.components.widgets.keyboard import Keyboard
from ui.components.widgets.tooltip import Tooltip
from PIL import Image
from ui.components.widgets.math_label import MathLabel


class ControlPanel(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.last_focused_entry = None

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._load_icons()

        self._create_input_widgets()
        self._create_result_display()
        # --- La creación del teclado ahora es una sola línea ---
        self.keyboard = Keyboard(self, key_press_callback=self.on_key_press, backspace_callback=self.on_backspace_press)
        self.keyboard.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self._setup_focus_tracking()

    def _load_icons(self):
        try:
            # Cargar las imágenes para ambos modos (claro y oscuro)
            self.calc_icon = ctk.CTkImage(
                light_image=Image.open("assets/icons/calculator.png"),
                dark_image=Image.open("assets/icons/calculator.png"),
                size=(20, 20)
            )
            self.clear_icon = ctk.CTkImage(
                light_image=Image.open("assets/icons/clear.png"),
                dark_image=Image.open("assets/icons/clear.png"),
                size=(20, 20)
            )
        except FileNotFoundError as e:
            print(f"ADVERTENCIA: No se pudieron cargar los iconos. Error: {e}")
            print("Los botones se mostrarán sin iconos.")
            self.calc_icon = None
            self.clear_icon = None

    def _create_input_widgets(self):
        input_group = ctk.CTkFrame(self, fg_color="transparent")
        input_group.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Función
        ctk.CTkLabel(input_group, text="f(x) =").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.func_entry = ctk.CTkEntry(input_group, placeholder_text="Ej: k*x^2")
        self.func_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=2, sticky="ew")

        # Límite Inferior
        ctk.CTkLabel(input_group, text="Lím. Inferior (a):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lower_limit_entry = ctk.CTkEntry(input_group, width=150)
        self.lower_limit_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Límite Superior
        ctk.CTkLabel(input_group, text="Lím. Superior (b):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.upper_limit_entry = ctk.CTkEntry(input_group, width=150)
        self.upper_limit_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Constantes
        ctk.CTkLabel(input_group, text="Constantes:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.constants_entry = ctk.CTkEntry(input_group, placeholder_text="ej: a, k, m (separadas por coma)")
        self.constants_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        # Ahora sí podemos agregar el Tooltip, después de crear el widget
        Tooltip(self.constants_entry, "Define tus constantes simbólicas separadas por comas")

        # Grupo de botones
        button_group = ctk.CTkFrame(self, fg_color="transparent")
        button_group.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Botón Calcular con icono
        calc_button = ctk.CTkButton(
            button_group, 
            text="Calcular",
            image=self.calc_icon,
            compound="left",
            command=lambda: self.controller.on_calculate_click()
        )
        calc_button.pack(side="left", padx=5)


        # Botón Limpiar con icono
        clear_button = ctk.CTkButton(
            button_group,
            text="Limpiar Todo",
            image=self.clear_icon,
            compound="left",
            fg_color="#5C6773",
            hover_color="#495057",
            command=lambda: self.controller.on_clear_click()
        )
        clear_button.pack(side="left", padx=5)


    def _create_result_display(self):
        result_group = ctk.CTkFrame(self, fg_color="transparent")
        result_group.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Para el resultado principal (la integral definida)
        self.result_label = MathLabel(result_group, font_size=16)
        self.result_label.pack(fill="x", pady=(0, 5))
        self.result_label.set_text(r"\text{Resultado:}") # Texto inicial

        # Para el resultado secundario (la antiderivada)
        self.indefinite_result_label = MathLabel(result_group, font_size=12)
        self.indefinite_result_label.pack(fill="x")
        self.indefinite_result_label.set_text(r"\text{Antiderivada: } + C") # Texto inicial

    def _setup_focus_tracking(self):
        self.last_focused_entry = self.func_entry
        self.func_entry.bind("<FocusIn>", lambda e: self.set_focus(self.func_entry))
        self.lower_limit_entry.bind("<FocusIn>", lambda e: self.set_focus(self.lower_limit_entry))
        self.upper_limit_entry.bind("<FocusIn>", lambda e: self.set_focus(self.upper_limit_entry))
        self.constants_entry.bind("<FocusIn>", lambda e: self.set_focus(self.constants_entry))

    def set_focus(self, entry_widget):
        self.last_focused_entry = entry_widget

    def on_key_press(self, value: str):
        if self.last_focused_entry:
            if self.last_focused_entry == self.constants_entry and not (value.isalpha() or value == ','):
                return
            self.last_focused_entry.insert(tk.END, value)

    def on_backspace_press(self):
        if self.last_focused_entry:
            current_text = self.last_focused_entry.get()
            if current_text: self.last_focused_entry.delete(len(current_text) - 1, tk.END)

    def get_inputs(self):
        return {"function": self.func_entry.get(), "lower_limit": self.lower_limit_entry.get(),
                "upper_limit": self.upper_limit_entry.get(), "constants": self.constants_entry.get()}

    def update_results(self, defined_integral_str, indefinite_integral_str):
        self.result_label.set_text(rf"\int f(x)dx = {defined_integral_str}", is_result=True)
        self.indefinite_result_label.set_text(rf"\int f(x)dx = {indefinite_integral_str} + C")

    def clear_inputs(self):
        self.func_entry.delete(0, 'end')
        self.lower_limit_entry.delete(0, 'end')
        self.upper_limit_entry.delete(0, 'end')
        self.constants_entry.delete(0, 'end')

        # Limpiar los nuevos labels matemáticos
        self.result_label.set_text(r"\text{Resultado:}")
        self.indefinite_result_label.set_text(r"\text{Antiderivada: } + C")
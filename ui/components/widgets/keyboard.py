# ui/components/keyboard.py (Nueva versión limpia y basada en datos)
import customtkinter as ctk
from ui.components.widgets.tooltip import Tooltip
# >>> Importa la estructura del layout desde el nuevo archivo
from ui.components.widgets.keyboard_layouts import KEYBOARD_LAYOUT


class Keyboard(ctk.CTkTabview):
    """
    Un teclado virtual que construye su interfaz dinámicamente a partir
    de una estructura de datos externa.
    """

    def __init__(self, master, key_press_callback, backspace_callback):
        super().__init__(master, anchor="w")

        self.key_press_callback = key_press_callback
        self.backspace_callback = backspace_callback

        # Construir el teclado iterando sobre la estructura de datos
        self._build_from_layout()

    def _build_from_layout(self):
        """
        Itera sobre la estructura KEYBOARD_LAYOUT para crear pestañas y botones.
        """
        for tab_name, tab_data in KEYBOARD_LAYOUT.items():
            tab = self.add(tab_name)
            layout = tab_data["layout"]
            tooltips = tab_data["tooltips"]

            # Configurar la rejilla de la pestaña dinámicamente
            num_rows = len(layout)
            num_cols = len(layout[0]) if num_rows > 0 else 0
            for i in range(num_cols):
                tab.grid_columnconfigure(i, weight=1)
            for i in range(num_rows):
                tab.grid_rowconfigure(i, weight=1)

            # Crear los botones para esta pestaña
            for r_idx, row in enumerate(layout):
                for c_idx, btn_text in enumerate(row):
                    self._create_button(tab, btn_text, r_idx, c_idx, tooltips)

    def _create_button(self, parent, text, row, col, tooltips):
        """Función helper para crear un único botón."""
        if text == "Borrar":
            command = self.backspace_callback
        else:
            command = lambda t=text: self.key_press_callback(t)

        button = ctk.CTkButton(parent, text=text, command=command)
        button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        if text in tooltips:
            Tooltip(button, tooltips[text])
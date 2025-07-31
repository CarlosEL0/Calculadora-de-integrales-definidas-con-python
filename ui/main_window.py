# ui/main_window.py

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from ui.style import AppTheme
from ui.components.panels.control_panel import ControlPanel
from ui.components.panels.plot_panel import PlotPanel


class MainWindow(ctk.CTk):
    """La ventana principal de la aplicación. Ensambla los componentes."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # --- Configuración de la Ventana Principal ---
        self.title("Calculadora de Integrales Avanzada")
        self.geometry("1100x800")
        self.configure(fg_color=AppTheme.BG_COLOR)
        ctk.set_appearance_mode("Dark")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Configuración del Layout Principal (Grid) ---
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

        # --- Creación de los componentes y la "carcasa" ---
        self._create_menu()
        self._create_components()
        self._create_statusbar()

    def _create_menu(self):
        """Crea la barra de menú superior."""
        self.menubar = tk.Menu(self, bg=AppTheme.FG_COLOR, fg=AppTheme.TEXT_COLOR)
        self.config(menu=self.menubar)

        # Menú Archivo
        file_menu = tk.Menu(self.menubar, tearoff=0, bg=AppTheme.FG_COLOR, fg=AppTheme.TEXT_COLOR)
        self.menubar.add_command(label="Salir", command=self.on_closing)


        # Menú Historial
        menubar = tk.Menu(self.menubar, tearoff=0, bg=AppTheme.FG_COLOR, fg=AppTheme.TEXT_COLOR)
        self.menubar.add_command(label="Historial", command=lambda: self.controller.on_show_history_click())


    def _create_components(self):
        """Crea e instancia los paneles principales de la UI."""
        self.control_panel = ControlPanel(self, self.controller)
        self.control_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.plot_panel = PlotPanel(self)
        self.plot_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

    def _create_statusbar(self):
        self.statusbar = ctk.CTkLabel(self, text="Listo.", anchor="w", height=25)
        self.statusbar.grid(row=1, column=0, columnspan=2, sticky="ew")

    # --- Métodos de Interfaz Pública (Fachada/Facade) ---
    # Estos métodos simplemente delegan la llamada al componente correcto.
    # El controlador solo necesita hablar con MainWindow.

    def get_inputs(self):
        return self.control_panel.get_inputs()

    def update_results(self, defined_integral, indefinite_integral):
        self.control_panel.update_results(defined_integral, indefinite_integral)

    def plot_function(self, numeric_func, a, b, title, fill_area=True):
        self.plot_panel.plot_function(numeric_func, a, b, title, fill_area)

    def clear_plot(self, title="Gráfica de f(x)"):
        self.plot_panel.clear_plot(title=title) # Permitir un título personalizado al limpiar

    def clear_ui(self):
        self.control_panel.clear_inputs()
        self.plot_panel.clear_plot()
        self.update_statusbar("Campos limpiados.")

    def update_statusbar(self, message: str, is_error: bool = False):
        self.statusbar.configure(text=f"  {message}", fg_color=("#DC3545" if is_error else AppTheme.PRIMARY))

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def on_closing(self):
        # Lógica de guardado o confirmación si fuera necesario en el futuro
        self.destroy()

    def show_info(self, title, message):
        """Muestra un popup de información."""
        messagebox.showinfo(title, message)
# ui/components/history_window.py
import customtkinter as ctk
from tkinter import ttk
from ui.style import AppTheme

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, master, history_data):
        super().__init__(master)

        self.title("Historial de Cálculos")
        self.geometry("800x400")  # Aumentado el ancho para mejor visualización
        self.transient(master)
        self.grab_set()
        self.configure(fg_color=AppTheme.BG_COLOR)

        self.sort_state = {}
        self._create_widgets(history_data)

    def _create_widgets(self, history_data):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Configurar el estilo del Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                       background=AppTheme.ENTRY_BG,
                       foreground=AppTheme.TEXT_COLOR,
                       fieldbackground=AppTheme.ENTRY_BG,
                       bordercolor=AppTheme.FG_COLOR,
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background=AppTheme.PRIMARY,
                       foreground="white",
                       font=('Segoe UI', 10, 'bold'),
                       relief="flat")
        style.map('Treeview',
                  background=[('selected', AppTheme.PRIMARY)])
        style.map('Treeview.Heading',
                  background=[('active', AppTheme.BUTTON_HOVER)])

        # Definir las columnas con sus nombres internos y de visualización
        columns = {
            "function": "Función f(x)",
            "lower_limit": "Límite a",
            "upper_limit": "Límite b",
            "constants": "Constantes",
            "result": "Resultado"
        }

        self.tree = ttk.Treeview(container, columns=list(columns.keys()), show="headings")

        # Configurar las cabeceras y el ancho de las columnas
        for col_id, col_text in columns.items():
            self.tree.heading(col_id, text=col_text,
                            command=lambda c=col_id: self.sort_column(c))
            if col_id == "function":
                self.tree.column(col_id, width=200, anchor='w')
            elif col_id == "result":
                self.tree.column(col_id, width=200, anchor='center')
            elif col_id == "constants":
                self.tree.column(col_id, width=100, anchor='center')
            else:
                self.tree.column(col_id, width=80, anchor='center')

        # Insertar los datos en la tabla
        for item in history_data:
            values = [
                item["function"],
                item["lower_limit"],
                item["upper_limit"],
                item.get("constants", ""),  # Usar get() para manejar casos donde no hay constantes
                item["result"]
            ]
            self.tree.insert("", "end", values=values)

        # Añadir scrollbar
        scrollbar = ctk.CTkScrollbar(container, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Colocar el Treeview
        self.tree.grid(row=0, column=0, sticky="nsew")

    def sort_column(self, col):
        """Ordena la tabla por la columna especificada."""
        reverse = self.sort_state.get(col, False)
        data_list = []
        
        for child_id in self.tree.get_children(''):
            try:
                value = float(self.tree.set(child_id, col))
            except ValueError:
                value = self.tree.set(child_id, col).lower()
            data_list.append((value, child_id))

        data_list.sort(reverse=reverse)
        for index, (_, child_id) in enumerate(data_list):
            self.tree.move(child_id, '', index)

        self.sort_state[col] = not reverse
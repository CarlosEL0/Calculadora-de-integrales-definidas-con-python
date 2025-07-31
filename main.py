# main.py (Corregido)
from ui.main_window import MainWindow
from core.calculator import CalculatorEngine
from sympy import latex
from ui.components.windows.history_window import HistoryWindow

class AppController:
    """Controlador que conecta la UI con la lógica de cálculo."""

    def __init__(self):
        self.model = CalculatorEngine()
        # 2. El controlador crea la Vista, pasándose a sí mismo como referencia.
        #    Ahora la vista SIEMPRE tendrá un controlador válido desde el inicio.
        self.view = MainWindow(self)

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.view.update_statusbar("Aplicación iniciada. Lista para calcular.")
        self.view.mainloop()

    def on_calculate_click(self):
        """Maneja el evento del botón 'Calcular'."""
        # Se obtiene una referencia a la vista (opcional, pero puede ser útil)
        view = self.view

        inputs = view.get_inputs()

        if not inputs["function"] or not inputs["lower_limit"] or not inputs["upper_limit"]:
            view.show_error("Campos vacíos", "Por favor, rellene todos los campos (función y límites).")
            view.update_statusbar("Error: Todos los campos son requeridos.", is_error=True)
            return

        view.update_statusbar("Calculando...")
        result = self.model.calculate_integral(
            inputs["function"], inputs["lower_limit"], inputs["upper_limit"], inputs["constants"]
        )

        if result["success"]:
            # Manejar el caso donde el resultado es simbólico
            # Usar LaTeX para una presentación matemática limpia
            defined_result_str = str(latex(result['defined_integral']))
            indef_result_str = str(latex(result['indefinite_integral']))

            view.update_results(defined_result_str, indef_result_str)

            if result["numeric_func"]:
                view.plot_function(
                    result["numeric_func"], result["a"], result["b"],
                    title=f"Gráfica de: ${latex(result['func_expr'])}$",
                    fill_area=result["can_fill_area"]  # <--- Ahora usamos el nuevo flag can_fill_area
                )
            else:
                # Si no se puede graficar (contiene símbolos), limpiamos el plot
                view.clear_plot("Función no graficable (contiene símbolos)")
                view.update_statusbar("Cálculo simbólico completado. No se puede graficar la función.", is_error=True)

    def on_clear_click(self):
        self.view.clear_ui()

    def on_key_press(self, value):
        self.view.control_panel.insert_text_in_entry(value)

    # >>> NUEVO: Método para mostrar la ventana de historial
    def on_show_history_click(self):
        """Muestra una ventana con el historial de cálculos."""
        history = self.model.get_history()
        if not history:
            self.view.show_info("Historial", "El historial de cálculos está vacío.")
            return

        # Crea la ventana del historial, pasándole la data
        history_window = HistoryWindow(master=self.view, history_data=history)
        history_window.focus()

    def on_export_click(self):
        self.view.update_statusbar("FUNCIONALIDAD: Exportar a PDF (aún no implementada)")

    def on_show_help_click(self):
        self.view.update_statusbar("FUNCIONALIDAD: Mostrar ventana de ayuda (aún no implementada)")

    def on_show_about_click(self):
        self.view.show_error(
            "Acerca de Calculadora de Integrales",
            "Calculadora de Integrales Avanzada v1.0\n"
            "Desarrollada como proyecto de ejemplo."
        )


if __name__ == "__main__":
    # La nueva forma de iniciar la aplicación. Limpia y segura.
    app = AppController()
    app.run()
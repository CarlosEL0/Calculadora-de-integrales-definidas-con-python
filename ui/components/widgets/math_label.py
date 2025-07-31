# ui/components/math_label.py
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.style import AppTheme


class MathLabel(ctk.CTkFrame):
    """
    Un widget para renderizar y mostrar expresiones LaTeX usando Matplotlib.
    """

    def __init__(self, master, font_size=12):
        super().__init__(master, fg_color="transparent")

        self.figure = Figure(figsize=(4, 0.6), dpi=100, facecolor=AppTheme.FG_COLOR)
        # Quitar los ejes y hacer que el layout sea compacto
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        self.figure.tight_layout(pad=0)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.font_size = font_size

    def set_text(self, latex_string: str, is_result=False):
        """
        Limpia la figura y renderiza la nueva cadena LaTeX.
        """
        self.ax.clear()
        self.ax.axis('off')

        clean_latex_string = latex_string.replace(r'\limits', '')

        # El resto del método usa la cadena ya limpia.
        display_text = rf"${clean_latex_string}$"

        try:
            self.ax.text(0.5, 0.5, display_text,
                         fontsize=self.font_size + (4 if is_result else 0),
                         color=AppTheme.TEXT_COLOR,
                         va='center', ha='center')
        except Exception as e:
            print(f"Error de renderizado de Mathtext: {e}")
            self.ax.text(0.5, 0.5, "Error de formato", fontsize=self.font_size, color="red", va='center', ha='center')

        self.canvas.draw()

    def clear(self):
        """Limpia el contenido del label."""
        self.ax.clear()
        self.ax.axis('off')
        self.canvas.draw()
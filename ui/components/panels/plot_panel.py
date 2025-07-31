import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from ui.style import AppTheme


class PlotPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=AppTheme.FG_COLOR, corner_radius=8)

        self.current_numeric_func = None
        self.view_change_cid = None

        self._create_plot_widgets()

    def _create_plot_widgets(self):
        """Crea la infraestructura de Matplotlib de forma robusta."""
        self.fig = Figure(figsize=(7, 4), dpi=100, facecolor=AppTheme.FG_COLOR)
        self.fig.subplots_adjust(bottom=0.15, top=0.95, left=0.1, right=0.95)

        self.ax = self.fig.add_subplot(111)
        # ... (toda la configuración de estilo del 'ax' se mantiene igual) ...
        self.ax.set_facecolor(AppTheme.BG_COLOR)
        self.ax.tick_params(axis='x', colors=AppTheme.TEXT_COLOR)
        self.ax.tick_params(axis='y', colors=AppTheme.TEXT_COLOR)
        self.ax.spines['bottom'].set_color(AppTheme.TEXT_COLOR)
        self.ax.spines['top'].set_color('none')
        self.ax.spines['left'].set_color(AppTheme.TEXT_COLOR)
        self.ax.spines['right'].set_color('none')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=5)

        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        toolbar.update()
        toolbar.configure(background=AppTheme.FG_COLOR)
        for button in toolbar.winfo_children():
            button.configure(background=AppTheme.FG_COLOR, relief=ctk.FLAT)
        toolbar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self.clear_plot()

    def clear_plot(self, title="Gráfica de f(x)"):
        """Limpia el gráfico y desconecta cualquier callback activo."""
        # >>> CORREGIDO: Desconectar del objeto 'ax', no de la figura <<<
        if self.view_change_cid:
            self.ax.callbacks.disconnect(self.view_change_cid)
            self.view_change_cid = None

        self.current_numeric_func = None

        self.ax.clear()
        self.ax.grid(True, linestyle="--", alpha=0.3)
        self.ax.set_title(title, color=AppTheme.TEXT_COLOR)
        self.canvas.draw()

    def plot_function(self, numeric_func, a, b, title, fill_area=True):
        """Dibuja la gráfica inicial y activa el redibujado dinámico."""
        self.clear_plot(title=title)

        self.current_numeric_func = numeric_func
        # Guardar los límites de integración para el redibujado
        if fill_area:
            self.integration_limits = (a, b)
        else:
            self.integration_limits = None

        self._draw_initial_view(a, b, fill_area)
        self.view_change_cid = self.ax.callbacks.connect('xlim_changed', self.on_view_change)

    def on_view_change(self, axes):
        """Callback que se activa al panear/hacer zoom, redibuja la línea de la función y el área."""
        if self.current_numeric_func is None:
            return

        new_xmin, new_xmax = axes.get_xlim()
        x_dynamic = np.linspace(new_xmin, new_xmax, 800)

        with np.errstate(invalid='ignore'):
            y_dynamic = np.array([self.current_numeric_func(v) for v in x_dynamic])

        # Actualizar la línea principal
        if self.ax.lines:
            self.ax.lines[0].set_data(x_dynamic, y_dynamic)

        # Actualizar el área sombreada si existe
        if self.ax.collections and hasattr(self, 'integration_limits'):
            a, b = self.integration_limits
            fill_mask = ((x_dynamic >= a) & (x_dynamic <= b))
            # Remover el área sombreada anterior
            self.ax.collections[0].remove()
            # Crear nueva área sombreada
            self.ax.fill_between(x_dynamic[fill_mask], y_dynamic[fill_mask],
                                 color=AppTheme.PRIMARY, alpha=0.4)

        # Re-calcular los límites Y
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)

        self.canvas.draw_idle()

    def _draw_initial_view(self, a, b, fill_area):
        """Dibuja los elementos que no cambian (línea inicial y área sombreada)."""
        range_span = max((b - a), 4)  # Un poco más de rango inicial
        x_min, x_max = a - range_span / 2, b + range_span / 2

        x_vals = np.linspace(x_min, x_max, 400)
        with np.errstate(invalid='ignore'):
            y_vals = np.array([self.current_numeric_func(v) for v in x_vals])

        finite_mask = np.isfinite(y_vals)
        # Dibujar la línea de la función
        self.ax.plot(x_vals[finite_mask], y_vals[finite_mask], label="f(x)", color="#33C1FF")

        # Dibujar el área de integración si es aplicable
        if fill_area:
            fill_mask = ((x_vals >= a) & (x_vals <= b))
            self.ax.fill_between(x_vals[fill_mask], y_vals[fill_mask], color=AppTheme.PRIMARY, alpha=0.4,
                                 label="Área de integración")

        self.ax.legend(facecolor=AppTheme.FG_COLOR, labelcolor=AppTheme.TEXT_COLOR, framealpha=0.5)
        self.canvas.draw()
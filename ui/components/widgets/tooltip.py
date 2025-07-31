# ui/components/tooltip.py (Versión Mejorada con Retardo)

import customtkinter as ctk


class Tooltip:
    """
    Crea un Tooltip con un retardo para cualquier widget de CustomTkinter.
    """

    def __init__(self, widget, text: str, delay_ms: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay_ms
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.cancel_tooltip)
        self.widget.bind("<ButtonPress>", self.cancel_tooltip)  # Ocultar si se hace clic

    def schedule_tooltip(self, event=None):
        """Programa la aparición del tooltip después de un retardo."""
        self.cancel_tooltip()  # Cancelar cualquier tooltip pendiente
        if self.text:
            self.after_id = self.widget.after(self.delay, self._show_tooltip)

    def cancel_tooltip(self, event=None):
        """Cancela la aparición programada y oculta el tooltip si ya es visible."""
        # Cancelar el evento programado
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

        # Ocultar la ventana si ya existe
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def _show_tooltip(self):
        """Crea y muestra la ventana del tooltip."""
        if self.tooltip_window or not self.text:
            return

        # Usar winfo_pointer para obtener la posición actual del ratón
        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)  # Asegurar que esté por encima de todo

        label = ctk.CTkLabel(self.tooltip_window, text=self.text,
                             fg_color="#303030", text_color="white",
                             corner_radius=4, padx=8, pady=4,
                             font=("Segoe UI", 10))
        label.pack()
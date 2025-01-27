#!/usr/bin/env python3

__author__ = "Juan Sebastian Daleman Martine"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martine"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

import tkinter as tk
from tkinter import ttk

#Paletas de colores
#https://colorhunt.co/palette/f3f3e0133e87608bc1cbdceb
#https://colorhunt.co/palette/001f3f3a6d8c6a9ab0ead8b1

class BaseStyle:
    """Clase base para aplicar estilos personalizados a los widgets."""

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(root)

    def apply_style(self, widget, style_name=None):
        if style_name is None:
            style_name = self.style_name
        """Aplica un estilo a un widget dado."""
        widget.config(style=style_name)

class StyleFrame(BaseStyle):
    """Clase para aplicar estilos personalizados a los frames."""

    def __init__(self, root):
        super().__init__(root)

        self.style_name = 'Personality.TFrame'
        # Configuración del estilo para frames
        self.style.configure(
            'Personality.TFrame',
            background='#CBDCEB',
            relief='solid',
            bordercolor='#133E87',
            borderwidth=1
        )

class StyleButton(BaseStyle):
    """Clase para aplicar estilos personalizados a los botones."""

    def __init__(self, root):
        super().__init__(root)

        self.style_name = 'Personality.TButton'
        # Configuración del estilo para botones
        self.style.configure(
            'Personality.TButton',
            font=('Roboto', 12),
            foreground='#EAD8B1',
            background='#6A9AB0',
            relief='flat',
            padding=2
        )
        self.style.map(
            'Personality.TButton',
            foreground=[('pressed', '#6A9AB0'), ('active', '#3E5879')],
            background=[('pressed', '#213555'), ('active', '#EAD8B1')]
        )


class StyleLabel(BaseStyle):
    """Clase para aplicar estilos personalizados a las etiquetas."""

    def __init__(self, root):
        super().__init__(root)

        self.style_name = 'Personality.TLabel'
        # Configuración del estilo para etiquetas
        self.style.configure(
            'Personality.TLabel',
            font=('Roboto', 12, 'bold'),
            foreground='#3E5879',
            background='#CBDCEB',
            padding=5
        )


class StyleEntry(BaseStyle):
    """Clase para aplicar estilos personalizados a los campos de entrada."""

    def __init__(self, root):
        super().__init__(root)

        self.style_name = 'Personality.TEntry'
        # Configuración del estilo para campos de entrada
        self.style.configure(
            'Personality.TEntry',
            font=('Roboto', 12),
            foreground='#3E5879',
            fieldbackground='#F3F3E0',
            padding=5
        )
        self.style.map(
            'Personality.TEntry',
            focusbackground=[('focus', '#2980B9')],
            foreground=[('disabled', '#7F8C8D')]
        )


def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Aplicación con Estilos Personalizados")
    root.geometry("400x400")

    # Instanciar los estilos
    button_style = StyleButton(root)
    frame_style = StyleFrame(root)
    label_style = StyleLabel(root)
    entry_style = StyleEntry(root)

    # Crear un frame y aplicar estilo
    frame = ttk.Frame(root)
    frame_style.apply_style(frame, 'Personality.TFrame')
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Crear un label y aplicar estilo
    label = ttk.Label(frame, text="Etiqueta con estilo personalizado")
    label_style.apply_style(label, 'Personality.TLabel')
    label.pack(pady=10)

    # Crear un entry y aplicar estilo
    entry = ttk.Entry(frame)
    entry_style.apply_style(entry, 'Personality.TEntry')
    entry.pack(pady=10)

    # Crear un botón y aplicar estilo
    button = ttk.Button(frame, text="Haz clic aquí")
    button_style.apply_style(button, 'Personality.TButton')
    button.pack(pady=10)

    # Iniciar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk

class StyleButtonApp:
    def __init__(self, root):
        self.root = root

        # Crear un objeto Style para personalizar los estilos
        self.style = ttk.Style()

        #Paleta de colores https://colorhunt.co/palette/001f3f3a6d8c6a9ab0ead8b1
        # Definir un estilo personalizado para los botones
        self.style.configure('Personality.TButton',  # Nombre del estilo
                             font=('Roboto', 12),         # Fuente
                             foreground='#EAD8B1',        # Color del texto
                             background='#6A9AB0',        # Color de fondo
                             relief='flat',                  # Borde plano
                             padding=2                      # Espaciado interno
                            )

        self.style.map('Personality.TButton',  # Nombre del estilo
                       foreground=[('pressed', '#6A9AB0'), ('active', '#3E5879')],  # Color del texto cuando está presionado o activo
                       background=[('pressed', '#213555'), ('active', '#EAD8B1')] # Color de fondo cuando está presionado o activo
                      )
    
    def apply_style(self, button):
        # Aplicar el estilo al botón proporcionado
        button.config(style='Personality.TButton')


def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Aplicación con Estilos de Botones")

    # Crear un botón en la ventana principal
    button = ttk.Button(root, text="Haz clic aquí", command=lambda: print("¡Botón presionado!"))
    button.pack(pady=20)

    # Crear el objeto de la clase StyleButtonApp
    app = StyleButtonApp(root)

    # Aplicar el estilo al botón
    app.apply_style(button)

    # Iniciar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()

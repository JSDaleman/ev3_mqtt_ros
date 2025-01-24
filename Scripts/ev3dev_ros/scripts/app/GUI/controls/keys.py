

def manejar_tecla_right(root, event, entry):
        if root.focus_get() == entry:
            # Comportamiento cuando el Entry tiene el enfoque
            print("Cursor moviéndose a la derecha dentro del Entry")
            return
        else:
            # Comportamiento cuando el Entry NO tiene el enfoque
            print("Hola mundo (tecla Right fuera del Entry)")
            return "break"  # Bloquea el comportamiento predeterminado de la tecla

def quitar_foco(root, event, entry):
        # Si el clic no es sobre el Entry, quita el enfoque
        if event.widget != entry:
            root.focus()


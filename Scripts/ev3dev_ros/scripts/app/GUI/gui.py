#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
import app.gui.views.frames.differencial_frame as differencial_frame
import app.gui.styles.styles as styles

class GUI(QMainWindow):

    def __init__(self, mqtt_client, delegate):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.delegate = delegate

        # Creación de ventana principal del GUI y título
        self.setWindowTitle("Control EV3 with MQTT messages")
        self.setGeometry(100, 100, 400, 300)
        self.setMinimumSize(300, 200)

        # Aplicar estilo al MainWindow
        self.style_main_window = styles.StyleMainWindow()
        self.style_main_window.apply_style(self)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Creación de frame diferencial
        self.diff_frame = differencial_frame.DifferencialFrame(self, self.mqtt_client, delegate)
        layout.addWidget(self.diff_frame)

    def resizeEvent(self, event):
        """Evento que se ejecuta cuando la ventana cambia de tamaño"""
        super().resizeEvent(event)
        self.update_font_size()  # Actualizar fuente al cambiar tamaño0000

    def update_font_size(self):
        """Calcula el tamaño de fuente dinámico basado en el ancho de la ventana"""
        nuevo_tamano = max(min(self.width(), self.height()) // 30, 12)  # Ajuste proporcional al ancho

        # Aplicar el nuevo tamaño de fuente a todos los widgets
        for widget in self.findChildren(QWidget):  
            if hasattr(widget, "setFont"):  # Verifica que el widget soporta setFont
                fuente = widget.font()
                fuente.setPointSize(nuevo_tamano)
                widget.setFont(fuente)

    def closeEvent(self, event):
        """ Controla el cierre de la ventana (X) """
        # Cierre del cliente MQTT al finalizar
        self.mqtt_client.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = GUI(None, None)  # Pasar los objetos mqtt_client y delegate reales
    window.show()
    sys.exit(app.exec_())

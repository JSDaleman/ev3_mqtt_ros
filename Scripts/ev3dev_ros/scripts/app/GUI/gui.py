#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import app.gui.views.frames.differencial_frame as differencial_frame

class GUI(QMainWindow):

    def __init__(self, mqtt_client, delegate):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.delegate = delegate

        # Creación de ventana principal del GUI y título
        self.setWindowTitle("Control EV3 with MQTT messages")
        self.setGeometry(100, 100, 400, 300)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Creación de frame diferencial
        self.diff_frame = differencial_frame.DifferencialFrame(self, self.mqtt_client, delegate)
        layout.addWidget(self.diff_frame)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = GUI(None, None)  # Pasar los objetos mqtt_client y delegate reales
    window.show()
    sys.exit(app.exec_())

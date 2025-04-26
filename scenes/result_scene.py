
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt

class ResultsScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui() # UI başlat

    def init_ui(self):
        layout = QVBoxLayout() # Ana dikey layout oluşturuyoruz

        # NAVIGATION BUTTONS
        nav_layout = QHBoxLayout() # Yatay navigasyon butonları layout'u
        
        # geri butonu
        back_button = QPushButton("Geri")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        # Geri butonuna tıklayınca yapılacak işlem
        # back_button.clicked.connect(self.main_window.switch_to_diagnosis_scene(self.main_window.tc_no.text()))
        nav_layout.addWidget(back_button)
        layout.addLayout(nav_layout)

        # Ana layout'a bir başlık etiketi ekliyoruz
        layout.addWidget(QLabel("Sonuçlar ve geçmiş kayıtlar:"))

        # Tüm layout'u pencereye uyguluyoruz
        self.setLayout(layout)


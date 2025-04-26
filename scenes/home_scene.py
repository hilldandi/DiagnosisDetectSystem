from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt


class HomeScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Ana pencere referansını alıyoruz
        self.init_ui()  # Arayüzü oluşturuyoruz

    def init_ui(self):
        layout = QVBoxLayout()  # Ana dikey layout
        layout.setContentsMargins(60, 40, 60, 40) # soldan 60px, üstten 40px, sağdan 60px, alttan 40px
        layout.setSpacing(20) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar

        # Spacer ile üstten ve alttan eşit genişleyebilen boşluk eklenerek içerik ortalanıyor
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Başlık
        title_label = QLabel("Hastane Yönetim Sistemine Hoş Geldiniz")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)

        # Spacer: Başlık ile butonlar arası
        layout.addSpacerItem(QSpacerItem(10, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Doktor Girişi Butonu
        doctor_login_button = QPushButton("🔓 Doktor Girişi")
        doctor_login_button.setStyleSheet("font-size: 20px; padding: 12px 24px;")
        doctor_login_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # butona tıklandığında çalışacak fonksiyon (doktor login ekranına git)
        doctor_login_button.clicked.connect(self.main_window.switch_to_doctor_login_scene)
        layout.addWidget(doctor_login_button, alignment=Qt.AlignCenter)

        # Spacer: Butonlar arası boşluk
        layout.addSpacing(20)

        # Yönetici Girişi Butonu
        admin_login_button = QPushButton("🧬 Yönetici Girişi")
        admin_login_button.setStyleSheet("font-size: 20px; padding: 12px 24px;")
        admin_login_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # butona tıklandığında çalışacak fonksiyon (admin login ekranına git)
        admin_login_button.clicked.connect(self.main_window.switch_to_admin_login_scene)
        layout.addWidget(admin_login_button, alignment=Qt.AlignCenter)

        # Spacer: Alt boşluk (dikey denge / üstle aynı)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)  # Layout'u pencereye uygula
    


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from service import ad_service as ad

class AdminLoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 80, 100, 80)
        layout.setSpacing(30)

        # Sol üst Geri Butonu
        top_bar = QHBoxLayout()
        back_button = QPushButton("← Geri")
        back_button.setStyleSheet("font-size: 15px; padding: 6px 12px;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.main_window.switch_to_home_scene)
        top_bar.addWidget(back_button, alignment=Qt.AlignLeft)
        layout.addLayout(top_bar)

        # Spacer üst
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Başlık
        title = QLabel("🧬 Yönetici Girişi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; padding: 10px;")

        subtitle = QLabel("Lütfen yönetici ID ve şifrenizi giriniz.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: gray; padding-bottom: 10px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Form
        form_wrapper_outer = QHBoxLayout()
        form_wrapper_outer.setAlignment(Qt.AlignCenter)

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(80, 30, 80, 20)
        self.form_layout.setSpacing(20)

        label_id = QLabel("Yönetici ID : ")
        label_id.setStyleSheet("font-size: 18px;")
        self.admin_id = QLineEdit()
        self.admin_id.setPlaceholderText("Yönetici ID")
        self.admin_id.setFixedHeight(45)
        self.admin_id.setStyleSheet("font-size: 16px; padding: 8px;")

        label_pass = QLabel("Şifre : ")
        label_pass.setStyleSheet("font-size: 18px;")
        self.admin_password = QLineEdit()
        self.admin_password.setPlaceholderText("Şifre")
        self.admin_password.setEchoMode(QLineEdit.Password)
        self.admin_password.setFixedHeight(45)
        self.admin_password.setStyleSheet("font-size: 16px; padding: 8px;")

        self.form_layout.addRow(label_id, self.admin_id)
        self.form_layout.addRow(label_pass, self.admin_password)

        self.login_button = QPushButton("🔑 Giriş Yap")
        self.login_button.setStyleSheet("font-size: 17px; padding: 10px 25px;")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.admin_enter)
        self.form_layout.addRow(self.login_button)

        self.alert = QLabel("")
        self.alert.setStyleSheet("color: red; font-size: 14px; padding-top: 8px;")
        self.alert.setVisible(False)
        self.form_layout.addRow(self.alert)

        form_wrapper = QWidget()
        form_wrapper.setLayout(self.form_layout)
        form_wrapper_outer.addWidget(form_wrapper)

        layout.addLayout(form_wrapper_outer)
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    # giriş butonuna tıklandığında çalışacak fonksiyon
    def admin_enter(self):
        admin_id = self.admin_id.text() # kullanıcının girdiği admin_id değeri
        admin_password = self.admin_password.text() # kullanıcının girdiği password değeri

        # Eğer hem ID hem şifre değeri boş değilse, login denemesi yapılacak
        if admin_id !='' and  admin_password !='':
            # service > ad_service.py > check_log_info()
            # login check fonksiyonu
            admin_name=ad.check_log_info(admin_id=admin_id, admin_password=admin_password)

            if admin_name:
                # eğer giriş başarılıysa
                # admin_id değerini güncelle
                self.main_window.admin_scene.admin_id.setText(self.admin_id.text())
                # yönetim paneli sahnesine geç
                self.main_window.switch_to_admin_panel_scene()
            else: 
                # eğer giriş başarılı değilse hata ekranı göster
                self.alert.setText("ID or password is wrong!!")
                self.alert.setVisible(True)
        else:
            # hem ID hem şifre değeri boşsa hata ekranı göster
            self.alert.setText("Enter your ID and Password please!")
            self.alert.setVisible(True)

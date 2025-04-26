from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from service import dr_service as dr

# doktor giriş ekranı

"""
Genel olarak;
1- "Kullanıcı ID" ve "Şifre" bilgilerini al
2- Giriş bilgileri doğruysa hastalar sahnesine geç
3- Yanlışsa hata mesajı göster
"""

class doctor_login_scene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window # ana pencereyi (app.py > DiagnosisApp) referans al
        self.init_ui() # Arayüz bileşenlerini oluşturan fonksiyonu çağırıyoruz

    # arayüz kurulumu
    def init_ui(self):
        layout = QVBoxLayout() # dikey bir layout oluşturuluyor 
        layout.setContentsMargins(100, 80, 100, 80) # soldan 100px, üstten 80px, sağdan 100px, alttan 80px
        layout.setSpacing(30) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar

        # Sol üst köşeye Geri butonu
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
        title = QLabel("👨‍⚕️ Doktor Girişi")
        title.setAlignment(Qt.AlignCenter) # ortaya hizala
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Lütfen giriş bilgilerinizi giriniz")
        subtitle.setAlignment(Qt.AlignCenter) # ortaya hizala
        subtitle.setStyleSheet("font-size: 16px; color: gray;")

        # title ve subtitle'ı widget olarak ekle
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Form düzeni
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(80, 30, 80, 20) # soldan 80px, üstten 30px, sağdan 80px, alttan 20px
        self.form_layout.setSpacing(20) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar

        label_id = QLabel("ID : ")
        label_id.setStyleSheet("font-size: 18px;")
        self.doctor_id = QLineEdit() # input oluştur
        self.doctor_id.setPlaceholderText("Doktor ID") # input placeholer(yazısı) ayarla
        self.doctor_id.setFixedHeight(45) # fix height(uzunluk) 35px olsun
        self.doctor_id.setFixedWidth(400)
        self.doctor_id.setStyleSheet("font-size: 16px; padding: 5px;")

        label_pass = QLabel("Şifre : ")
        label_pass.setStyleSheet("font-size: 18px;")
        self.doctor_password = QLineEdit() # input oluştur
        self.doctor_password.setPlaceholderText("Şifre") # input placeholer(yazısı) ayarla
        self.doctor_password.setEchoMode(QLineEdit.Password) # kutuya yazılanların **** olarak gözükmesini sağlıyoruz
        self.doctor_password.setFixedHeight(42) # fix height(uzunluk) 35px olsun
        self.doctor_password.setFixedWidth(400)
        self.doctor_password.setStyleSheet("font-size: 16px; padding: 5px;")

        self.form_layout.addRow(label_id, self.doctor_id)
        self.form_layout.addRow(label_pass, self.doctor_password)

        self.enter_button = QPushButton("Giriş Yap") # button oluştur
        self.enter_button.clicked.connect(self.doctor_enter) # butona tıklayınca doctor_enter() fonksiyonunu çalıştır
        self.enter_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.enter_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        self.form_layout.addRow(self.enter_button) # layout'a satır olarak ekle

        self.alert = QLabel("") # boş yazı alanı oluştur
        self.alert.setStyleSheet("color: red; font-size: 14px;")
        self.alert.setVisible(False) # alert alanını gizle
        self.form_layout.addRow(self.alert) # satır olarak ekle

        self.form = QWidget() # form widget'ı oluştur
        self.form.setLayout(self.form_layout) # form_layout kısmını form widget'a ekle

        layout.addWidget(self.form, alignment=Qt.AlignCenter) # form'u layoutta ortaya hizala

        # Spacer alt
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    # giriş butonuna tıklandığında çalışacak fonksiyon
    def doctor_enter(self):
        doctor_id=self.doctor_id.text() # kullanıcının girdiği doctor_id değeri
        doctor_password=self.doctor_password.text() # kullanıcının girdiği password değeri

        # Eğer hem ID hem şifre değeri boş değilse, login denemesi yapılacak
        if doctor_id !='' and  doctor_password !='':

            # service > dr_service.py > check_log_info()
            # login check fonksiyonu
            doctor_name=dr.check_log_info(doctor_id=doctor_id, doctor_password=doctor_password)

            if doctor_name:
                # eğer giriş başarılıysa
                # doctor_login.py > doctor_login_scene() içerisindeki (yani bu dosyadaki) doctor_id değerini güncelle
                self.main_window.doc_log.doctor_id.setText(self.doctor_id.text())
                # hasta sahnesine geç
                self.main_window.switch_to_patients_scene()
            else: 
                # eğer giriş başarılı değilse hata ekranı göster
                self.alert.setText("ID or password is wrong!!")
                self.alert.setVisible(True)
        else:
            # hem ID hem şifre değeri boşsa hata ekranı göster
            self.alert.setText("Enter your ID and Password please!")
            self.alert.setVisible(True)

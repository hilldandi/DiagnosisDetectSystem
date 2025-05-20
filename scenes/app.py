# PyQt5 kütüphanesinden kullanılacak widget sınıflarını import ediyoruz
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
# Bunu align işlemleri için kullancaz
from PyQt5.QtCore import Qt

# diğer sayfaları (sahneleri) import ediyoruz (modüler yapı)
import scenes.result_scene as  rs
import scenes.patients_scene as ls
import scenes.diagnosis_scene as ds
import scenes.doctor_login as dr
import scenes.home_scene as hm
import scenes.admin_login as ad
import scenes.admin_panel as adp

# main app
class DiagnosisApp(QMainWindow):
    def __init__(self):
        super().__init__() # QWidget'in kendi constructor'ı

        # ilk açılan ana penceredeki sayfa başlığı ve boyutlandırması
        self.setWindowTitle("Hospital Diagnosis System")
        self.setGeometry(100, 100, 800, 600)
        
        # sayfaları yönetmek için QStackedWidget oluşturuluyor
        # burda kart destesine benzer bi yapı var
        # her sahneyi oluşturuyor ama en üstte bu ekranı(self) açık tutuyor
        # istediğin zaman en üstteki kartı değiştirebiliyosun (diğer sahneleri aktif edebiliyosun)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # burda sahne nesnelerini (destedeki kartları) oluşturuyoruz
        self.home = hm.HomeScene(self)                      # anasayfa                  (home_scene.py > HomeScene())
        self.admin_scene = ad.AdminLoginScene(self)         # admin giriş ekranı        (admin_login.py > AdminLoginScene())
        self.admin_panel_scene = adp.AdminPanelScene(self) # admin panel ekranı        (admin_panel.py > AdminPanelScene())
        self.doc_log=dr.doctor_login_scene(self)            # doktor giriş ekranı       (doctor_login.py > doctor_login_scene())
        self.login_scene = ls.LoginScene(self)              # hasta giriş ekranı        (patients_scene.py > LoginScene())
        self.diagnosis_scene = ds.DiagnosisScene(self)      # teşhis ekranı             (diagnosis_scene.py > DiagnosisScene())
        self.results_scene = rs.ResultsScene(self)          # sonuç ekranı              (result_scene.py > ResultsScene())

        # login sayfasından(sahnesinden) girilen TC numarasını burda değişken olarak tutuyoruz (sonra kullancaz)
        self.tc_no= self.login_scene.tc_number
        
        # sahneleri bir deste haline getiriyoruz (QStackedWidget'a ekliyoruz)
        self.stacked_widget.addWidget(self.home)
        self.stacked_widget.addWidget(self.admin_scene)
        self.stacked_widget.addWidget(self.admin_panel_scene)
        self.stacked_widget.addWidget(self.login_scene)
        self.stacked_widget.addWidget(self.diagnosis_scene)
        self.stacked_widget.addWidget(self.results_scene)
        self.stacked_widget.addWidget(self.doc_log)

        # uygulama başladığında ilk (kart) olarak doktor login sahnesini gösteriyoruz
        self.stacked_widget.setCurrentWidget(self.home)

    # hastalar(patients) sahnesine/sayfasına giriş fonksiyonu
    def switch_to_patients_scene(self):
        self.login_scene.set_name()                             # karşılama mesajı için doktorun ismini düzenleyen fonksiyon (patients_scene.py > LoginScene.set_name())
        self.login_scene.get_all_patients()                     # doktorun tüm hastalarını db'den çeken fonksiyon (patients_scene.py > LoginScene.get_all_patients())
        self.login_scene.set_rating()                           # doktor rating bilgisini güncelleyen fonksiyon (patients_scene.py > LoginScene.set_rating())
        self.stacked_widget.setCurrentWidget(self.login_scene)  # hasta giriş ekranını göster
        

    # Teşhis sahnesine/sayfasına geçiş fonksiyonu (tc_no = hangi hastaya teşhis yapılacaksa onun kimlik numarası)
    def switch_to_diagnosis_scene(self, tc_no):
        self.diagnosis_scene = ds.DiagnosisScene(self, tc_no)           # Yeni diagnosis sahnesi oluşturuluyor (hasta bazlı, yani her hasta için farklı bilgiler içerecek)
        self.stacked_widget.addWidget(self.diagnosis_scene)             # her hasta için özel bir ekran oluştuğu için bunu da tekrar QStackedWidget'ın (destenin) içine ekliyoruz
        self.stacked_widget.setCurrentWidget(self.diagnosis_scene)      # teşhis ekranını göster
        self.diagnosis_scene.load_patient_diagnoses()                   # hastanın daha önceen yapılmış teşhislerini yüklüyor (tc_no ile sorgu yapıyor)

    # Sonuç sahnesine/sayfasına geçiş fonksiyonu
    def switch_to_results_scene(self):
        self.stacked_widget.setCurrentWidget(self.results_scene) # sonuç ekranını göster

    # Doktor login sahnesine/sayfasına geçiş fonksiyonu
    def switch_to_doctor_login_scene(self):
        self.doc_log.alert.setVisible(False)                    # ekranda hata mesajı varsa gizle
        self.doc_log.doctor_id.clear()                          # doktor giriş ekranındaki "Kullanıcı ID" kısmını resetle
        self.doc_log.doctor_password.clear()                    # doktor giriş ekranındaki "password" alanını resetle
        self.stacked_widget.setCurrentWidget(self.doc_log)      # doktor giriş ekranını göster

    # Admin login sahnesine/sayfasına geçiş fonksiyonu
    def switch_to_admin_login_scene(self):
        self.admin_scene.alert.setVisible(False)               # ekranda hata mesajı varsa gizle
        self.admin_scene.admin_id.clear()                      # admin giriş ekranındaki "Kullanıcı ID" kısmını resetle
        self.admin_scene.admin_password.clear()                # admin giriş ekranındaki "password" alanını resetle
        self.stacked_widget.setCurrentWidget(self.admin_scene) # admin login ekranını göster
    
    # Admin panel sahnesine/sayfasına geçiş fonksiyonu
    def switch_to_admin_panel_scene(self):
        self.admin_panel_scene.create_grafik_tab()
        self.admin_panel_scene.update_oran_tab()
        self.stacked_widget.setCurrentWidget(self.admin_panel_scene) # admin panel ekranını göster

    # Home sahnesine/sayfasına geçiş fonksiyonu
    def switch_to_home_scene(self):
        self.stacked_widget.setCurrentWidget(self.home) # anasayfa ekranını göster
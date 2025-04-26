from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
import service.patient_service as pt_ser , utility, service.dr_service as dr_service

class LoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window # ana pencereyi (app.py > DiagnosisApp) referans al
        self.rating = None

        self.init_ui() # UI başlat

    def init_ui(self):
        layout = QVBoxLayout() # dikey bir layout oluşturuluyor 
        layout.setContentsMargins(40, 30, 40, 30) # soldan 40px, üstten 30px, sağdan 40px, alttan 30px
        layout.setSpacing(20) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar

        # hoşgeldiniz mesajı
        self.name_box = QLabel("Hoşgeldiniz ")
        self.name_box.setAlignment(Qt.AlignLeft) # ortaya hizala
        self.name_box.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.name_box)

        # "Geri" ve "Hasta Aç" butonları için layout
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        # doktor puan gösterimi
        self.rating_box = QLabel("⭐Puanınız: -")
        self.rating_box.setAlignment(Qt.AlignCenter) # ortaya hizala
        self.rating_box.setStyleSheet("""
            font-size: 16px;
            padding: 8px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 6px;
            color: #333;
        """)
        
        # geri butonu
        back_button = QPushButton("← Geri")
        back_button.setStyleSheet("font-size: 16px; padding: 6px 14px;")
        back_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # butona tıklandığında çalışacak fonksiyon (doktor login ekranına geri dön)
        back_button.clicked.connect(self.main_window.switch_to_doctor_login_scene)
        
        # hastayı aç butonu
        self.search_button = QPushButton("🔍 Hastayı Aç")
        self.search_button.setStyleSheet("font-size: 16px; padding: 6px 14px;")
        self.search_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        self.search_button.setEnabled(False) # butonu disable et (şu anda kullanıcı basamasın)
        # butona tıklandığında çalışacak fonksiyon (teşhis ekranını getir)
        self.search_button.clicked.connect(self.OpenPatient) # (diagnosis_scene)

        hbox.addWidget(back_button, alignment=Qt.AlignLeft) # geri butonunu sola hizala ve hbox layout'una ekle
        hbox.addWidget(self.rating_box, alignment=Qt.AlignRight) # doktor puanını sağa hizala ve hbox layout'Una ekle
        hbox.addWidget(self.search_button, alignment=Qt.AlignRight) # hastayı aç butonunu sağa hizala ve hbox layout'una ekle

        layout.addLayout(hbox)

        # Hasta tablosu başlığı
        table_label = QLabel("🗂️ Kayıtlı Hasta Listesi")  
        table_label.setAlignment(Qt.AlignLeft) # sola hizala
        table_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(table_label) # widget'ı layout'a ekle 
        layout.addWidget(utility.create_horizontal_line()) # yatay ayırıcı çizgi ekliyoruz

        # Hasta tablosu (yüksekliği artırıldı)
        self.patients_table = QTableWidget() # table widget'ı oluştur
        self.patients_table.setColumnCount(4) # 4 sütunlu olacak
        self.patients_table.setHorizontalHeaderLabels(["TC Kimlik No", "Ad", "Soyad", "Tanı Sayısı"]) # sütun isimleri
        self.patients_table.horizontalHeader().setStretchLastSection(True) # tablodaki son sütun, kalan boşluğu tamamlasın (tablo ekranda tam gözüksün diye bu var)
        self.patients_table.setSelectionBehavior(QTableWidget.SelectRows) # seçilebilir satırlar olsun
        self.patients_table.setSelectionMode(QTableWidget.SingleSelection) # aynı anda tek satır seçilebilisin (birden fazla satır seçilemez)
        self.patients_table.setStyleSheet("font-size: 14px;")
        self.patients_table.setMinimumHeight(250)  # minimum yükseklik 250px
        # tablo içerisind yeni bir satır seçildiğinde bu fonksiyon çalışacak (hastayı aç butonunu aktif etme fonksiyonu)
        self.patients_table.itemSelectionChanged.connect(self.enable_search_button_if_selected)
        layout.addWidget(self.patients_table)



        # Yeni hasta form başlığı
        label = QLabel("👤 Yeni Hasta Ekleme")
        label.setAlignment(Qt.AlignLeft) # sola hizala
        label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(label)
        layout.addWidget(utility.create_horizontal_line()) # yatay ayırıcı çizgi ekliyoruz

        # Yeni hasta formu
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(20, 10, 20, 10) # soldan 20px, üstten 10px, sağdan 20px, alttan 10px
        self.form_layout.setSpacing(10) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar



        # Ortak bir stil belirlediğimiz fonksiyon
        # böylece her widget için ayrı bir stil vermeye uğraşmıyoruz
        def styled_lineedit(placeholder):
            le = QLineEdit()
            le.setPlaceholderText(placeholder) # placeholer parametresiyle verilen değeri placeholder olarak ayarla

            le.setFixedHeight(28) # fix yükseklik: 28px
            le.setStyleSheet("font-size: 13px; padding: 4px;")
            return le

        # TC Kimlik No, Ad, Soyad kısımlarının oluşturulması
        self.tc_number = styled_lineedit("TC Kimlik No")
        self.name_input = styled_lineedit("Ad")
        self.surname_input = styled_lineedit("Soyad")

        # Cinsiyet seçimi için "Erkek" ve "Kadın" seçimi bulunan ComboBox
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Erkek", "Kadın"])

        self.gender_combo.setFixedHeight(28) # fix yükseklik: 28px
        self.gender_combo.setStyleSheet("font-size: 13px;")
        self.gender_combo.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)

        # yaş kısmı
        self.age_input = styled_lineedit("Yaş")

        # kaydet butonu
        self.save_button = QPushButton("💾 Kaydet")
        self.save_button.setStyleSheet("font-size: 15px; padding: 6px 20px;")
        self.save_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # kaydet butonuna tıklandığında çalışacak fonksiyon (hastayı kaydet)
        self.save_button.clicked.connect(self.save_patient)

        # oluşturduğumuz widget'ları form_layout içerisine ekliyoruz
        self.form_layout.addRow("TC Kimlik No:", self.tc_number)
        self.form_layout.addRow("Ad:", self.name_input)
        self.form_layout.addRow("Soyad:", self.surname_input)
        self.form_layout.addRow("Cinsiyet:", self.gender_combo)
        self.form_layout.addRow("Yaş:", self.age_input)

        self.form_group = QWidget()
        self.form_group.setLayout(self.form_layout)
        self.form_group.setVisible(True) # form'un görünür yapıyoruz

        layout.addWidget(self.form_group)
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter) # kaydet butonunu layout'a ekle ve ortaya hizala

        self.setLayout(layout)

    # doktor rating bilgisini güncelleyen fonksiyon
    def set_rating(self):
        try:
            # (doctor_login.py > doctor_login_scene.doctor_id) burdaki kayıtlı olan doctor_id değerini çekiyoruz
            doctor_id_str = self.main_window.doc_log.doctor_id.text().strip() # strip = baştaki ve sondaki boşlukları siler

            # Eğer doktor ID'si yoksa veya sayısal değilse "-" şeklinde yazdır
            if not doctor_id_str or not doctor_id_str.isdigit():
                self.rating_box.setText("⭐ Doktor Puanı: -")
                return

            # doctor_id'yi int türüne çeviriyoruz
            doctor_id = int(doctor_id_str)
            # dr_service.py içerisindeki get_doctor_rating() fonksiyonuyla doktora ait rating değerini çekiyoruz
            rating = dr_service.get_doctor_rating(doctor_id)
            # rating değerini yazdırıyoruz
            self.rating_box.setText(f"⭐ Doktor Puanı: {rating} / 5.0")

        except Exception as e:
            # hata aldıysak hatayı terminale yazdırıyoruz, ekrana ise "-" olarak gösteriyoruz
            print(f"❌ set_rating hatası: {e}")
            self.rating_box.setText("⭐ Doktor Puanı: -")

    def set_name(self):
        try:
            # (doctor_login.py > doctor_login_scene.doctor_id) burdaki kayıtlı olan doctor_id değerini çekiyoruz
            doctor_id_str = self.main_window.doc_log.doctor_id.text().strip()
            # Eğer ID boşsa veya sayı değilse "doktor adı bilinmiyor" yazdırıyoruz
            if not doctor_id_str or not doctor_id_str.isdigit():
                self.name_box.setText("Doktor Adı: Bilinmiyor")
                return

            # doctor_id'yi int türüne çeviriyoruz
            doctor_id = int(doctor_id_str)
            # dr_service.py içerisindeki get_doctor_info() fonksiyonuyla doktora ait isim ve cinsiyet değerlerini çekiyoruz
            doctor_info = dr_service.get_doctor_info(doctor_id)

            if doctor_info:
                name = doctor_info[0] # isim

            else:
                # hata kontrolü, doctor_info boş döndüyse bilinmiyor yazdır
                name = "Dr. Bilinmiyor"

            # Düzenlenen doktor ismiyle birlikte ekrana bunu yazdır:
            self.name_box.setText(f"👨‍⚕️ Doktor: {name}")

        except Exception as e:
            # hata aldıysak hatayı terminale yazdırıyoruz, ekrana ise "doktor bilinmiyor" olarak gösteriyoruz
            print(f"❌ set_name hatası: {e}")
            self.name_box.setText("👨‍⚕️ Doktor: Bilinmiyor")

    # Giriş yapan doktora ait bütün hastaları tabloya yazdır
    def get_all_patients(self):
        # (doctor_login.py > doctor_login_scene.doctor_id) burdaki kayıtlı olan doctor_id değerini çekiyoruz
        doctor_id_str = self.main_window.doc_log.doctor_id.text().strip()
        # Eğer ID boşsa veya sayı değilse fonksiyonu durdur
        if not doctor_id_str or not doctor_id_str.isdigit():
            return

        # doctor_id'yi int türüne çeviriyoruz
        doctor_id = int(doctor_id_str)

        # giriş yapan doktorlara ait hastaları çek (patient_service.py > get_all_patinet())
        patients = pt_ser.get_all_patient(doctor_id)

        # her hasta için
        for p in patients:
            tc_no = p[0] # tc_no bilgisini al
            pt_ser.update_number_of_diagnoses(tc_no) # bu tc_no ile sorgu atarak, hastaya ait teşhis sayılarını getir

        # giriş yapan doktorlara ait hastaların GÜNCEL HALİNİ çek (patient_service.py > get_all_patinet())
        # çünkü her biri için ayrı fonksiyon çalıştırdık
        patients = pt_ser.get_all_patient(doctor_id)

        self.patients_table.setRowCount(len(patients)) # hastaların toplam sayısı kadar satır(row) oluştur
        self.patients_table.setColumnCount(4) # 4 tane sütun olacak
        self.patients_table.setHorizontalHeaderLabels(["TC Kimlik No", "Ad", "Soyad", "Teşhis Sayısı"]) # sütun isimleri

        # Döngüyle her hastayı tek tek tabloya yazıyoruz.
        for row_idx, (tc_no, name, surname, number_of_diagnoses) in enumerate(patients):
            self.patients_table.setItem(row_idx, 0, QTableWidgetItem(tc_no)) # 0 indexli sütuna tc_no gelecek
            self.patients_table.setItem(row_idx, 1, QTableWidgetItem(name)) # 1 indexli sütuna name  gelecek
            self.patients_table.setItem(row_idx, 2, QTableWidgetItem(surname)) # 2 indexli sütuna surname gelecek
            self.patients_table.setItem(row_idx, 3, QTableWidgetItem(str(number_of_diagnoses or 0))) # 3 indexli sütuna teşhis sayıları gelecek ("None" değer gelirse 0 yaz)

        
    def enable_search_button_if_selected(self):
        selected_row = self.patients_table.currentRow() #  tablo üzerinde hangi satırın seçildiğini buluyoruz (seçilmediyse -1 döner)
        self.search_button.setEnabled(selected_row != -1) # eğer dönen sonuç -1 değilse "Hastayı Aç" butonunu enable et

    # hastanın teşhis sayfasını açan fonksiyon 
    def OpenPatient(self):
        selected_row = self.patients_table.currentRow() # hasta tablosunda hangi satır seçilmiş onu alıyoruz
        if selected_row == -1:
            # eğer sonuç -1 dönmüşse satır seçilmemiş demektir, uyarı gösterip bu fonksiyondan çıkıyoruz
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçin.")
            return


        tc_item = self.patients_table.item(selected_row, 0)  # seçilen satırın ilk sütunundaki veriyi alıyoruz (yani tc_no)
        if tc_item:
            # eğer tc_no varsa, içeriğini tc_number diye ayrı bi değişkene alıyoruz
            tc_number = tc_item.text()
            # giriş yapmış olan doktorun id'sini alıyoruz
            self.doctor_id = self.main_window.doc_log.doctor_id.text()

            # patient_service.py içerisindeki get_patient() fonksiyonuyla
            # bu tc_no ve doctor_id ile bir hasta var mı kontrol ediyoruz
            is_there_patient = pt_ser.get_patient(tc_no=tc_number, doctor_id=self.doctor_id)

            if is_there_patient:
                # eğer hasta varsa diagnosis(teşhis) sayfasını açıyoruz
                self.main_window.switch_to_diagnosis_scene(tc_number)
        else:
            # hata kontrolü: seçilen satırın ilk sütununa veri yoksa uyarı veriyoruz
            QMessageBox.warning(self, "Hata", "Seçilen hasta verisi alınamadı.")

    # yeni hasta kaydetme fonksiyonu
    def save_patient(self):
        tc_no = self.tc_number.text() # formda tc_number inputundaki değeri tc_no olarak alıyoruz
        name = self.name_input.text() # formda name inputundaki değeri name olarak alıyoruz
        surname = self.surname_input.text() # formda surname inputundaki değeri surname olarak alıyoruz
        gender = self.gender_combo.currentText() # formda gender combobox'undaki değeri gender olarak alıyoruz
        self.doctor_id = self.main_window.doc_log.doctor_id.text() # şu an giriş yapmış olan doktorun id'sini alıyoruz
        age = self.age_input.text() # formda age inputundaki değeri age olarak alıyoruz
        number_of_diagnoses = 0 # teşhisleri default 0 olarak alıyoruz
    
        # Boş alan kontrolü
        if not (tc_no and name and surname and age):
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun.")
            return
    
        # TC No'nun 11 haneli ve sadece rakamlardan oluştuğunu kontrol et
        if not (tc_no.isdigit() and len(tc_no) == 11):
            QMessageBox.warning(self, "Hata", "TC Kimlik Numarası 11 haneli olmalıdır.")
            return
        
        # girilen yaşın rakamlaran oluşup oluşmadığını kontrol et
        if not (age.isdigit() ):
            QMessageBox.warning(self, "Hata", "Yaşı lütfen sayı olarak girin.")
            return
    
        # hasta kayıt fonksiyonunu çalıştırıyoruz
        if pt_ser.create_patient(tc_no, name, surname, gender, age, self.doctor_id, number_of_diagnoses) == 1:
            # sonuç 1 dönerse başarılı
            QMessageBox.information(self, "Başarılı", "Hasta kaydedildi.")
        else:
            # başka sonuç dönerse uyarı veriyoruz
            QMessageBox.warning(self, "Hata", "Bu TC Kimlik No zaten kayıtlı.")
    
        # Formdaki inputları sıfırla
        self.tc_number.setText('')
        self.name_input.setText('')
        self.surname_input.setText('')
        self.age_input.setText('')
        self.main_window.switch_to_patients_scene()
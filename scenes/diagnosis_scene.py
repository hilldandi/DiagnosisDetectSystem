

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,QComboBox, QPushButton, QMessageBox,QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout)
from PyQt5.QtCore import Qt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utility, service.medicine_service as ms , service.patient_service as pt_ser, service.diagnose_service as ds , service.dr_service as dr_service
import json
from scenes.follow_up_dialog import FollowUpDialog as fd 
import config as c

class DiagnosisScene(QWidget):
    def __init__(self, main_window, tc_no=None):  
        super().__init__()
        self.main_window = main_window # ana pencereyi (app.py > DiagnosisApp) referans al
        self.tc_no = tc_no # Hasta TC numarası
        self.diagnostic_trees = utility.load_diagnostic_trees() # diagnostic_trees çekiyoruz    (data > diagnostic_trees.json)
        self.follow_up_tree=utility.load_follow_up_tree() # follow_up_tree'yi çekiyoruz         (data > follow_up_questions.json)
        self.current_tree = None
        self.current_node = None
        self.questions_and_answers = [] # Soru-cevap geçmişi kaydı

        self.init_ui() # UI başlat
        

    def init_ui(self):
        layout = QVBoxLayout() # dikey bir layout oluşturuluyor 
        layout.setContentsMargins(40, 30, 40, 30) # soldan 40px, üstten 30px, sağdan 40px, alttan 30px
        layout.setSpacing(20) # widgetlar (buton, yazı vb.) arasındaki boşlukları ayarlar

        # NAVIGATION BAR LAYOUT
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)

        # Geri butonu
        back_button = QPushButton("← Geri")
        back_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setToolTip("Geri dönmek için tıklayın") # cursor'u ayarla (işaret eden el)
        # butona tıklandığında çalışacak fonksiyon (patients ekranına geri dön)
        back_button.clicked.connect(self.main_window.switch_to_patients_scene)
        nav_layout.addWidget(back_button, alignment=Qt.AlignLeft) # navbar layout'a butonu ekle ve sola hizala

        # Teşhisi değerlendir butonu
        self.eval_button = QPushButton("🩺 Teşhisi Değerlendir")
        self.eval_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        self.eval_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # butona tıklandığında bu fonksiyon çalışacak (teşhisi değerlendirme fonksiyonu)
        self.eval_button.clicked.connect(self.evaluate_diagnose)
        nav_layout.addWidget(self.eval_button, alignment=Qt.AlignRight) # navbar layout'a butonu ekle ve sağa hizala

        layout.addLayout(nav_layout)

        # Hasta teşhis geçmişi başlığı
        table_label = QLabel("📋 Hasta Teşhis Geçmişi")
        table_label.setAlignment(Qt.AlignLeft) # sola hizala
        table_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        layout.addWidget(table_label)
        layout.addWidget(utility.create_horizontal_line()) # yatay ayırıcı çizgi ekliyoruz

        # Teşhis geçmişi tablosu
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5) # 5 sütun olacak
        self.history_table.setHorizontalHeaderLabels(["Protokol Numarası", "Teşhis", "İlaç", "İyileşti mi?", "Memnuniyet Seviyesi"]) # sütun isimleri
        self.history_table.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.history_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft) # sola hizala
        self.history_table.horizontalHeader().setStretchLastSection(True) # tablodaki son sütun, kalan boşluğu tamamlasın (tablo ekranda tam gözüksün diye bu var)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows) # seçilebilir satırlar olsun
        self.history_table.setSelectionMode(QTableWidget.SingleSelection)  # aynı anda tek satır seçilebilisin (birden fazla satır seçilemez)
        self.history_table.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        self.history_table.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.history_table)

        layout.addWidget(utility.create_horizontal_line()) # yatay ayırıcı çizgi ekliyoruz

        # Teşhis ağacı seçimi başlığı
        layout.addSpacing(10)
        layout.addWidget(QLabel("Teşhis ağacını seçin ve soruları cevaplayın:", alignment=Qt.AlignCenter))
        
        # Teşhis ağacı combobox'ı
        self.tree_combo = QComboBox()
        self.tree_combo.setStyleSheet("font-size: 16px; padding: 5px;")
        self.tree_combo.addItems(self.diagnostic_trees.keys())
        self.tree_combo.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        layout.addWidget(self.tree_combo, alignment=Qt.AlignCenter)

        self.select_tree_button = QPushButton("Ağacı Seç")
        self.select_tree_button.setStyleSheet("font-size: 16px; padding: 8px 16px;")
        self.select_tree_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        # butona tıklandığında bu fonksiyon çalışacak (teşhis ağacını yükleyip soruları başlatan fonksiyon)
        self.select_tree_button.clicked.connect(self.load_tree_diagnoses)
        layout.addWidget(self.select_tree_button, alignment=Qt.AlignCenter) # widget'ı layout'a ekle ve ortaya hizala

        #SORU GÖSTERİMİ
        self.question_label = QLabel("") # boş bi label oluşturuyoruz (soruyu burda göstercez)
        self.question_label.setAlignment(Qt.AlignCenter) # ortaya hizala
        self.question_label.setStyleSheet("font-size: 18px; padding: 10px; color: #333;")
        layout.addWidget(self.question_label)

        #EVET / HAYIR Butonlarının Layoutu
        hbox_yes_no = QHBoxLayout() 
        hbox_yes_no.setSpacing(40)

        # Evet Butonu
        self.yes_button = QPushButton("Evet")
        self.yes_button.setStyleSheet("font-size: 16px; padding: 8px 20px;")
        self.yes_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        self.yes_button.clicked.connect(lambda: self.answer_question("yes")) # tıklanınca answer_question() fonksiyonunu çağır (param=yes)
        self.yes_button.setVisible(False) # butonu gizle

        # Hayır butonu
        self.no_button = QPushButton("Hayır")
        self.no_button.setStyleSheet("font-size: 16px; padding: 8px 20px;")
        self.no_button.setCursor(Qt.PointingHandCursor) # cursor'u ayarla (işaret eden el)
        self.no_button.clicked.connect(lambda: self.answer_question("no")) # tıklanınca answer_question() fonksiyonunu çağır (param=no)
        self.no_button.setVisible(False) # butonu gizle

        hbox_yes_no.addWidget(self.no_button)
        hbox_yes_no.addWidget(self.yes_button)

        layout.addLayout(hbox_yes_no)

        #Layout'u uygula
        self.setLayout(layout)


    # Seçilen teşhisi değerlendirme fonksiyonu
    def evaluate_diagnose(self):
        # seçili olan teşhisi al 
        selected_row = self.history_table.currentRow()
        if selected_row == -1:
            # teşhis seçilmediyse (sonuç -1 ise) uyarı ver
            QMessageBox.warning(self, "Uyarı", "Lütfen bir teşhis seçin.")
            return
        
        healed= self.history_table.item(selected_row, 3).text()
        if healed.lower() == "no" or (healed == None or healed ==""):
            # Eğer hasta iyileşmediyse takip diyalogunu aç
            with open(c.FollowUp_Path, "r", encoding="utf-8") as file:
                followup_data = json.load(file)
            
            # seçili satırın 0. sütunundaki "protokol numarası"nı alıyoruz
            protocol_item = self.history_table.item(selected_row, 0)  
            protocol_number = protocol_item.text()

            # takip diyaloğundaki soruları ve seçenekleri (followup_data), 
            # seçili hastanın teşhis protokol numarası (protocol_number),
            # değerlerini alıp FollowUpDialog sınıfı üretiyoruz (scenes > follow_up_dialog.py)
            dialog = fd(followup_data, protocol_number, self)
            result = dialog.exec_()

            # şu anda giriş yapılan doktorun id'sini alıyoruz
            doctor_id = self.main_window.doc_log.doctor_id.text()
            
            
            if result == QDialog.Accepted:
                # takip verileri kaydedildiyse
                healed = dialog.are_you_healed # hasta iyileşti mi ?
                satisfaction = dialog.satisfaction_level # memnuniyet seviyesi
                dr_service.calculate_doctor_rating(doctor_id) # doktor rating oranını tekrar hesapla
                self.load_patient_diagnoses() # hastanın teşhslerini yükle

                # eğer hasta iyileşti mi kısmı ve memnuniyet seviyesi boş değilse
                if healed is not None and satisfaction is not None:
                    # seçili tablonun 0. indexindeki sütunu (Prtokol Numarası) alıyoruz ve int türüne çeviriyoruz
                    diagnose_id_item = self.history_table.item(selected_row, 0)
                    diagnose_id = int(diagnose_id_item.text()) 
                    # hastanın teşhis kaydını güncelliyoruz
                    ds.update_diagnose(healed, satisfaction, diagnose_id)     
            else:
                # takip verileri kaydedilmediyse:
                QMessageBox.information(self, "İptal", "Değerlendirme iptal edildi.")
        else:
            # hasta iyileşmişse:
            QMessageBox.information(self, "Bilgi", "Bu hasta zaten iyileşmiş.")

    # Memnuniyet seviyesi gönderildi fonksiyonu
    def submit_satisfaction(self, level):
        self.questions_and_answers.append(("Satisfaction Level", str(level)))
        QMessageBox.information(self, "Teşekkürler", f"{level} seviyesindeki geri bildiriminiz için teşekkür ederiz.\nGeçmiş olsun!")
        self.follow_up_popup.accept() # kullanıcının memnuniyet verisi girdiğiyle ilgili işaretleme

    # Hastanın geçmiş teşhis kayıtlarını tabloya yükleyen fonksiyon
    def load_patient_diagnoses(self):
        # şu anda giriş yapılan doktorun id'sini alıyoruz
        doctor_id= self.main_window.doc_log.doctor_id.text()
        tc_no = self.tc_no

        # db'den bu hasta ve doktora ait teşhisleri çekiyoruz
        diagnoses = ds.get_diagnoses(tc_no,doctor_id) 

        self.history_table.setRowCount(len(diagnoses)) # tablonun satır sayısı teşhis sayısı kadar olacak
        # her teşhisi tabloya pushluyoruz
        for row_idx, (protocol_number, final_diagnosis, medicine, are_you_healed, satisfaction_level) in enumerate(diagnoses):
            self.history_table.setItem(row_idx, 0, QTableWidgetItem(str(protocol_number))) # 0 indexli sütuna protocol_number gelecek
            self.history_table.setItem(row_idx, 1, QTableWidgetItem(str(final_diagnosis) if final_diagnosis else "")) # 1 indexli sütuna final_diagnosis gelecek, yoksa boş
            self.history_table.setItem(row_idx, 2, QTableWidgetItem(str(medicine) if medicine else "")) # 1 indexli sütuna medicine gelecek, yoksa boş
            self.history_table.setItem(row_idx, 3, QTableWidgetItem(str(are_you_healed) if are_you_healed else "")) # 1 indexli sütuna are_you_healed gelecek, yoksa boş
            self.history_table.setItem(row_idx, 4, QTableWidgetItem(str(satisfaction_level) if satisfaction_level is not None else "")) # 4 indexli sütuna memnuniyet seviyesi gelcek, yoksa boş

    # Seçilen teşhis ağacını yükleyip soruları başlatan fonksiyon
    def load_tree_diagnoses(self):
        tree_name = self.tree_combo.currentText() # combobox üzerinde seçilen teşhis ağacının adını yazıyoruz
        # daha önce yüklediğimiz JSON formatınaki teşhis ağacının içinden (data > diagnostic_trees.json)
        # seçili olan teşhis ağacının adını alıyoruz
        self.current_tree = self.diagnostic_trees.get(tree_name)
        self.current_node = self.current_tree  
        # yeni bir liste oluşturduk ve soru-cevap sürecini başlattık
        self.questions_and_answers = []
        self.next_question()

    # Sıradaki soruyu gösteren fonksiyon
    def next_question(self):
        """Display the next question or diagnosis result."""
        if isinstance(self.current_node, dict):
            # eğer current_node bir sözlük(dict) ise (bu bir soru içeriyor demektir)
            question = list(self.current_node.keys())[0] # soruyu alıyoruz
            self.question_label.setText(question) # soruyu ekranda göster (question_label içine yaz) 
            self.yes_button.setVisible(True) # evet butonunu aktif hale getir
            self.no_button.setVisible(True) # hayır butonunu aktif hale getir
        else:
            # eğer current_node sözlük değilse (final teşhis geldi demektir)
            self.question_label.setText(f"Teşhis: {self.current_node}") # ekrana teşhis adını yaz
            self.yes_button.setVisible(False) # evet butonunu gizle
            self.no_button.setVisible(False) # hayır butonunu gizle
            self.save_diagnosis(self.current_node) # teşhisi db'ye kaydet
            self.question_label.setText('') # question_label'ı sil

    def answer_question(self, answer):
        """Process the user's answer and navigate the tree."""
        if isinstance(self.current_node, dict):
            # eğer current_node bir sözlük(dict) ise (bu bir soru içeriyor demektir)
            question = list(self.current_node.keys())[0] # soruyu alıyoruz
            self.questions_and_answers.append((question, answer)) # soruyu ve cevabı questions_and_answers listesine kaydediyoruz
            self.current_node = self.current_node[question].get(answer) # bir sonraki node'a geçiyoruz
            self.next_question() # yeni node'a göre tekrar işlemleri yapıyoruz

    # Teşhisi db'ye kaydeden fonksiyon
    def save_diagnosis(self, final_diagnosis):
        # şu anda giriş yapılan doktorun id'sini alıyoruz
        doctor_id = self.main_window.doc_log.doctor_id.text()
        tc_no = self.tc_no

        # kullanıcının sorulara verdiği cevapları (questions_and_answers) JSON'a çeviriyoruz
        qa_str = json.dumps(self.questions_and_answers, ensure_ascii=False)
        # hastayı db'de bul
        patient = pt_ser.get_patient(tc_no, doctor_id)
        if not patient:
            # bulunamıyorsa uyarı ver, fonksiyondan çık
            QMessageBox.warning(self, "Hata", "Hasta bulunamadı.")
            return

        # hasta adı ve soyadını birleştir
        patient_name = f"{patient[0]} {patient[1]}"
        # yeni bi protokol numarası üret
        protocol_number = utility.generate_protocol_number()

        # final teşhise uygun bir ilaç varsa onu çekiyoruz (service > medicine_service.py > get_medicine())
        medicine = ms.get_medicine(final_diagnosis) if final_diagnosis else ""
        # henüz iyileşmediği için noyazıp memnuniyet puanını 0 giriyoruz
        are_you_healed = None
        satisfaction_level = None

        # db'ye yeni teşhis kaydı ekliyoruz
        pt_ser.create_patient_record(protocol_number,doctor_id,patient_name,tc_no,qa_str,final_diagnosis,are_you_healed,medicine,satisfaction_level)
        
        # kullanıcının teşhis sayısını 1 artır
        pt_ser.update_number_of_diagnoses(tc_no)

        # teşhisin eklendiğiyle ilgili uyarı ekranı gösteriyoruz
        QMessageBox.information(self, f"Teşhis: {final_diagnosis}", f"Teşhis başarıyla kaydedildi. Protokol Numarası: {protocol_number}.")
        # hasta geçmiş tablosunu yeniliyoruz
        self.load_patient_diagnoses()

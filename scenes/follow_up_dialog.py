from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QTimer
from service.diagnose_service import update_diagnose

class FollowUpDialog(QDialog):
    def __init__(self, followup_data: dict, protocol_number: str, parent=None):
        super().__init__(parent)
        self.protocol_number = protocol_number # hangi teşhis kaydı için çalışıyoruz onu tutuyoruz

        # cevapları tutulacak değişkenler
        self.did_you_take_medicine = None
        self.are_you_healed = None
        self.satisfaction_level = None

        # Dialog penceresinin özellikleri
        self.setWindowTitle("Takip Soruları")
        self.setMinimumSize(400, 300)

        # JSON'dan gelen takip sorularını yüklüyoruz
        self.data = followup_data
        self.current_node = self.data["Follow up Questions"]

        # Ana layout'u başlatıyoruz
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        # Üstteki bilgilendirme etiketi
        self.label = QLabel("Takip sorularını cevaplayın:")
        self.label.setAlignment(Qt.AlignCenter) # ortaya hizala
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.label)

        # Ana soru
        self.question_label = QLabel("")
        self.question_label.setAlignment(Qt.AlignCenter) # ortaya hizala
        self.question_label.setStyleSheet("font-size: 18px; padding: 8px; color: #222;")
        self.layout.addWidget(self.question_label)

        # Geri sayım alanı
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignCenter) # ortaya hizala
        self.countdown_label.setStyleSheet("font-size: 14px; color: gray;")
        self.layout.addWidget(self.countdown_label)

        # Evet / Hayır butonları
        self.yes_button = QPushButton("Evet")
        self.no_button = QPushButton("Hayır")
        # iki buton için de bu özellikleri ekle:
        for btn in (self.yes_button, self.no_button):
            btn.setStyleSheet("font-size: 15px; padding: 8px 20px;")
            btn.setVisible(False) # butonları gizle
            self.layout.addWidget(btn, alignment=Qt.AlignCenter) # ortaya hizala

        # Butonlara tıklanınca hangi fonksiyon çalışacak onları belirliyoruz
        self.yes_button.clicked.connect(lambda: self.handle_answer("yes")) # handle_answer() fonksiyonu (param=yes)
        self.no_button.clicked.connect(lambda: self.handle_answer("no")) # handle_answer() fonksiyonu (param=no)

        # Skor seçimi için combobox
        self.score_combo = QComboBox()
        self.score_combo.addItems(["1", "2", "3", "4", "5"]) # 1-5 arası skorlar
        self.score_combo.setStyleSheet("font-size: 15px; padding: 4px;")
        self.score_combo.setVisible(False)

        # Skor gönderme butonu
        self.submit_score = QPushButton("💾 Gönder")
        self.submit_score.setStyleSheet("font-size: 15px; padding: 8px 20px;")
        self.submit_score.setVisible(False) # butonu gizle

        self.layout.addWidget(self.score_combo, alignment=Qt.AlignCenter) # ortaya hizalayarak layout'a ekle
        self.layout.addWidget(self.submit_score, alignment=Qt.AlignCenter) # ortaya hizalayarak layout'a ekle

        # Skor gönder butonuna tıklanınca çalışan fonksiyon
        self.submit_score.clicked.connect(self.submit_score_selected)

        # İlk soruyla başla
        self.show_question(self.current_node)

    def show_question(self, node):
        """Gelen node'a göre yeni soru veya mesaj gösterimi yapar."""
        if isinstance(node, str):
            # Bu bir sonuç mesajıysa (tüm butonları gizle  ve node'u ekrana yazdır)
            self.question_label.setText(node)
            self.yes_button.setVisible(False)
            self.no_button.setVisible(False)
            self.score_combo.setVisible(False)
            self.submit_score.setVisible(False)
            self.start_countdown(2) # 2 saniyelik geri sayım başlatıyoruz
        elif isinstance(node, dict):
            # eğer bir soru mesajıysa
            self.countdown_label.setText("")
            question = list(node.keys())[0] # soruyu al
            self.question_label.setText(question) # soruyu ekranda göster
            self.current_question = question
            self.current_node = node[question]

            # Skor sorusu mu?
            if all(k in ["1", "2", "3", "4", "5"] for k in self.current_node.keys()):
                # evet ise yes no butonlarını gizle, score ve submit butonlarını göster
                self.yes_button.setVisible(False)
                self.no_button.setVisible(False)
                self.score_combo.setVisible(True)
                self.submit_score.setVisible(True)
            else:
                # hayır ise score submit butonlarını gizle, yes no butonlarını göster
                self.score_combo.setVisible(False)
                self.submit_score.setVisible(False)
                self.yes_button.setVisible("yes" in self.current_node)
                self.no_button.setVisible("no" in self.current_node)

    def handle_answer(self, answer):
        """Evet/Hayır cevabına göre yönlendirme yapar ve gerekli verileri toplar."""

        if self.current_question == "Did you take the medicine?" or self.current_question == "İlacınızı aldınız mı?":
            self.did_you_take_medicine = answer

        elif self.current_question == "Are you healed" or self.current_question == "İyileştiniz mi?":
            self.are_you_healed = answer

        # sonraki soruya geç
        next_node = self.current_node.get(answer)
        self.show_question(next_node)

    def submit_score_selected(self):
        """Skor gönderildiğinde veritabanına kaydeder ve sonucu gösterir."""
        score = int(self.score_combo.currentText())
        self.satisfaction_level = score

        # final mesajını göster
        final_message = self.current_node.get(str(score), "Teşekkürler!")
        self.show_question(final_message)

        # veritabanında güncelleme yap
        result_message = update_diagnose(self.are_you_healed, self.satisfaction_level, self.protocol_number)
        self.label.setText(result_message)

        # pencereyi 2 saniye içinde kapat
        self.start_countdown(2)

    def start_countdown(self, seconds):
        """Dialog'u belirli saniye sonra otomatik kapatır."""
        self.remaining_seconds = seconds
        self.countdown_label.setText(f"Pencere {self.remaining_seconds} saniye içinde kapanacak...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000) # 1 saniyede bir güncelle

    def update_countdown(self):
        """Geri sayım bitince pencereyi kapatır."""
        self.remaining_seconds -= 1
        if self.remaining_seconds > 0:
            self.countdown_label.setText(f"Pencere {self.remaining_seconds} saniye içinde kapanacak...")
        else:
            self.timer.stop()
            self.accept() # Dialog'u kapat

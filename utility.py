import service.patient_service as pt_ser
import json
import config as c
from PyQt5.QtWidgets import QFrame
import datetime  # Tarih işlemleri için

# Protokol numarası oluşturma fonksiyonu
def generate_protocol_number():
    today = datetime.datetime.now() # Şu anki tarih ve saat bilgisini alıyoruz
    date_prefix = today.strftime("%Y%m%d")  # '20250408' formatında (string)

    # Aynı gün içerisinde kaçıncı teşhis olduğunu buluyoruz (hasta sayısı gibi düşün)
    count = pt_ser.get_patient_number( today.year, today.month, today.day)

    # Tarih + o günkü sıra numarası (örneğin: 2025040801) şeklinde protokol numarası üretiyoruz
    protocol_number = f"{date_prefix}{count:02d}"
    return protocol_number

# Teşhis ağaçlarını yükleme fonksiyonu
def load_diagnostic_trees():
    # Belirlenen dosya yolundan (Diagnose_Path) JSON formatında teşhis ağaçlarını okuyoruz
    with open(c.Diagnose_Path, 'r', encoding='utf-8') as file:
        diagnostic_trees = json.load(file)
    return diagnostic_trees # Yüklenen teşhis ağaçlarını döndürüyoruz

# Takip ağacını yükleme fonksiyonu
def load_follow_up_tree():
    # Belirlenen dosya yolundan (FollowUp_Path) JSON formatında takip ağaçlarını okuyoruz
    with open(c.FollowUp_Path, 'r', encoding='utf-8') as file:
        follow_up_tree = json.load(file)
    return follow_up_tree # Yüklenen takip ağacını döndürüyoruz

# Yatay çizgi (separator) oluşturma fonksiyonu
def create_horizontal_line():
    line = QFrame() # QFrame nesnesi oluşturuyoruz
    line.setFrameShape(QFrame.HLine) # Çerçeve şeklini yatay çizgi (HLine) olarak ayarlıyoruz
    line.setFrameShadow(QFrame.Sunken) # Çizgiye gölgeli bir efekt veriyoruz (gömülü görünüm)
    line.setLineWidth(2) # Çizginin kalınlığını 2px olarak ayarlıyoruz
    return line # Oluşturulan yatay çizgiyi döndürüyoruz

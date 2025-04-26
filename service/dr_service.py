import sqlite3
import datetime, os
import config as c
from service.db_setup import query_executer

# doktor login doğrulama fonksiyonu
def check_log_info(doctor_id, doctor_password):
    # doctors tablosunda doctor_id ve doctor_password eşleşen bir kayıt arıyoruz
    result = query_executer('''
        SELECT doctor_name FROM doctors WHERE doctor_id = ? AND doctor_password = ?
    ''', (doctor_id, doctor_password))
    
    # eğer bulabilirsek sadece doctor_name değerini döndürüyoruz
    # bulamazsak None değer döndürüyoruz
    return result[0] if result else None

def get_doctor_info(doctor_id):
    # Sadece ID'ye göre doktorun adını ve cinsiyetini çekiyoruz
    result = query_executer('''
        SELECT doctor_name, doctor_gender FROM doctors WHERE doctor_id = ?
    ''', (doctor_id,))
    
    # bulamazsak None değer döndürüyoruz
    return result if result else None

# doktor rating puanı hesaplama fonksiyonu
def calculate_doctor_rating(doctor_id):
    try:
        conn = sqlite3.connect(c.DB_PATH)
        cursor = conn.cursor()

        # diagnoses(teşhisler) tablosundan o doktorun yaptığı teşhislerdeki memnuniyet puanlarını çekiyo
        # Sıfır olmayan memnuniyet puanlarını al
        cursor.execute("""
            SELECT satisfaction_level FROM diagnoses
            WHERE doctor_id = ? AND satisfaction_level != 0
        """, (doctor_id,))
        scores = [row[0] for row in cursor.fetchall()]

        # Ortalama hesapla
        if scores:
            rating = sum(scores) / len(scores)
        else:
            rating = 0

        # doctors tablosunda rating'i güncelle
        cursor.execute("""
            UPDATE doctors
            SET rating = ?
            WHERE doctor_id = ?
        """, (rating, doctor_id))

        conn.commit()
        conn.close()

        return round(rating, 2)
    except Exception as e:
        print(f"Rating hesaplanırken hata oluştu: {e}")
        return None

def get_doctor_rating(doctor_id):
    # Doktorun en güncel rating değerini veritabanından çekiyoruz
    result = query_executer('''
        SELECT rating FROM doctors WHERE doctor_id = ?
    ''', (doctor_id,))

    # Rating bulunamazsa 0.0 döndürüyoruz
    # Bulunan değer virgülden sonra 2 basamağa yuvarlanır (örn: 4.7685 => 4.77)
    return round(result[0], 2) if result and result[0] is not None else 0.0
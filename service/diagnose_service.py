import sqlite3
from service.db_setup import query_executer
import config as c

# hastanın iyileşmediğini kontrol eden fonksiyon
# returns => protocol_number, final_diagnosis
def check_are_you_healed(tc_no, doctor_id):
    return query_executer("""
        SELECT protocol_number, final_diagnosis
        FROM diagnoses
        WHERE tc_no = ? AND doctor_id = ? AND LOWER(are_you_healed) = 'no'
    """, (tc_no, doctor_id))

# db'den tüm teşhisleri getiren fonksiyon
def get_diagnoses(tc_no,doctor_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT protocol_number, final_diagnosis, medicine , are_you_healed, satisfaction_level FROM diagnoses WHERE tc_no = ? AND doctor_id = ?",
        (tc_no, doctor_id)
    )
    diagnoses = cursor.fetchall()
    conn.close()
    return diagnoses

# teşhis güncelleme fonksiyonu
def update_diagnose(healed, satisfaction, protocol_number):
    try:
        query_executer("""
            UPDATE diagnoses
            SET are_you_healed = ?, satisfaction_level = ?
            WHERE protocol_number = ?
        """, (healed, satisfaction, protocol_number))
        return "Değerlendirme başarıyla kaydedildi."
    except Exception as e:
        return f"Veritabanı hatası: {str(e)}"
    
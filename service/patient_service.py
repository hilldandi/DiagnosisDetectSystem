import sqlite3
import datetime, os
import config as c

from service.db_setup import query_executer

# Hastanin teşhis sayısını getiren fonksiyon
def get_number_of_diagnoses(tc_no):
    # Hastanın toplam teşhis sayısını öğreniyoruz
    count_result = query_executer("SELECT COUNT(*) FROM diagnoses WHERE tc_no = ?", (tc_no,))
    count = count_result[0] if count_result else 0
    return count

# Teşhis sayısını hastanın kaydına güncelleyen fonksiyon
def update_number_of_diagnoses(tc_no):
    # Hastanın toplam teşhis sayısını öğreniyoruz
    count = int(get_number_of_diagnoses(tc_no))

    # Bu sayıyı hastalar tablosunda güncelliyoruz
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients
        SET number_of_diagnoses = ?
        WHERE tc_no = ?
    """, (count, tc_no))
    conn.commit()
    conn.close()


# Belirli bir doktora ait tüm hastaları getiren fonksiyon
def get_all_patient(doctor_id):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tc_no, name, surname,number_of_diagnoses FROM patients WHERE doctor_id = ?",(doctor_id,))
    patients = cursor.fetchall() # hepsini getir
    conn.close()
    return patients

# Yeni hasta oluşturan fonksiyon
def create_patient(tc_no, name, surname, gender, age, doctor_id, number_of_diagnoses):
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (tc_no, name, surname, gender, age, doctor_id, number_of_diagnoses) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tc_no, name, surname, gender, int(age), doctor_id, number_of_diagnoses)
        )
        conn.commit()
        return 1 # Kayıt başarılıysa 1 dön
    except sqlite3.IntegrityError:
        return 0 # TC zaten kayıtlıysa 0 dön
    finally:
        conn.close()


# Belirli bir doktorun belirli bir hastasını getiren fonksiyon
def get_patient(tc_no,doctor_id):
    return query_executer("SELECT name, surname FROM patients WHERE tc_no = ? AND doctor_id = ?", (tc_no, int(doctor_id)))

# Yeni teşhis kaydı oluşturan fonksiyon
def create_patient_record(protocol_number,doctor_id, patient_name, tc_no, questions_and_answers_str, final_diagnosis,are_you_healed,medicine, satisfaction):
    print(protocol_number,doctor_id, patient_name, tc_no, questions_and_answers_str, final_diagnosis,are_you_healed,medicine, satisfaction)
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Anlık tarih saat bilgisi
        conn = sqlite3.connect(c.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diagnoses 
            (date, protocol_number,doctor_id, patient_name, tc_no, questions_and_answers, final_diagnosis,medicine,are_you_healed,satisfaction_level)
            VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?)
        ''', (date,protocol_number,doctor_id, patient_name, tc_no, questions_and_answers_str, final_diagnosis, medicine, are_you_healed, satisfaction))
        conn.commit()
        conn.close()
        print("Kayıt başarıyla eklendi.")
    except sqlite3.Error as e:
        print("SQLite hatası (create):", e)
    finally:
        conn.close()

# Var olan bir teşhis kaydını güncelleyen fonksiyon
def update_patient_record(protocol_number, doctor_id, patient_name, tc_no, questions_and_answers_str, final_diagnosis, are_you_healed, medicine, satisfaction):
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(c.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE diagnoses 
            SET date = ?, doctor_id = ?, patient_name = ?, tc_no = ?, questions_and_answers = ?, final_diagnosis = ?, medicine = ?, are_you_healed = ?, satisfaction_level = ?
            WHERE protocol_number = ?
        ''', (date, doctor_id, patient_name, tc_no, questions_and_answers_str, final_diagnosis, medicine, are_you_healed, satisfaction, protocol_number))

        if cursor.rowcount == 0:
            print("Güncellenecek kayıt bulunamadı.")
        else:
            print("Kayıt başarıyla güncellendi.")
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite hatası (update):", e)
    finally:
        conn.close()

# Belirli bir gün için kaç adet teşhis yapıldığını getiren fonksiyon
def get_patient_number( year, month, day):
    date_pattern = f"{year}-{month:02}-{day:02}%"  # Örn: 2025-04-25%
    count_result = query_executer("SELECT COUNT(*) FROM diagnoses WHERE date LIKE ?", (date_pattern,))
    return (count_result[0] + 1) if count_result else 1  # Yeni kayıt numarası için 1 ekleniyor


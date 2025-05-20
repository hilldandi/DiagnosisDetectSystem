import sqlite3

# Veritabanı yolunu belirt
db_path = "data/hospital.db"

# Silinecek satırın ID'si
diagnosis_id = 41  # Burayı değiştirebilirsin

# Bağlantı oluştur
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Silme işlemi
cursor.execute("DELETE FROM diagnoses WHERE id = ?", (diagnosis_id,))
conn.commit()
conn.close()

print(f"ID'si {diagnosis_id} olan kayıt silindi.")

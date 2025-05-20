import sqlite3
import pandas as pd

# Veritabanını bağla
conn = sqlite3.connect('data/hospital.db')

# 'diagnoses' tablosunu oku
df = pd.read_sql_query("SELECT * FROM diagnoses", conn)

# UTF-8 formatında CSV olarak dışa aktar
df.to_csv('diagnoses_export.csv', index=False, encoding='utf-8')

# Bağlantıyı kapat
conn.close()

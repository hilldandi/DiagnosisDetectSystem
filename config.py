import os

# Amaç: Projedeki önemli dosya yollarını merkezi bir yerde tanımlamak


# BASE_DIR: config.py dosyasının bulunduğu klasörü temsil eder (constant value)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DB_PATH: Veritabanı dosyasının tam yolu (örnek: /home/kullanici/proje/data/hospital.db)
DB_PATH = os.path.join(BASE_DIR, 'data/hospital.db')

# SQL script dosyasının yolu (tablo oluşturma vb. SQL kodları burda)
SQL_PATH = os.path.join(BASE_DIR, 'data/init_db.sql')

# Teşhis karar ağacı verisinin yolu
Diagnose_Path = os.path.join(BASE_DIR, 'data/diagnostic_trees.json')

# Takip sorularının bulunduğu JSON dosyasının yolu
FollowUp_Path = os.path.join(BASE_DIR, 'data/follow_up_questions.json')
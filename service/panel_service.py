import sqlite3
import config as c

# Veritabanından doktor değerlendirme istatistiklerini çekme fonksiyonu
def get_doctor_review_stats():
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()
    # doktor ismi, toplam değerlendirme sayısı, iyileşen sayısı, iyileşmeyen sayısı
    cursor.execute("""
        SELECT d.doctor_name,
               COUNT(r.id) as total_reviews,
               SUM(CASE WHEN LOWER(r.are_you_healed) = 'yes' THEN 1 ELSE 0 END) as iyilesen,
               SUM(CASE WHEN LOWER(r.are_you_healed) = 'no' THEN 1 ELSE 0 END) as iyilesmeyen
        FROM doctors d
        LEFT JOIN diagnoses r ON d.doctor_id = r.doctor_id
        WHERE r.satisfaction_level IS NOT NULL
        GROUP BY d.doctor_id
    """)

    results = cursor.fetchall()
    conn.close()
    return results

# tüm doktorların skorlarını al
def get_all_doctor_ratings():
    conn = sqlite3.connect(c.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT doctor_name, rating
        FROM doctors
    """)

    results = cursor.fetchall()
    conn.close()
    return results
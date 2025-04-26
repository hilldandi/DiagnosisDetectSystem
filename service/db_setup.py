import sqlite3
import config as c # Proje ayarlarının bulunduğu config.py dosyasını çağırıyoruz

# sorgu çalıştırma fonksiyonu (parametreli / parametresiz)
def query_executer(query, params=None):
    conn = sqlite3.connect(c.DB_PATH) # Veritabanına bağlantı oluşturuluyor
    cursor = conn.cursor() # imleç(cursor) oluşturuluyor

    if params:
        cursor.execute(query, params) # gelen SQL sorgusu parametrelerle birlikte çalıştırılıyor
    else:
        cursor.execute(query) # gelen SQL sorgusu direkt çalıştırılıyor
    

    result=cursor.fetchone() # ilk satır (row) okunuyor
    conn.close() # bağlantı kapatılıyor
    return result # sonuç döndürlüyor

# db oluşturma fonksiyonu
def setup_database():
    conn = sqlite3.connect(c.DB_PATH) # Veritabanına bağlantı oluşturuluyor
    cursor = conn.cursor() # imleç(cursor) oluşturuluyor
    
    # SQL'i çalıştır ve veritabanını yarat (init_db.sql dosyası okunuyor ve "sql_script" değişkenine atanıyor) 
    with open(c.SQL_PATH, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script) # init_db.sql dosyasındaki SQL scriptleri çalıştırılıyor

    conn.commit() # Yapılan değişiklikler kaydediliyor
    conn.close() # Bağlantı kapatılıyor


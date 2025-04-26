import sqlite3
import datetime, os
import config as c
from service.db_setup import query_executer

# admin login doğrulama fonksiyonu
def check_log_info(admin_id, admin_password):
    # admins tablosunda admin_id ve admin_password eşleşen bir kayıt arıyoruz
    result = query_executer('''
        SELECT admin_name FROM admins WHERE admin_id = ? AND admin_password = ?
    ''', (admin_id, admin_password))
    
    # eğer bulabilirsek sadece doctor_name değerini döndürüyoruz
    # bulamazsak None değer döndürüyoruz
    return result[0] if result else None

def get_admin_info(admin_id):
    # Sadece ID'ye göre adminin adını çekiyoruz
    result = query_executer('''
        SELECT admin_name FROM admins WHERE admin_id = ?
    ''', (admin_id,))
    
    # bulamazsak None değer döndürüyoruz
    return result if result else None
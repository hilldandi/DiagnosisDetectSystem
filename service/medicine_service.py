import sqlite3
import config as c
from service.db_setup import query_executer

# Verilen teşhise(diagnose) göre veritabanından uygun ilacı getiren fonksiyon
def get_medicine(diagnose):
    result = query_executer("SELECT medicine FROM diagnose_medicine WHERE diagnose = ?", (diagnose,))
    return result[0] if result else None
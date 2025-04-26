import sys
import service.db_setup as db_setup 
import scenes.app as main_app

from PyQt5.QtWidgets import QApplication # pip install PyQt5


if __name__ == '__main__':
    # Veritabanı kurulumu veya kontrolü yapılır (gerekirse tablolar oluşturulur)
    db_setup.setup_database()
    # PyQt5 uygulaması oluşturulur (GUI framework başlatılıyor)
    app = QApplication(sys.argv)
    # Ana pencere (Main Window) scenes>app.py içindeki DiagnosisApp sınıfından üretiliyor
    main_window = main_app.DiagnosisApp()
    # Ana pencere ekranda gösterilir
    main_window.show()
    # Uygulama çalışmaya devam eder, kullanıcı kapatana kadar event loop döner
    sys.exit(app.exec_())

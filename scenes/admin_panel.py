from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from service import panel_service as pnl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class AdminPanelScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Sol üst geri butonu
        top_bar = QHBoxLayout()
        back_button = QPushButton("← Geri")
        back_button.setStyleSheet("font-size: 15px; padding: 6px 12px;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.main_window.switch_to_admin_login_scene)
        top_bar.addWidget(back_button, alignment=Qt.AlignLeft)
        layout.addLayout(top_bar)

        # Başlık
        title = QLabel("📊 Yönetici Paneli")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Sekmeli alan
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_oran_tab(), "📈 Oran Tablosu")
        self.tabs.addTab(self.create_grafik_tab(), "📊 Grafik")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    # paneldeki tabloyu oluşturan fonksiyon
    def create_oran_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4) # 4 sütun olacak
        self.table.setHorizontalHeaderLabels(["Doktor", "İyileşen Sayısı", "İyileşmeyen Sayısı", "Toplam Değerlendirme"]) # sütun isimleri
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch) # isimlerin tam gözükmesi için hizalama

        # veritabanından veriyi al
        stats = pnl.get_doctor_review_stats()
        self.table.setRowCount(len(stats)) # gelen verilerin uzunluğu kadar satır olacak
        # her veri için şu işlemleri yap
        for row, (name, total, iyilesen, iyilesmeyen) in enumerate(stats):
            formatted_name = f"Dr. {name.title()}" # ismi düzenliyoruz
            self.table.setItem(row, 0, QTableWidgetItem(formatted_name)) # 0. index name sütunu
            self.table.setItem(row, 1, QTableWidgetItem(str(iyilesen))) # 1. index iylesen sütunu
            self.table.setItem(row, 2, QTableWidgetItem(str(iyilesmeyen))) # 2. index iyilesmeyen sütunu
            self.table.setItem(row, 3, QTableWidgetItem(str(total))) # 3. index total sütunu

        layout.addWidget(self.table)
        tab.setLayout(layout)
        return tab

    # paneldeki tabloyu güncelleyen fonksiyon
    def update_oran_tab(self):
        # veritabanından veriyi al
        stats = pnl.get_doctor_review_stats()
        self.table.setRowCount(len(stats)) # gelen verilerin uzunluğu kadar satır olacak
        # her veri için şu işlemleri yap
        for row, (name, total, iyilesen, iyilesmeyen) in enumerate(stats):
            formatted_name = f"Dr. {name.title()}" # ismi düzenliyoruz
            print(f"{formatted_name} degerlendirmeler = {total}")
            self.table.setItem(row, 0, QTableWidgetItem(formatted_name)) # 0. index name sütunu
            self.table.setItem(row, 1, QTableWidgetItem(str(iyilesen))) # 1. index iylesen sütunu
            self.table.setItem(row, 2, QTableWidgetItem(str(iyilesmeyen))) # 2. index iyilesmeyen sütunu
            self.table.setItem(row, 3, QTableWidgetItem(str(total))) # 3. index total sütunu

    # paneldeki grafiği olşturan fonksiyon
    def create_grafik_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Veritabanından doktor isimlerini ve skorlarını al
        doctor_ratings = pnl.get_all_doctor_ratings()
        doctor_names = [f"Dr. {row[0].title()}" for row in doctor_ratings]
        ratings = [row[1] for row in doctor_ratings]
        
        # burayı sonra sil
        count=0
        while(count < len(doctor_names)):
            print(f"{doctor_ratings[count]}")
            count+=1

        fig, ax = plt.subplots()
        ax.bar(doctor_names, ratings, color='skyblue')
        ax.set_ylabel("Puan")
        ax.set_xlabel("Doktor")
        ax.set_title("Doktor Skorları")
        ax.set_ylim(0, 5.1)
        ax.axhline(y=sum(ratings)/len(ratings), color='red', linestyle='--', label='Ortalama')
        ax.legend()
        plt.xticks(rotation=45, ha="right")  
        fig.tight_layout()

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        tab.setLayout(layout)
        return tab

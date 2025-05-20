-- hastalar tablosu
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    tc_no TEXT UNIQUE NOT NULL,
    name TEXT,
    surname TEXT,
    gender TEXT,
    age INTEGER,
    doctor_id INTEGER NOT NULL, -- takip eden doktor id'si
    number_of_diagnoses INTEGER, -- teşhis sayısı
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- doktorlar tablosu
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL UNIQUE,
    doctor_name TEXT NOT NULL,
    doctor_password TEXT NOT NULL,
    doctor_gender TEXT,
    doctor_age INTEGER,
    rating REAL DEFAULT 0 -- hasta memnuniyet puanı (default:0)
);

-- teşhisler tablosu
CREATE TABLE IF NOT EXISTS diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    protocol_number TEXT NOT NULL UNIQUE,
    doctor_id INTEGER NOT NULL,
    patient_name TEXT,
    tc_no TEXT,
    questions_and_answers TEXT, -- sorulan sorular ve cevapları (JSON veri gelecek)
    final_diagnosis TEXT, -- en son konulan (nihai) teşhis
    medicine TEXT, -- yazılan ilaç
    are_you_healed TEXT, -- hasta iyileşti mi
    satisfaction_level INTEGER DEFAULT 0, -- memnuniyet puanı
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- teşhis & ilaç eşleştirme tablosu ()
CREATE TABLE IF NOT EXISTS diagnose_medicine (
    id INTEGER PRIMARY KEY,
    diagnose TEXT, -- teşhis 
    medicine TEXT -- ilaç
);

-- Admin (Yönetici) Tablosu
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL UNIQUE,
    admin_name TEXT NOT NULL,
    admin_password TEXT NOT NULL
);

-- yönetici - doktor - hastane ekleme
INSERT INTO admins (admin_id, admin_name, admin_password)
SELECT 007, 'admin','123'
WHERE NOT EXISTS (
    SELECT 1 FROM admins WHERE admin_id = '007' -- eğer 007 id'li bi yönetici yoksa bu idd ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 123456,'Fatma Ezgi Erkat','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '123456' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 12345,'Emre Şimşek','123','Male','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '12345' -- eğer 12345 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);

INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 123456789,'Duygu Söğütdallı','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id ='0123456789' -- eğer 0123456789 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 1234567,'Ahmet Sermet Anagün','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '1234567' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 12345678,'İlker Korkmaz','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '12345678' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 12345678912,'Oğuz Soylu','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '12345678912' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 666666,'Kaan Soylu','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '666666' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);
INSERT INTO doctors (doctor_id, doctor_name, doctor_password,doctor_gender,doctor_age)
SELECT 77777,'Zeynep Gümüş','123','Female','23'
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE doctor_id = '77777' -- eğer 123456 id'li bi doktor yoksa bu id ile oluştur, Şifre=123 
);



-- İlaç ve hastalık ekleme

/*

Migren	                                        => Sumatriptan
Tansiyon tipi baş ağrısı	                    => Parasetamol
COVID-19 Olabilir	                            => Favipiravir
COVID-19 Şüphesi (Test Önerilir)	            => PCR Testi Önerilir
COVID-19 Şüphesi Az                             => Semptom Takibi Yapılmalı
COVID-19 Olasılığı Çok Düşük	                => Önlem alınmaya devam edilmeli
COVID-19 veya Bronşit Olabilir.                 => Azitromisin
Soğuk Algınlığı / Grip	                        => Parasetamol
Soğuk algınlığı olasılığı yüksek                => Parasetamol
Grip Olabilir	                                => Oseltamivir
Sinüzit olabilir	                            => Nazal Dekonjestan ve Ağrı Kesici
Hafif Üst Solunum Yolu Enfeksiyonu.             => Bol Sıvı ve Dinlenme
Akciğer enfeksiyonu veya Bronşit olabilir.      => Amoksisilin-Klavulanat
Diğer                                           => Doktor değerlendirmesi önerilir
Diğer Nedenler Araştırılmalı                    => Doktor değerlendirmesi önerilir

*/

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Migren', 'Sumatriptan,Rizatriptan,Ergotamin (daha eski tip ilaçlarda),Naproksen (atağa destek amaçlı)'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Migren' AND medicine = 'Sumatriptan,Rizatriptan,Ergotamin (daha eski tip ilaçlarda),Naproksen (atağa destek amaçlı)'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Tansiyon tipi baş ağrısı', 'Parasetamol (Paracetamol),Ibuprofen,Naproksen'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Tansiyon tipi baş ağrısı' AND medicine = 'Parasetamol (Paracetamol),Ibuprofen,Naproksen'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Diğer', 'Doktor değerlendirmesi önerilir'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Diğer' AND medicine = 'Doktor değerlendirmesi önerilir'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'COVID-19 Olabilir', 'Antiviral ilaçlar bazı durumlarda: Nirmatrelvir + Ritonavir (Paxlovid içerikleri)\nSemptomatik tedavi:Parasetamol (ateş için), Ibuprofen (semptom kontrolü için)'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'COVID-19 Olabilir' AND medicine = 'Antiviral ilaçlar bazı durumlarda: Nirmatrelvir + Ritonavir (Paxlovid içerikleri)\nSemptomatik tedavi:Parasetamol (ateş için), Ibuprofen (semptom kontrolü için)'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Soğuk Algınlığı veya Grip', 'Parasetamol (ateş ve ağrı için),Ibuprofen,Pseudoefedrin (burun tıkanıklığı için),Dekstrometorfan (öksürük için)'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Soğuk Algınlığı veya Grip' AND medicine = 'Parasetamol (ateş ve ağrı için),Ibuprofen,Pseudoefedrin (burun tıkanıklığı için),Dekstrometorfan (öksürük için)'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'COVID-19 Şüphesi (Test Önerilir)', 'PCR Testi Önerilir'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'COVID-19 Şüphesi (Test Önerilir)' AND medicine = 'PCR Testi Önerilir'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Diğer Nedenler Araştırılmalı', 'Doktor değerlendirmesi önerilir'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Diğer Nedenler Araştırılmalı' AND medicine = 'Doktor değerlendirmesi önerilir'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'COVID-19 Şüphesi Az', 'Semptom Takibi Yapılmalı'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'COVID-19 Şüphesi Az' AND medicine = 'Semptom Takibi Yapılmalı'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'COVID-19 Olasılığı Çok Düşük', 'Önlem alınmaya devam edilmeli'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'COVID-19 Olasılığı Çok Düşük' AND medicine = 'Önlem alınmaya devam edilmeli'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'COVID-19 veya Bronşit Olabilir.', 'Azitromisin'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'COVID-19 veya Bronşit Olabilir.' AND medicine = 'Azitromisin'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Grip Olabilir.', 'Oseltamivir (antiviral, ağır vakalarda),Parasetamol,Ibuprofen'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Grip Olabilir.' AND medicine = 'Oseltamivir (antiviral, ağır vakalarda),Parasetamol,Ibuprofen'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Soğuk algınlığı olasılığı yüksek.', 'Parasetamol'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Soğuk algınlığı olasılığı yüksek.' AND medicine = 'Parasetamol'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Akciğer enfeksiyonu veya Bronşit olabilir.', 'Hafif olgularda semptomatik:Parasetamol,Ibuprofen\nBakteriyel olursa:Amoksisilin (antibiyotik)\nAmoksisilin + Klavulanik Asit,Azitromisin,Levofloksasin (ciddi vakalarda)'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Akciğer enfeksiyonu veya Bronşit olabilir.' AND medicine = 'Hafif olgularda semptomatik:Parasetamol,Ibuprofen\nBakteriyel olursa:Amoksisilin (antibiyotik)\nAmoksisilin + Klavulanik Asit,Azitromisin,Levofloksasin (ciddi vakalarda)'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Hafif Üst Solunum Yolu Enfeksiyonu.', 'Genellikle semptomatik:Parasetamol,Ibuprofen'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Hafif Üst Solunum Yolu Enfeksiyonu.' AND medicine = 'Genellikle semptomatik:Parasetamol,Ibuprofen'
);

INSERT INTO diagnose_medicine (diagnose, medicine)
SELECT 'Sinüzit olabilir.', 'Hafif vakalar:Parasetamol,Ibuprofen\nBakteriyel enfeksiyonsa:Amoksisilin'
WHERE NOT EXISTS (
    SELECT 1 FROM diagnose_medicine WHERE diagnose = 'Sinüzit olabilir.' AND medicine = 'Hafif vakalar:Parasetamol,Ibuprofen\nBakteriyel enfeksiyonsa:Amoksisilin'
);
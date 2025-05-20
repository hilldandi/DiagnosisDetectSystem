import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data/hospital.db')
SQL_PATH = os.path.join(BASE_DIR, 'data/init_db.sql')
Diagnose_Path = os.path.join(BASE_DIR, 'data/diagnostic_trees.json')
FollowUp_Path = os.path.join(BASE_DIR, 'data/follow_up_questions.json')
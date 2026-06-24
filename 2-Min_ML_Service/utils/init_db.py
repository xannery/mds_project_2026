import sqlite3
from pathlib import Path

Path("models.db").unlink(missing_ok=True) 

conn = sqlite3.connect("models.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS training_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        model_type TEXT,
        dataset_filename TEXT,
        target_column TEXT,
        hyperparameters TEXT,
        accuracy REAL,
        model_path TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()
print("База данных успешно создана как файл")
from pathlib import Path
import pickle
import json
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model(dataset_filename: str, model_name: str, model_type: str,
                hyperparameters: dict, train_size: float = 0.8):
    
    if dataset_filename == "digits":
        from sklearn.datasets import load_digits
        data = load_digits()
        X, y = data.data, data.target
    else:
        path = Path("data") / dataset_filename
        df = pd.read_csv(path)
        target = df.columns[-1]
        X = pd.get_dummies(df.drop(columns=[target]), drop_first=True)
        y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size, random_state=42
    )

    # Модель
    if model_type == "logistic":
        params = hyperparameters.copy()
        params.setdefault("max_iter", 1000)
        model = LogisticRegression(**params)
    elif model_type == "random_forest":
        params = hyperparameters.copy()
        params.setdefault("random_state", 42)
        model = RandomForestClassifier(**params)
    else:
        model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, pred)

    # Сохранение модели
    Path("models").mkdir(exist_ok=True)
    model_path = Path("models") / f"{model_name}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    try:
        conn = sqlite3.connect("models.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS training_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT,
                model_type TEXT,
                dataset_filename TEXT,
                hyperparameters TEXT,
                accuracy REAL,
                model_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            INSERT INTO training_results 
            (model_name, model_type, dataset_filename, hyperparameters, accuracy, model_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (model_name, model_type, dataset_filename, json.dumps(hyperparameters), float(accuracy), str(model_path)))
        
        conn.commit()
        conn.close()
        print(f"Модель {model_name} обучена. Accuracy: {accuracy:.4f} | Сохранена в БД")
    except Exception as e:
        print(f"Ошибка сохранения в БД: {e}")

    return {"accuracy": accuracy, "model_path": str(model_path)}
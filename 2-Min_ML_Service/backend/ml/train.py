from pathlib import Path
import pickle
import json
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

def train_model(dataset_filename: str, model_name: str, model_type: str,
                hyperparameters: dict, train_size: float = 0.8, target_column: str = "target"):
    
    path = Path("data") / dataset_filename
    if not path.exists():
        raise FileNotFoundError(f"Датасет '{dataset_filename}' не найден")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Датасет пустой")

    if target_column not in df.columns:
        raise ValueError(f"Целевая колонка '{target_column}' не найдена. Доступные: {list(df.columns)}")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Обработка пропусков
    numeric_cols = X.select_dtypes(include=['number']).columns
    categorical_cols = X.select_dtypes(exclude=['number']).columns

    if len(numeric_cols) > 0:
        num_imputer = SimpleImputer(strategy='mean')
        X[numeric_cols] = num_imputer.fit_transform(X[numeric_cols])

    if len(categorical_cols) > 0:
        cat_imputer = SimpleImputer(strategy='most_frequent')
        X[categorical_cols] = cat_imputer.fit_transform(X[categorical_cols])

    # One-hot
    X = pd.get_dummies(X, drop_first=True)

    # Split
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=train_size, random_state=42,
            stratify=y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
        )
    except:
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

    # Сохранение в БД
    try:
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
        
        conn.execute("""
            INSERT INTO training_results 
            (model_name, model_type, dataset_filename, target_column, hyperparameters, accuracy, model_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (model_name, model_type, dataset_filename, target_column, json.dumps(hyperparameters), float(accuracy), str(model_path)))
        
        conn.commit()
        conn.close()
        print(f"✅ Модель {model_name} обучена. Accuracy: {accuracy:.4f}")
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")

    return {"accuracy": accuracy, "model_path": str(model_path)}
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pathlib import Path
from backend.schemas import TrainRequest
from backend.ml.train import train_model

app = FastAPI(title="Min ML Service v1.0")

# Создаём необходимые папки
Path("data").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)

@app.get("/")
def root():
    return {"message": "Сервер работает. Документация: /docs"}

@app.post("/train")
def train_endpoint(req: TrainRequest, background_tasks: BackgroundTasks):
    data_path = Path("data") / req.dataset_filename
    
    if not data_path.exists() and req.dataset_filename != "digits":
        raise HTTPException(status_code=404, detail=f"Датасет {req.dataset_filename} не найден")
    
    background_tasks.add_task(
        train_model,
        dataset_filename=req.dataset_filename,
        model_name=req.model_name,
        model_type=req.model_type,
        hyperparameters=req.hyperparameters,
        train_size=req.train_size,
        target_column=req.target_column
    )
    
    return {
        "status": "ok",
        "message": "Обучение запущено в фоне",
        "model_name": req.model_name,
        "model_type": req.model_type
    }

@app.get("/models/available")
def get_available_models():
    return {
        "models": [
            {
                "type": "logistic",
                "name": "Logistic Regression",
                "default_params": {"max_iter": 1000, "C": 1.0}
            },
            {
                "type": "random_forest",
                "name": "Random Forest",
                "default_params": {"n_estimators": 100, "max_depth": 10}
            }
        ]
    }
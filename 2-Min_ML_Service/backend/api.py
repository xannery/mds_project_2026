from fastapi import FastAPI, BackgroundTasks, HTTPException
from pathlib import Path
from backend.schemas import TrainRequest
from backend.ml.train import train_model  

app = FastAPI(title="Min ML Service v1.0")

@app.get("/")
def root():
    return {"message": "Сервер работает. Документация: /docs"}

@app.post("/train")
def train_endpoint(req: TrainRequest, background_tasks: BackgroundTasks):
    if req.dataset_filename != "digits":
        data_path = Path("data") / req.dataset_filename
        if not data_path.exists():
            raise HTTPException(status_code=404, detail=f"Датасет {req.dataset_filename} не найден")
    
    background_tasks.add_task(
        train_model,
        dataset_filename=req.dataset_filename,
        model_name=req.model_name,
        model_type=req.model_type,
        hyperparameters=req.hyperparameters,
        train_size=req.train_size
    )
    
    return {
        "status": "ok",
        "message": "Обучение запущено в фоне",
        "model_name": req.model_name,
        "model_type": req.model_type
    }

@app.get("/models/available")
def get_available_models():
    """Список доступных моделей для фронтенда"""
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
                "default_params": {"n_estimators": 100, "max_depth": None}
            }
        ]
    }
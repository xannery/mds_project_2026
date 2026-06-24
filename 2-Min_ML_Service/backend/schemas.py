from pydantic import BaseModel, Field
from typing import Dict, Any

class TrainRequest(BaseModel):
    dataset_filename: str
    model_type: str = Field(..., description="logistic или random_forest")
    model_name: str
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    train_size: float = Field(0.8, ge=0.1, le=0.9)
    target_column: str = Field("target", description="Название целевой колонки")

    class Config:
        json_schema_extra = {
            "example": {
                "dataset_filename": "my_data.csv",
                "model_type": "logistic",
                "model_name": "my_model_v1",
                "hyperparameters": {"max_iter": 1000},
                "train_size": 0.75,
                "target_column": "target"
            }
        }
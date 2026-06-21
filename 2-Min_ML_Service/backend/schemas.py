from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class TrainRequest(BaseModel):
    dataset_filename: str
    model_type: str = Field(..., description="logistic regression или random_forest")
    model_name: str
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    train_size: float = Field(0.8, ge=0.1, le=0.9)

    class Config:
        json_schema_extra = {  
            "example": {
                "dataset_filename": "digits",
                "model_type": "logistic",
                "model_name": "test_model_1",
                "hyperparameters": {"max_iter": 500},
                "train_size": 0.75
            }
        }
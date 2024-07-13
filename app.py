from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List
import logging
import os

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MODEL_PATH = os.getenv("MODEL_PATH", "/app/model")

# Load the text classification pipeline from the model directory
try:
    classifier = pipeline("text-classification", model=MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError("Failed to load model")

class Prediction(BaseModel):
    label: str
    score: float

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    predictions: List[Prediction]

@app.post("/predict", response_model=TextResponse)
def classify_text(request: TextRequest):
    try:
        results = classifier(request.text , return_all_scores=True)[0]
        predictions = [Prediction(label=result['label'], score=result['score']) for result in results]
        return TextResponse(predictions=predictions)
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(status_code=500, detail="Classification failed")
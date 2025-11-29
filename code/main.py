# code/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .model import predict_food
from .utils import map_label_to_health


app = FastAPI(
    title="Food Tamagotchi Backend",
    description="FastAPI service for Food Tamagotchi (Food -> Health Score).",
    version="0.1.0",
)

# Allow frontend (e.g. React / plain JS on localhost) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    """Simple health check."""
    return {"status": "ok", "message": "Backend is alive"}


@app.post("/analyze_food")
async def analyze_food(image: UploadFile = File(...)):
    """
    Accept an image file, run AI model, and return health info.

    Request:
        multipart/form-data with field name "image"

    Response JSON:
    {
      "raw_label": "...",
      "confidence": 0.87,
      "category": "healthy",
      "health_score": 90,
      "tip": "Great choice! ..."
    }
    """
    # Basic validation
    if image.content_type is None or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_bytes = await image.read()
        if not image_bytes:
            raise ValueError("Empty image file.")

        label, confidence = predict_food(image_bytes)
        category, health_score, tip = map_label_to_health(label)

        return {
            "raw_label": label,
            "confidence": confidence,
            "category": category,
            "health_score": health_score,
            "tip": tip,
        }

    except HTTPException:
        # Let FastAPI handle already raised HTTP errors
        raise
    except Exception as e:
        # Generic error
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

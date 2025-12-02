from fastapi import FastAPI, UploadFile, File, HTTPException
from uuid import uuid4
import os, shutil 

from db import db, cursor
from ai_model import analyze_food
from scoring import calculate_score, update_dragon

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#upload & analyze endpoint
@app.post("/meal/analyze")
async def analyze_meal(
        user_id: int,
        level: int,
        progress: int,
        file: UploadFile = File(...)
):
    
    #validation file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG/PNG images allowed")

    #save JPG on local disk
    filename = f"{uuid4()}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    #AI model here
    results = analyze_food(path)
    #scoring
    score = calculate_score(results)
    #update dragon state
    new_level, new_progress = update_dragon(score, level, progress)
    #save history
    cursor.execute("""
        INSERT INTO meal_history
        (user_id, photo_path, score)
        VALUES (%s,%s,%s)
    """,(user_id,path,score))

    db.commit()

    return{
        "score": score,
        "previous": {"level":level, "progress":progress},
        "current": {"level": new_level,"progress": new_progress},
        "ai_results": results
    }


#history endpont
@app.get("/history/{user_id}")
def history(user_id:int):
    cursor.execute("""
        SELECT photo_path,score,uploaded_at
        FROM meal_history
        WHERE user_id=%s
        ORDER BY uploaded_at DESC
    """, (user_id,))

    return cursor.fetchall()

    return history
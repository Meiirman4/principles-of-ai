from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import os, shutil

# FIXED IMPORTS — your folder name is "upload", NOT "uploads"
from code.upload.db import db, cursor, create_user, get_user
from code.upload.ai_engine import analyze_food
from code.upload.scoring import calculate_score, update_dragon


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Homepage
@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):

    user_id = 1

    cursor.execute("SELECT level, progress FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        level = 1
        progress = 50
    else:
        level = user["level"]
        progress = user["progress"]

    hp = progress
    exp = progress / 2

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "user_id": user_id,
            "level": level,
            "hp": hp,
            "exp": exp,
        }
    )


# Register
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):

    success = create_user(username, password)

    if not success:
        return JSONResponse({"status": "error", "message": "Username already exists"})

    return JSONResponse({"status": "ok", "message": "User registered successfully"})


# Login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    user = get_user(username)

    if not user:
        return JSONResponse({"status": "error", "message": "User not found"})

    if user["password"] != password:
        return JSONResponse({"status": "error", "message": "Incorrect password"})

    return JSONResponse({
        "status": "ok",
        "message": "Logged in",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "level": user["level"],
            "progress": user["progress"],
        }
    })


# Meal analyze
@app.post("/meal/analyze", response_class=HTMLResponse)
async def analyze_meal(
    request: Request,
    user_id: int,
    file: UploadFile = File(...)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG/PNG images allowed")

    filename = f"{uuid4()}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cursor.execute("SELECT level, progress FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    level = user["level"]
    progress = user["progress"]

    ai_results = analyze_food(path)
    score = calculate_score(ai_results)

    new_level, new_progress = update_dragon(score, level, progress)

    cursor.execute(
        "UPDATE users SET level=%s, progress=%s WHERE id=%s",
        (new_level, new_progress, user_id)
    )
    db.commit()

    cursor.execute("""
        INSERT INTO meal_history (user_id, photo_path, score)
        VALUES (%s, %s, %s)
    """, (user_id, path, score))
    db.commit()

    hp = new_progress
    exp = new_progress / 2

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "user_id": user_id,
            "level": new_level,
            "hp": hp,
            "exp": exp,
        }
    )


# History
@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request, user_id: int):

    cursor.execute("""
        SELECT photo_path, score, uploaded_at
        FROM meal_history
        WHERE user_id=%s
        ORDER BY uploaded_at DESC
    """, (user_id,))

    history = cursor.fetchall()

    return templates.TemplateResponse(
        "history.html",
        {"request": request, "history": history}
    )

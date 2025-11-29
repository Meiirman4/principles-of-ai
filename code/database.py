# database.py
import json
import os
import hashlib
import datetime

DB_FILE = "dragon_save.json"

def _load_data():
    if not os.path.exists(DB_FILE):
        return {"stats": {"health": 50, "xp": 0, "level": 1}, "history": []}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"stats": {"health": 50, "xp": 0, "level": 1}, "history": []}

def _save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def init_db():
    data = _load_data()
    _save_data(data)

def get_dragon_state():
    return _load_data()["stats"]

def is_duplicate_image(image_bytes):
    img_hash = hashlib.md5(image_bytes).hexdigest()
    data = _load_data()
    for entry in data["history"]:
        if entry["hash"] == img_hash:
            return True
    return False

# --- UPDATED FUNCTION FOR RPG MODEL ---
def update_dragon(food_name, hp_change, xp_change, image_bytes):
    data = _load_data()
    stats = data["stats"]
    
    # 1. Update Health (Cap between 0 and 100)
    stats["health"] = max(0, min(100, stats["health"] + hp_change))
    
    # 2. Update XP (Always goes up)
    stats["xp"] += xp_change
    
    # 3. Level Up Logic (Level up every 100 XP)
    # Example: 250 XP = Level 3 (Starts at Lvl 1)
    stats["level"] = 1 + (stats["xp"] // 100)
    
    # 4. Log History
    img_hash = hashlib.md5(image_bytes).hexdigest()
    data["history"].append({
        "food": food_name,
        "hp_change": hp_change,
        "xp_change": xp_change,
        "hash": img_hash,
        "time": str(datetime.datetime.now())
    })
    
    _save_data(data)
    return stats
# game_logic.py

# FORMAT: "keyword": {"hp": Health_Change, "xp": XP_Gain, "mood": Reaction}

FOOD_STATS = {
    # --- 🟢 THE HEALERS (High HP, Low XP) ---
    "salad":        {"hp": 20, "xp": 5,  "mood": "happy"},
    "broccoli":     {"hp": 20, "xp": 5,  "mood": "happy"},
    "cucumber":     {"hp": 20, "xp": 5,  "mood": "happy"},
    "apple":        {"hp": 10, "xp": 10, "mood": "happy"},
    "orange":       {"hp": 10, "xp": 10, "mood": "happy"},
    "banana":       {"hp": 10, "xp": 10, "mood": "happy"},
    "strawberry":   {"hp": 15, "xp": 5,  "mood": "happy"},

    # --- 🟡 THE FUEL / CARBS (Neutral HP, High XP) ---
    # Logic: Energy for growth, but doesn't heal wounds.
    "rice":         {"hp": 0,  "xp": 25, "mood": "neutral"},
    "pasta":        {"hp": 0,  "xp": 25, "mood": "neutral"},
    "spaghetti":    {"hp": 0,  "xp": 25, "mood": "neutral"},
    "bread":        {"hp": 0,  "xp": 20, "mood": "neutral"},
    "potato":       {"hp": 0,  "xp": 20, "mood": "neutral"},
    "mashed_potato":{"hp": 0,  "xp": 20, "mood": "neutral"},
    "bagel":        {"hp": -5, "xp": 30, "mood": "neutral"}, # Slight junk

    # --- 🔵 PROTEINS (Low HP, High XP) ---
    "chicken":      {"hp": 5,  "xp": 25, "mood": "happy"},
    "steak":        {"hp": 5,  "xp": 25, "mood": "happy"},
    "fish":         {"hp": 10, "xp": 20, "mood": "happy"},
    "egg":          {"hp": 5,  "xp": 15, "mood": "neutral"},

    # --- 🔴 JUNK FOOD (Damage HP, Massive XP) ---
    # Logic: Dragon loves the taste (XP), but gets sick (HP).
    "burger":       {"hp": -15, "xp": 40, "mood": "sick"},
    "cheeseburger": {"hp": -15, "xp": 40, "mood": "sick"},
    "pizza":        {"hp": -10, "xp": 35, "mood": "sick"},
    "hotdog":       {"hp": -15, "xp": 35, "mood": "sick"},
    "fries":        {"hp": -10, "xp": 25, "mood": "neutral"},
    "ice_cream":    {"hp": -10, "xp": 30, "mood": "sick"},
    "chocolate":    {"hp": -5,  "xp": 20, "mood": "sick"},
    "cake":         {"hp": -10, "xp": 30, "mood": "sick"},
}

def analyze_food(ai_label):
    clean_label = ai_label.lower().replace("_", " ")
    
    # Check our dictionary
    for food_key, stats in FOOD_STATS.items():
        if food_key in clean_label:
            return stats # Return the whole object: {"hp": 20, "xp": 5...}
            
    # Default if unknown food
    return {"hp": 0, "xp": 5, "mood": "neutral"}
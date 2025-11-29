"""
Health Logic: map model label -> category, score, tip
"""

def map_label_to_health(label: str):
    label = label.lower()

    healthy_keywords = [
        "salad", "vegetable", "veggie", "broccoli", "spinach",
        "fruit", "apple", "banana", "orange", "avocado", "carrot",
    ]

    neutral_keywords = [
        "rice", "pasta", "noodle", "bread", "sandwich", "egg",
        "omelet", "omelette",
    ]

    unhealthy_keywords = [
        "pizza", "burger", "cheeseburger", "fries", "fried",
        "ice cream", "donut", "doughnut", "cake", "hotdog", "soda",
    ]

    if any(w in label for w in healthy_keywords):
        return "healthy", 90, "Great choice! Lots of nutrients for your body and your dragon."

    if any(w in label for w in neutral_keywords):
        return "neutral", 60, "Not bad! Try adding some fruits or vegetables next time."

    if any(w in label for w in unhealthy_keywords):
        return "unhealthy", 25, "Tasty but heavy… too much of this makes your dragon sleepy."

    return "unknown", 50, "I'm not sure what this is. Try a clearer food photo!"

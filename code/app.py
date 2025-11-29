from flask import Flask, render_template, request, jsonify
import ai_engine
import database
import game_logic

app = Flask(__name__)

ai_engine.load_model()
database.init_db()

@app.route('/')
def home():
    stats = database.get_dragon_state()
    return render_template('index.html', stats=stats)

@app.route('/feed', methods=['POST'])
def feed():
    if 'image' not in request.files:
        return jsonify({'error': 'No image sent'}), 400
        
    file = request.files['image']
    img_bytes = file.read()
    
    # 1. Anti-Cheat
    if database.is_duplicate_image(img_bytes):
        return jsonify({'error': 'Duplicate photo! No cheating!'})
        
    # 2. AI Prediction
    label, confidence = ai_engine.predict_image(img_bytes)
    if not label:
        return jsonify({'error': 'Could not see image'}), 400
        
    print(f"DEBUG: AI saw '{label}'") # Keep this for debugging
    
    # 3. Game Logic (New RPG Logic)
    result = game_logic.analyze_food(label)
    
    hp_change = result['hp']
    xp_change = result['xp']
    mood = result['mood']
    
    # 4. Update Database
    new_stats = database.update_dragon(label, hp_change, xp_change, img_bytes)
    
    return jsonify({
        'food': label,
        'hp_change': hp_change,
        'xp_change': xp_change,
        'mood': mood,
        'stats': new_stats
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
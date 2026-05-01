from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

def analyze_text(text, typing_time, edit_count):
    # Sentiment
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    # Keyword suspicion
    suspicious_words = ["honestly", "trust me", "believe me", "i swear", "to tell the truth", "actually"]
    keyword_score = sum(word in text.lower() for word in suspicious_words)
    
    # Smarter Typing Hesitation (WPM)
    word_count = len(text.split())
    time_in_minutes = typing_time / 60 if typing_time > 0 else 0.01
    wpm = word_count / time_in_minutes
    
    hesitation_score = 1 if wpm < 25 else 0
    
    # Edit Penalty: If they backspaced more than 3 times, add a penalty
    edit_penalty = 1 if edit_count > 3 else 0
    
    # Final score logic (Truth needs a positive score)
    score = (sentiment * 2) - keyword_score - hesitation_score - edit_penalty
    
    verdict = "Likely Truth" if score >= 0 else "Suspicious"
    
    return {
        "verdict": verdict,
        "sentiment": round(sentiment, 2),
        "wpm": round(wpm),
        "flags": keyword_score,
        "edits": edit_count
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    typing_time = data.get('time', 0)
    edit_count = data.get('edits', 0) # Safely get the new edit count
    
    if not text.strip():
        return jsonify({"error": "Text cannot be empty"}), 400
        
    breakdown = analyze_text(text, typing_time, edit_count)
    return jsonify(breakdown)

if __name__ == '__main__':
    app.run(debug=True)
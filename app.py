from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

def analyze_text(text, typing_time):
    # Sentiment
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    # Keyword suspicion
    suspicious_words = ["honestly", "trust me", "believe me", "i swear"]
    keyword_score = sum(word in text.lower() for word in suspicious_words)

    # Typing hesitation (more time = more suspicious)
    if typing_time > 5:
        hesitation_score = 1
    else:
        hesitation_score = 0

    # Final score
    score = (sentiment * 2) - keyword_score - hesitation_score

    if score > 0:
        result = "Likely Truth ✅"
    else:
        result = "Suspicious ⚠️"

    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data['text']
    typing_time = data['time']

    result = analyze_text(text, typing_time)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
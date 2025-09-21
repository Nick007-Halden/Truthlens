
from flask import Flask, render_template, request, jsonify, send_from_directory
import json, os, datetime, random

app = Flask(__name__)
DATA_FILE = os.path.join(app.root_path, 'data', 'factchecks.json')

def load_corpus():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def simple_score_claim(claim, corpus):
    claim_l = claim.lower()
    best = None
    best_score = 0
    matched = []
    for doc in corpus:
        score = 0
        for w in doc.get('keywords', []):
            if w in claim_l:
                score += 1
        if any(num in claim_l for num in ['%','percent','million','billion','crore']):
            score += 0.5
        for w in doc.get('title','').lower().split():
            if w in claim_l:
                score += 0.2
        if score > 0:
            matched.append((doc, score))
        if score > best_score:
            best_score = score
            best = doc
    if best is None:
        verdict = "Unverified / No credible matches"
        score_val = 0.0
        explanation = "We couldn't find matching credible sources in the local corpus. This demo uses a small seeded dataset. Try another claim or deploy with Vertex AI + news sources for full results."
        micro = "Tip: If no credible sources appear, check official fact-checkers (e.g., WHO, Reuters, PIB) or search for the original study."
    else:
        label = best.get('label')
        if label == 'false':
            verdict = "Likely False"
            score_val = -0.7
            explanation = f"This claim closely matches a known false item: \"{best.get('title')}\". Reason: {best.get('summary')}"
            micro = best.get('micro_lesson')
        elif label == 'true':
            verdict = "Likely True"
            score_val = 0.8
            explanation = f"This claim closely matches verified information: \"{best.get('title')}\". Summary: {best.get('summary')}"
            micro = best.get('micro_lesson')
        else:
            verdict = "Mixed / Context-dependent"
            score_val = 0.1
            explanation = f"Found related context: \"{best.get('title')}\". Summary: {best.get('summary')}"
            micro = best.get('micro_lesson')
    return {
        "verdict": verdict,
        "score": score_val,
        "explanation": explanation,
        "micro_lesson": micro,
        "matched": [ {"title": d.get('title'), "url": d.get('url')} for d,s in matched[:5] ]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    claim = data.get('claim','').strip()
    if not claim:
        return jsonify({"error":"No claim provided"}), 400
    corpus = load_corpus()
    result = simple_score_claim(claim, corpus)
    result['timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'
    return jsonify(result)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    f = request.files.get('image')
    if not f:
        return jsonify({"error":"No file uploaded"}), 400
    fname = f.filename.lower()
    corpus = load_corpus()
    for doc in corpus:
        imgs = doc.get('images', [])
        for im in imgs:
            if im.get('filename') and im.get('filename').lower() in fname:
                return jsonify({
                    "verdict":"Image context found",
                    "explanation": f"Image matches known item: {doc.get('title')}. Original date: {doc.get('date')}.",
                    "micro_lesson": doc.get('micro_lesson'),
                    "matched": [{"title": doc.get('title'), "url": doc.get('url'), "date": doc.get('date')}]
                })
    return jsonify({
        "verdict":"No match found",
        "explanation":"We couldn't find this image in the seeded corpus. Deploy with a larger reverse-image index for production.",
        "micro_lesson":"Tip: Use reverse image search (e.g., TinEye, Google Images) to find original context."
    })

@app.route('/static/<path:fname>')
def static_file(fname):
    return send_from_directory(os.path.join(app.root_path,'static'), fname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

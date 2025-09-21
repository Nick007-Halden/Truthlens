
TruthLens Coach - Prototype Web App (Demo)
=========================================

This lightweight prototype provides a local web app you can run and demo quickly for the hackathon.
It includes 2-3 working features:
1) Paste a claim and click Analyze -> returns verdict + explanation + micro-lesson (matches against a small seeded corpus)
2) Upload an image -> performs a simulated reverse-image 'PastCheck' lookup against the seeded corpus
3) Simple, aesthetic UI ready for screen recording

How to run locally (5 minutes)
------------------------------
1. Download and unzip this package.
2. Create a virtualenv and install requirements:
   python -m venv venv
   source venv/bin/activate   (on Windows: venv\\Scripts\\activate)
   pip install -r requirements.txt
3. Run the app:
   python app.py
4. Open http://localhost:8000 in your browser and demo the features.

Prototype link for submission
-----------------------------
- Run locally and present http://localhost:8000 as your prototype link (or expose with ngrok or localtunnel for remote access).

Recording a 3-minute video (script + shots)
-------------------------------------------
0:00-0:10 - Title slide: "TruthLens Coach - demo (Team: Syntax Shenanigans)"
0:10-0:40 - Show problem statement and why it's important (20s)
0:40-1:40 - Live demo:
  - Paste the pre-filled claim and click Analyze -> show verdict, explanation, micro-lesson (40s)
  - Upload the file named 'kerala2018.jpg' (or a sample image) and show PastCheck output (20s)
1:40-2:30 - Quick architecture overview (show README/BACKEND_NOTES) (50s)
2:30-3:00 - Closing: impact, next steps, call to action (30s)

GitHub repo & submission
------------------------
- Create a new GitHub repo and push this folder.
- Use the repo link as your submission. Include a short README (this file) and a link to your recorded video (hosted on Google Drive / YouTube unlisted).

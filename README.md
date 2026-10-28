# InterviewReady — AI Interview Coach MVP

A free-first Streamlit MVP for mock interviews, answer feedback, practice scores, a results dashboard, and CSV export.

## Current MVP capabilities
- Profile and interview setup (role, experience, interview type, question count)
- Question bank for HR/behavioral, technical, and situational interviews
- Save answers during a session
- Rule-based score breakdown: answer development, topic relevance, structure cues, and specificity
- Per-question feedback and model-answer guidance
- Performance dashboard and CSV download
- No API key required

## Important limitation
The first version uses a transparent heuristic rubric. It is **not a live generative AI model** and does not understand answers as deeply as an LLM. It is suitable as a working MVP/demo, but describe it honestly in your presentation. A later iteration can add an LLM API or a hosted open model.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
```

Windows:
```bat
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

macOS/Linux:
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy publicly with Streamlit Community Cloud
1. Create/sign in to GitHub.
2. Create a new repository, for example `ai-interview-coach-mvp`.
3. Upload `app.py`, `requirements.txt`, and `README.md` to the repository root.
4. Open https://share.streamlit.io/ and sign in with GitHub.
5. Select **Create app**, choose your repository, branch (usually `main`), and main file path `app.py`.
6. Click **Deploy**. Wait for the build to complete.
7. Open the generated `*.streamlit.app` URL and test the full flow: Setup → Mock Interview → Results Dashboard → CSV download.

Hosting providers can change their free-tier terms and availability. Use the deployment dashboard's current instructions if labels differ.

## Suggested acceptance test
- Start an interview with a name and choose each interview type.
- Save answers for at least 3 questions.
- Finish the interview and confirm the dashboard displays scores and feedback.
- Download the CSV and open it.
- Open the public URL in a private/incognito window to confirm it is publicly accessible.

## Privacy
The app keeps interview answers in Streamlit session state for the active session. It does not intentionally write answers to a database. Do not enter confidential personal or employer information.

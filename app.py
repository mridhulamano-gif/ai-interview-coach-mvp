import io
import re
import wave
import html
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import speech_recognition as sr
except Exception:
    sr = None


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)


# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --navy: #111b35;
    --ink: #17233b;
    --muted: #65728a;
    --blue: #4169e1;
    --cyan: #49c5c2;
    --gold: #f4bd62;
    --paper: #f4f7fc;
    --line: #e2e8f2;
}

.stApp {
    background: radial-gradient(circle at 85% 0%, #e9efff 0, transparent 27%), var(--paper);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111b35, #1c3158);
}

[data-testid="stSidebar"] * {
    color: #f5f7ff !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #d5def2 !important;
}

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--navy) !important;
}

[data-testid="stWidgetLabel"] p {
    color: #263752 !important;
    font-weight: 700 !important;
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

input, textarea {
    color: #17233b !important;
    background: #fff !important;
    -webkit-text-fill-color: #17233b !important;
}

div[data-baseweb="select"] > div {
    background: #fff !important;
}

div[data-baseweb="select"] * {
    color: #17233b !important;
}

[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid var(--line);
    padding: 16px;
    border-radius: 17px;
    box-shadow: 0 8px 24px #1b2b4a0a;
}

[data-testid="stMetricLabel"] {
    color: #65728a !important;
}

[data-testid="stMetricValue"] {
    color: #17233b !important;
    font-family: 'Manrope', sans-serif;
}

.hero {
    padding: 30px 34px;
    border-radius: 24px;
    background: linear-gradient(115deg, #111b35, #233d70 62%, #4169e1);
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 18px 40px #172b5525;
}

.hero h1 {
    color: white !important;
    font-size: 2.45rem;
    margin: 8px 0;
}

.hero p {
    color: #e4ecff !important;
    margin: 0;
}

.eyebrow {
    color: #f4bd62;
    font-size: .74rem;
    font-weight: 800;
    letter-spacing: .17em;
}

.feature, .panel {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 8px 24px #1b2b4a08;
}

.feature p {
    color: #65728a;
}

.question-card {
    background: linear-gradient(120deg, white, #f8faff);
    border: 1px solid #dce5f3;
    border-left: 6px solid var(--gold);
    border-radius: 18px;
    padding: 23px;
    margin: 10px 0 18px;
}

.pill {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 50px;
    background: #eaf0ff;
    color: #2c4c9b;
    font-size: .75rem;
    font-weight: 800;
}

.tip {
    background: #eef5ff;
    border-left: 4px solid var(--blue);
    padding: 14px 17px;
    border-radius: 12px;
    color: #263d65;
    margin: 12px 0;
}

.score-hero {
    background: linear-gradient(120deg, #14213e, #294b83);
    padding: 24px;
    border-radius: 20px;
    color: white;
}

.score-hero h2, .score-hero h3, .score-hero p {
    color: white !important;
}

.score-number {
    font-family: 'Manrope', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: white;
}

.bar-row {
    margin: 13px 0;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    color: #263752;
    margin-bottom: 6px;
}

.bar-track {
    height: 10px;
    background: #e9eef7;
    border-radius: 20px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #4169e1, #49c5c2);
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 750;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #3159c9, #5279e9);
    color: white;
    border: 0;
}

.footer {
    color: #8490a4;
    font-size: .78rem;
    padding: 20px 0 5px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# QUESTION BANK
# =====================================================

QUESTION_BANK = {
    "HR / Behavioural": [
        "Tell me about yourself and what makes you suitable for this role?",
        "What are your greatest strengths? Give an example of how you used them.",
        "Describe a challenge you faced and how you overcame it.",
        "Tell me about a time you worked successfully in a team.",
        "Describe a mistake you made and what you learned from it.",
        "How do you manage multiple deadlines?",
        "Tell me about a time you handled a disagreement with a teammate.",
        "Why do you want this role and this organisation?",
        "Describe a situation where you took initiative.",
        "How do you respond to constructive criticism?",
        "What motivates you to perform your best?",
        "What is one skill you are actively improving?"
    ],

    "Technical": [
        "Explain a technical project you worked on and your personal contribution.",
        "Describe how you would debug a problem you cannot immediately solve.",
        "Explain a technical concept in your field to a beginner.",
        "How do you test your work and ensure its quality?",
        "Describe a technical challenge and the steps you took to solve it.",
        "How do you learn a new programming language or technology?",
        "How would you investigate a slow-running application?",
        "Explain a project decision and the alternatives you considered.",
        "How do you approach a problem when requirements are unclear?",
        "Describe a time you improved an existing solution.",
        "How would you balance performance and maintainability?",
        "What technical skill are you currently improving, and why?"
    ],

    "Situational": [
        "What would you do if you were given a task with unclear instructions?",
        "How would you handle a disagreement with your manager?",
        "What would you do if you realised you might miss a deadline?",
        "How would you respond to a dissatisfied customer?",
        "What would you do if a teammate was not contributing?",
        "How would you prioritise two urgent tasks?",
        "What would you do if you discovered an error after submission?",
        "How would you handle an unfamiliar task with a short deadline?",
        "What would you do if you received conflicting feedback?",
        "How would you respond if you did not know an interview answer?",
        "How would you communicate a project delay to stakeholders?",
        "How would you approach a task when success criteria are unclear?"
    ]
}

QUESTION_BANK["Mixed"] = (
    QUESTION_BANK["HR / Behavioural"][:6]
    + QUESTION_BANK["Technical"][:6]
    + QUESTION_BANK["Situational"][:6]
)

ROLE_QUESTIONS = {
    "Software / IT": [
        "Explain a project where you used programming to solve a real problem.",
        "How would you find and fix a bug that occurs only occasionally?",
        "How do you choose suitable data structures for a problem?",
        "How would you collaborate with a team using Git?"
    ],

    "Data Science / Analytics": [
        "How would you handle missing values in a dataset?",
        "Explain the difference between classification and regression.",
        "How would you communicate a complex data insight to a non-technical audience?",
        "How would you check whether a model is overfitting?"
    ],

    "Business / Management": [
        "How would you prioritise competing business objectives?",
        "Describe how you would resolve a disagreement within a team.",
        "How would you measure whether a project was successful?",
        "How would you communicate an unpopular decision?"
    ],

    "Marketing / Sales": [
        "How would you identify the target audience for a new product?",
        "How would you measure the success of a marketing campaign?",
        "How would you respond to a potential customer who rejects your proposal?",
        "How would you use customer feedback to improve a campaign?"
    ],

    "General / Student": [
        "Tell me about an academic project you are proud of.",
        "Describe a time you learned a difficult skill.",
        "How do you manage your studies and other responsibilities?",
        "What would you contribute to this organisation?"
    ]
}

FILLERS = [
    "um", "uh", "erm", "actually",
    "basically", "literally", "you know", "i mean"
]

STOP_WORDS = {
    "tell", "about", "what", "when", "where", "which",
    "would", "could", "should", "have", "your", "with",
    "that", "this", "from", "into", "describe", "explain",
    "time", "role", "work", "they", "them", "how",
    "does", "did", "will", "were", "been", "being",
    "the", "and", "for", "are", "you"
}


# =====================================================
# SESSION STATE
# =====================================================

DEFAULTS = {
    "page": "Setup",
    "profile_name": "",
    "setup_name": "",
    "role": "General / Student",
    "experience": "Student / Fresher",
    "interview_type": "Mixed",
    "question_count": 5,
    "questions": [],
    "index": 0,
    "answers": {},
    "audio_metrics": {},
    "history": [],
    "result": None,
    "active": False,
    "session_id": 0,
    "start_error": ""
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# ANSWER ANALYSIS
# =====================================================

def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def filler_counts(text):
    low = (text or "").lower()

    return {
        word: len(re.findall(r"\b" + re.escape(word) + r"\b", low))
        for word in FILLERS
        if re.search(r"\b" + re.escape(word) + r"\b", low)
    }


def evaluate_answer(question, answer):
    answer = (answer or "").strip()
    words = word_count(answer)
    low = answer.lower()

    if not answer:
        return {
            "score": 0,
            "development": 0,
            "structure": 0,
            "specificity": 0,
            "relevance": 0,
            "words": 0,
            "strengths": [],
            "feedback": ["Add an answer before completing this question."],
            "communication": ["Try speaking in complete, clear sentences."],
            "fillers": {}
        }

    if words < 10:
        development = 4
    elif words < 25:
        development = 10
    elif words < 45:
        development = 17
    elif words <= 150:
        development = 23
    else:
        development = 18

    groups = [
        ["situation", "context", "when"],
        ["task", "goal", "responsible", "needed to"],
        ["action", "implemented", "developed", "created",
         "i decided", "i organised", "i analyzed", "i analysed"],
        ["result", "outcome", "achieved", "improved",
         "learned", "reduced", "increased"]
    ]

    hits = sum(
        any(term in low for term in group)
        for group in groups
    )

    sequence = any(
        term in low
        for term in ["first", "then", "after that", "finally", "as a result"]
    )

    structure = min(25, 5 + hits * 5 + (2 if sequence else 0))

    evidence_terms = [
        "because", "for example", "specifically", "measured",
        "tested", "customer", "project", "team", "deadline",
        "data", "client", "users", "percent", "%",
        "hours", "days", "budget"
    ]

    evidence = sum(1 for term in evidence_terms if term in low)
    has_number = bool(re.search(r"\b\d+(?:[.,]\d+)?%?\b", low))

    specificity = min(25, 5 + evidence * 2 + (4 if has_number else 0))

    question_terms = (
        set(re.findall(r"\b[a-z]{4,}\b", question.lower()))
        - STOP_WORDS
    )

    answer_terms = (
        set(re.findall(r"\b[a-z]{4,}\b", low))
        - STOP_WORDS
    )

    overlap = len(question_terms & answer_terms)

    relevance = (
        min(25, 7 + overlap * 4)
        if question_terms else 15
    )

    score = min(
        100,
        development + structure + specificity + relevance
    )

    strengths = []
    feedback = []
    communication = []

    if 45 <= words <= 150:
        strengths.append("Your answer has a useful level of detail.")
    elif words < 45:
        feedback.append(
            "Add context, explain your actions and finish with the outcome."
        )
    else:
        feedback.append("Keep the answer focused; remove repeated details.")

    if hits >= 3:
        strengths.append("Your answer includes several STAR elements.")
    else:
        feedback.append(
            "For experience-based questions, use STAR: Situation, Task, Action and Result."
        )

    if evidence >= 3 or has_number:
        strengths.append("You included concrete details or evidence.")
    else:
        feedback.append(
            "Add a specific example, your personal contribution or a measurable result."
        )

    if relevance >= 15:
        strengths.append("Some wording in your answer connects with the question.")
    else:
        feedback.append(
            "Answer the exact question directly in your opening sentence."
        )

    fillers = filler_counts(answer)
    total_fillers = sum(fillers.values())

    if total_fillers:
        communication.append(
            f"{total_fillers} common filler-word occurrence(s) detected in the text."
        )
    else:
        communication.append(
            "No common filler-word pattern was detected in the text."
        )

    if any(
        phrase in low
        for phrase in ["i think maybe", "i guess", "sort of", "kind of", "not sure"]
    ):
        communication.append(
            "Replace vague phrases with a clear explanation while staying honest."
        )

    communication.append(
        "Read your answer aloud once and check that each sentence adds useful information."
    )

    return {
        "score": score,
        "development": development,
        "structure": structure,
        "specificity": specificity,
        "relevance": relevance,
        "words": words,
        "strengths": strengths,
        "feedback": feedback,
        "communication": communication,
        "fillers": fillers
    }


# =====================================================
# AUDIO AND SPEECH RECOGNITION
# =====================================================

def audio_stats(data, transcript):
    try:
        with wave.open(io.BytesIO(data), "rb") as wav:
            duration = wav.getnframes() / float(wav.getframerate())

        words = word_count(transcript)

        wpm = (
            round(words / (duration / 60))
            if duration > 0 and words else None
        )

        return {
            "duration": round(duration, 1),
            "wpm": wpm
        }

    except Exception:
        return {"duration": None, "wpm": None}


def transcribe(data, language):
    if sr is None:
        return None, (
            "SpeechRecognition is not installed. You can type your answer instead."
        )

    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(data)) as source:
            audio = recognizer.record(source)

        transcript = recognizer.recognize_google(
            audio,
            language=language
        )

        return transcript, None

    except sr.UnknownValueError:
        return None, "The recording could not be understood. Try again in a quiet place."

    except sr.RequestError as exc:
        return None, f"Speech recognition is unavailable: {exc}. You can type your answer instead."

    except Exception as exc:
        return None, f"Could not process this recording: {exc}"


# =====================================================
# INTERVIEW CALLBACKS
# =====================================================

def answer_key(index):
    return f"answer_{st.session_state.session_id}_{index}"


def audio_key(index):
    return f"audio_{st.session_state.session_id}_{index}"


def save_profile_name():
    """Keep the name separately from the Setup widget state."""
    st.session_state.profile_name = str(
        st.session_state.get("setup_name", "")
    ).strip()


def start_interview():
    # Read the persistent name first; use the widget value as a fallback.
    entered_name = str(
        st.session_state.get("profile_name", "")
        or st.session_state.get("setup_name", "")
    ).strip()

    st.session_state.profile_name = entered_name

    if not entered_name:
        st.session_state.start_error = "Please enter your name before starting."
        return

    st.session_state.start_error = ""
    st.session_state.session_id += 1

    pool = (
        QUESTION_BANK[st.session_state.interview_type]
        + ROLE_QUESTIONS[st.session_state.role]
    )

    offset = (st.session_state.session_id * 3) % len(pool)
    pool = pool[offset:] + pool[:offset]

    st.session_state.questions = pool[:st.session_state.question_count]
    st.session_state.index = 0
    st.session_state.answers = {}
    st.session_state.audio_metrics = {}
    st.session_state.active = True
    st.session_state.result = None
    st.session_state.page = "Mock Interview"


def save_answer():
    index = st.session_state.index
    key = answer_key(index)

    st.session_state.answers[index] = str(
        st.session_state.get(key, "")
    ).strip()


def next_question():
    save_answer()
    st.session_state.index = min(
        st.session_state.index + 1,
        len(st.session_state.questions) - 1
    )


def previous_question():
    save_answer()
    st.session_state.index = max(0, st.session_state.index - 1)


def finish_interview():
    save_answer()
    details = []

    for i, question in enumerate(st.session_state.questions):
        answer = st.session_state.answers.get(i, "")

        details.append({
            "number": i + 1,
            "question": question,
            "answer": answer,
            **evaluate_answer(question, answer),
            "audio": st.session_state.audio_metrics.get(i, {})
        })

    answered = sum(bool(item["answer"]) for item in details)

    score = (
        round(sum(item["score"] for item in details) / len(details))
        if details else 0
    )

    # Safe name lookup: avoids the original AttributeError / KeyError.
    saved_name = str(
        st.session_state.get("profile_name", "User")
    ).strip() or "User"

    result = {
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "name": saved_name,
        "role": st.session_state.get("role", "General / Student"),
        "experience": st.session_state.get("experience", "Student / Fresher"),
        "type": st.session_state.get("interview_type", "Mixed"),
        "count": len(details),
        "score": score,
        "answered": answered,
        "details": details
    }

    st.session_state.result = result
    st.session_state.history.append(result)
    st.session_state.active = False
    st.session_state.page = "Results Dashboard"


def go_setup():
    st.session_state.page = "Setup"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("# 🎯 InterviewReady")
    st.markdown("**YOUR PERSONAL INTERVIEW STUDIO**")
    st.caption("Practise with purpose. Improve with every attempt.")

    st.divider()

    st.radio(
        "Workspace",
        ["Setup", "Mock Interview", "Results Dashboard"],
        key="page"
    )

    st.divider()

    st.markdown("### ✨ The STAR framework")
    st.markdown("**S**ituation · **T**ask · **A**ction · **R**esult")
    st.caption("A practice companion — not a hiring decision tool.")


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR PERSONAL PRACTICE SPACE</div>
    <h1>InterviewReady</h1>
    <p>
        Practise confidently. Communicate clearly.
        Turn every answer into progress.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SETUP PAGE
# =====================================================

if st.session_state.page == "Setup":

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown("## Build your practice session")
        st.caption("A few details help shape a more relevant interview.")

        st.text_input(
            "Your name",
            key="setup_name",
            on_change=save_profile_name,
            placeholder="e.g. Alex"
        )

        st.selectbox(
            "Target role",
            list(ROLE_QUESTIONS.keys()),
            key="role"
        )

        st.selectbox(
            "Experience level",
            [
                "Student / Fresher",
                "Entry level",
                "1–3 years",
                "3+ years"
            ],
            key="experience"
        )

        st.selectbox(
            "Interview focus",
            list(QUESTION_BANK.keys()),
            key="interview_type"
        )

        st.slider(
            "Questions in this session",
            3,
            10,
            value=5,
            key="question_count"
        )

        if st.session_state.start_error:
            st.error(st.session_state.start_error)

        st.button(
            "🚀 Start my interview",
            type="primary",
            use_container_width=True,
            on_click=start_interview
        )

    with right:
        st.markdown("## Your interview toolkit")

        features = [
            ("🧭", "Guided practice", "One question at a time with clear progress."),
            ("🎙️", "Voice-to-text", "Record an answer and review its editable transcript."),
            ("🪄", "Answer coaching", "See strengths, gaps and practical improvement tips."),
            ("📈", "Performance insights", "Explore skill scores and your practice history.")
        ]

        for icon, title, description in features:
            st.markdown(
                f"""
                <div class="feature">
                    <span style="font-size:1.5rem">{icon}</span>
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("""
        <div class="tip">
            <b>Quick coaching tip</b><br>
            Use a real example. Explain what <i>you</i> did,
            why you did it and what changed because of your actions.
        </div>
        """, unsafe_allow_html=True)

        if sr is None:
            st.info(
                "Voice transcription is unavailable until the speech package "
                "is installed. Typed answers work normally."
            )

    st.markdown(
        '<div class="footer">InterviewReady · Practice data is kept in this browser session. Avoid entering confidential information.</div>',
        unsafe_allow_html=True
    )


# =====================================================
# MOCK INTERVIEW PAGE
# =====================================================

elif st.session_state.page == "Mock Interview":

    if not st.session_state.active:
        st.info("There is no active interview. Start a new session from Setup.")

        st.button("Go to setup", on_click=go_setup)

    else:
        i = st.session_state.index
        total = len(st.session_state.questions)
        question = st.session_state.questions[i]

        key = answer_key(i)
        pending_key = f"pending_{st.session_state.session_id}_{i}"

        if pending_key in st.session_state:
            st.session_state[key] = st.session_state.pop(pending_key)

        elif key not in st.session_state:
            st.session_state[key] = st.session_state.answers.get(i, "")

        top1, top2 = st.columns([3, 1])

        with top1:
            display_name = str(
                st.session_state.get("profile_name", "User")
            ).strip() or "User"

            st.markdown(
                f"## Hello, {html.escape(display_name)} 👋"
            )

        with top2:
            st.markdown(
                f'<div style="text-align:right;padding-top:12px;color:#65728a;font-weight:700">SESSION {st.session_state.session_id:02d}</div>',
                unsafe_allow_html=True
            )

        st.progress(
            (i + 1) / total,
            text=f"Question {i + 1} of {total} · {round((i + 1) / total * 100)}% complete"
        )

        st.markdown(
            f"""
            <div class="question-card">
                <span class="pill">
                    {html.escape(st.session_state.interview_type.upper())}
                </span>
                <h2 style="margin:13px 0 7px">
                    {html.escape(question)}
                </h2>
                <p style="color:#65728a;margin:0">
                    Think clearly, use an example and explain the outcome.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.text_area(
            "Your answer",
            key=key,
            height=190,
            placeholder=(
                "Start with a direct response, then add context, "
                "actions and results..."
            )
        )

        current = str(st.session_state.get(key, "")).strip()

        st.caption(
            f"{word_count(current)} words · "
            "Your answer is saved as you move between questions."
        )

        # VOICE RECORDING
        with st.expander(
            "🎙️ Record your answer and create a transcript",
            expanded=False
        ):
            st.write(
                "Record in a quiet place. Transcription requires an "
                "internet connection and may make mistakes, so review "
                "the text before submitting."
            )

            language = st.selectbox(
                "Speech recognition language",
                ["English (India)", "English (US)", "English (UK)"],
                key=f"lang_{st.session_state.session_id}_{i}"
            )

            lang_code = {
                "English (India)": "en-IN",
                "English (US)": "en-US",
                "English (UK)": "en-GB"
            }[language]

            try:
                audio = st.audio_input(
                    "Record your response",
                    key=audio_key(i)
                )

                if audio is not None:
                    data = audio.getvalue()
                    st.audio(data, format="audio/wav")

                    if st.button(
                        "✨ Transcribe and add to answer",
                        key=f"transcribe_{st.session_state.session_id}_{i}",
                        type="primary"
                    ):
                        with st.spinner("Converting speech to text..."):
                            transcript, error = transcribe(data, lang_code)

                        if transcript:
                            st.session_state[pending_key] = transcript
                            st.session_state.answers[i] = transcript
                            st.session_state.audio_metrics[i] = audio_stats(
                                data, transcript
                            )
                            st.rerun()
                        else:
                            st.warning(
                                error or "Transcription could not be completed."
                            )

            except Exception:
                st.info(
                    "Audio recording is not supported in this browser. "
                    "You can type your answer instead."
                )

        # LIVE ANSWER REVIEW
        current = str(st.session_state.get(key, "")).strip()

        if current:
            review = evaluate_answer(question, current)

            st.markdown("### 🪄 Live coaching snapshot")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric("Practice score", f"{review['score']}/100")
            m2.metric("Answer length", f"{review['words']} words")
            m3.metric("Structure", f"{review['structure']}/25")
            m4.metric("Relevance estimate", f"{review['relevance']}/25")

            good, bad = st.columns(2)

            with good:
                st.markdown("**What is working**")

                for item in review["strengths"]:
                    st.success(item)

                if not review["strengths"]:
                    st.caption("Keep developing your answer to identify strengths.")

            with bad:
                st.markdown("**Try this next**")

                for item in review["feedback"]:
                    st.warning(item)

            with st.expander("🗣️ Communication and wording tips"):
                for item in review["communication"]:
                    st.write("• " + item)

                if review["fillers"]:
                    st.caption(
                        "Detected: "
                        + ", ".join(
                            f"{word}: {count}"
                            for word, count in review["fillers"].items()
                        )
                    )

        # NAVIGATION
        st.divider()

        a, b, c = st.columns([1, 1, 1.25])

        with a:
            st.button(
                "← Previous",
                disabled=(i == 0),
                use_container_width=True,
                on_click=previous_question
            )

        with b:
            if i < total - 1:
                st.button(
                    "Next question →",
                    type="primary",
                    use_container_width=True,
                    on_click=next_question
                )

        with c:
            st.button(
                "Finish interview ✓",
                type="primary",
                use_container_width=True,
                on_click=finish_interview
            )

        st.caption(
            "You can finish early. Unanswered questions will be included "
            "as zero-score items in the session summary."
        )


# =====================================================
# RESULTS DASHBOARD
# =====================================================

elif st.session_state.page == "Results Dashboard":

    st.markdown("## 📊 Your performance studio")

    st.caption(
        "A practical review of this session — celebrate strengths "
        "and choose one area to improve next."
    )

    result = st.session_state.result

    if not result:
        st.markdown("""
        <div class="panel">
            <h3>Your dashboard is waiting for your first practice session.</h3>
            <p>Complete a mock interview to unlock your performance insights.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Start my first interview",
            type="primary",
            on_click=go_setup
        )

    else:
        details = result["details"]
        total = result["count"]
        score = result["score"]
        answered = result["answered"]

        completion = round(answered / total * 100) if total else 0

        if score >= 80:
            level = "Interview-ready momentum"
            subtitle = "Your answers show consistent practice signals."
        elif score >= 60:
            level = "Promising foundation"
            subtitle = (
                "You have a base to build on. "
                "Sharper examples can lift your performance."
            )
        else:
            level = "Growth in progress"
            subtitle = (
                "Every interview is practice. Focus on complete, "
                "specific answers next time."
            )

        x, y = st.columns([1.35, 1])

        with x:
            st.markdown(
                f"""
                <div class="score-hero">
                    <div style="color:#f4bd62;font-size:.75rem;font-weight:800;letter-spacing:.14em">
                        YOUR SESSION RESULT
                    </div>
                    <div class="score-number">
                        {score}
                        <span style="font-size:1.2rem;color:#d9e4ff"> / 100</span>
                    </div>
                    <h3 style="margin:5px 0 8px">{level}</h3>
                    <p style="color:#e1eaff">{subtitle}</p>
                    <div style="margin-top:17px;color:#c8d7f4;font-size:.88rem">
                        {html.escape(result["role"])} ·
                        {html.escape(result["type"])} ·
                        {html.escape(result["date"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with y:
            st.markdown("### Session snapshot")

            st.metric("Questions answered", f"{answered}/{total}")

            st.progress(
                completion / 100,
                text=f"{completion}% completion"
            )

            st.metric("Practice sessions", len(st.session_state.history))

            st.caption(f"Prepared for: {result['experience']}")

        # SKILL BREAKDOWN
        st.markdown("### Your skill map")

        skill_definitions = [
            ("Answer development", "development"),
            ("STAR structure", "structure"),
            ("Specific evidence", "specificity"),
            ("Question relevance", "relevance")
        ]

        skill_rows = []

        for label, key in skill_definitions:
            value = (
                round(sum(item[key] for item in details) / len(details))
                if details else 0
            )

            skill_rows.append({"Skill": label, "Score": value})

        col_chart, col_focus = st.columns([1.25, 1])

        with col_chart:
            st.markdown("""
            <div class="panel">
                <h3>Skill breakdown</h3>
                <p style="color:#65728a">
                    Average score across all questions · out of 25
                </p>
            """, unsafe_allow_html=True)

            for row in skill_rows:
                percentage = round(row["Score"] / 25 * 100)

                st.markdown(
                    f"""
                    <div class="bar-row">
                        <div class="bar-label">
                            <span>{row["Skill"]}</span>
                            <span>{row["Score"]}/25</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width:{percentage}%"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with col_focus:
            weakest = min(skill_rows, key=lambda row: row["Score"])
            strongest = max(skill_rows, key=lambda row: row["Score"])

            st.markdown(
                f"""
                <div class="panel">
                    <div style="font-size:1.5rem">🏆</div>
                    <h3>Strongest signal</h3>
                    <p>{strongest["Skill"]}</p>
                    <h2 style="color:#2e65c8!important">
                        {strongest["Score"]}/25
                    </h2>
                    <hr>
                    <div style="font-size:1.5rem">🎯</div>
                    <h3>Next growth area</h3>
                    <p>{weakest["Skill"]}</p>
                    <h2 style="color:#c27a22!important">
                        {weakest["Score"]}/25
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        # PERSONAL IMPROVEMENT PLAN
        st.markdown("### Your next-practice plan")

        plan = []

        if weakest["Skill"] == "Answer development":
            plan.append(
                "Aim for a focused 45–120 word answer: direct response, context, action and outcome."
            )

        elif weakest["Skill"] == "STAR structure":
            plan.append(
                "Practise the STAR sequence. Spend the most time explaining your own Action and the Result."
            )

        elif weakest["Skill"] == "Specific evidence":
            plan.append(
                "Add concrete evidence: tools used, your contribution, scale, time saved or measurable outcome."
            )

        else:
            plan.append(
                "Start by answering the exact question in one sentence, then support it with a relevant example."
            )

        plan += [
            "Prepare two different examples from study, projects, internships or work.",
            "Practise aloud once, remove repeated phrases and end with a clear outcome."
        ]

        for number, item in enumerate(plan, 1):
            st.markdown(f"**{number}.** {item}")

        # QUESTION-WISE FEEDBACK
        st.markdown("### Question-by-question coaching")

        for item in details:
            with st.expander(
                f"Q{item['number']} · {item['score']}/100 · {item['question']}"
            ):
                st.markdown("**Your answer**")

                st.write(
                    item["answer"]
                    if item["answer"]
                    else "No answer submitted."
                )

                z1, z2, z3, z4 = st.columns(4)

                z1.metric("Development", f"{item['development']}/25")
                z2.metric("Structure", f"{item['structure']}/25")
                z3.metric("Specificity", f"{item['specificity']}/25")
                z4.metric("Relevance", f"{item['relevance']}/25")

                if item["strengths"]:
                    st.markdown("**Strengths**")

                    for message in item["strengths"]:
                        st.success(message)

                if item["feedback"]:
                    st.markdown("**Improvement suggestions**")

                    for message in item["feedback"]:
                        st.warning(message)

                if item["communication"]:
                    st.markdown("**Communication notes**")

                    for message in item["communication"]:
                        st.write("• " + message)

                if item["audio"]:
                    audio = item["audio"]

                    st.caption(
                        f"Voice practice: "
                        f"{audio.get('duration') or 'N/A'} sec recording · "
                        f"{audio.get('wpm') or 'N/A'} estimated words/minute"
                    )

        # PRACTICE HISTORY
        st.markdown("### Practice history")

        history_df = pd.DataFrame([
            {
                "Date": h["date"],
                "Role": h["role"],
                "Focus": h["type"],
                "Answered": f"{h['answered']}/{h['count']}",
                "Score": h["score"]
            }
            for h in st.session_state.history
        ])

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        if len(history_df) > 1:
            st.markdown("**Score progression**")

            trend = pd.DataFrame(
                {
                    "Session score": [
                        h["score"]
                        for h in st.session_state.history
                    ]
                },
                index=[
                    f"Session {i + 1}"
                    for i in range(len(st.session_state.history))
                ]
            )

            st.line_chart(trend, height=220)

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download practice history (CSV)",
            csv,
            "interviewready_history.csv",
            "text/csv",
            use_container_width=True
        )

        st.button(
            "🔄 Start a fresh interview",
            type="primary",
            use_container_width=True,
            on_click=go_setup
        )

        st.markdown("""
        <div class="tip">
            <b>How to read these results</b><br>
            Scores are transparent text-pattern practice estimates,
            not a trained AI assessment or a prediction of hiring success.
            Relevance is estimated using word overlap. Speech pace is
            approximate and depends on transcription accuracy.
            Session history is temporary and may reset when the app restarts.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">InterviewReady · Do not enter passwords, financial details or confidential personal information.</div>',
        unsafe_allow_html=True
    )

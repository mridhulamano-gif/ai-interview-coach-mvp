import io
import re
import wave
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import speech_recognition as sr
except Exception:
    sr = None

st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# ==========================================================
# DESIGN AND STYLING
# ==========================================================

st.markdown("""
<style>
:root {
    --navy: #101d36;
    --blue: #3568c8;
    --gold: #f2bd55;
    --ink: #18263d;
    --muted: #52627a;
    --line: #d9e2ef;
    --page: #f3f6fb;
}

.stApp {
    background: var(--page);
    color: var(--ink);
}

[data-testid="stSidebar"] {
    background: var(--navy);
}

[data-testid="stSidebar"] * {
    color: #f7f9ff !important;
}

h1, h2, h3, h4 {
    color: var(--navy) !important;
    font-weight: 780 !important;
}

p, li {
    color: var(--ink);
}

[data-testid="stWidgetLabel"] p {
    color: #263954 !important;
    font-weight: 650;
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

input, textarea {
    color: #17243b !important;
    background: #ffffff !important;
    -webkit-text-fill-color: #17243b !important;
}

textarea::placeholder, input::placeholder {
    color: #738198 !important;
    -webkit-text-fill-color: #738198 !important;
}

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #17243b !important;
    border-color: #b9c7da !important;
}

div[data-baseweb="select"] * {
    color: #17243b !important;
}

[role="listbox"] * {
    color: #17243b !important;
    background: #ffffff !important;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--line);
    padding: 13px 15px;
    border-radius: 13px;
    box-shadow: 0 3px 12px #101d3608;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    color: var(--navy) !important;
}

.hero {
    background: linear-gradient(
        118deg,
        #101d36,
        #24477e 72%,
        #3568c8
    );
    padding: 28px 32px;
    border-radius: 18px;
    margin: 2px 0 24px;
    box-shadow: 0 10px 26px #101d3620;
}

.hero h1 {
    color: white !important;
    margin: 0 0 7px;
    font-size: 2.2rem;
}

.hero p {
    color: #eaf1ff !important;
    margin: 0;
}

.eyebrow {
    color: var(--gold) !important;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    font-size: .75rem;
    margin-bottom: 8px;
}

.panel {
    background: white;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 18px 20px;
    margin: 10px 0;
    box-shadow: 0 3px 13px #101d3608;
}

.question {
    background: white;
    border: 1px solid var(--line);
    border-left: 5px solid var(--gold);
    border-radius: 14px;
    padding: 20px 22px;
    margin: 12px 0 18px;
}

.tag {
    display: inline-block;
    background: #eaf1ff;
    color: #244b98;
    padding: 5px 10px;
    border-radius: 25px;
    font-size: .78rem;
    font-weight: 750;
}

.tip {
    background: #eaf1ff;
    color: #233d66;
    border-left: 4px solid var(--blue);
    border-radius: 9px;
    padding: 13px 15px;
    margin: 10px 0;
}

.footer {
    color: #687890 !important;
    font-size: .79rem;
    padding: 20px 0;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 700;
    border: 1px solid #c7d3e3;
}

div.stButton > button[kind="primary"] {
    background: #d84c54;
    color: white;
    border: 0;
}

div.stButton > button[kind="primary"]:hover {
    background: #b93e48;
    color: white;
}

[data-testid="stProgress"] > div > div {
    background: var(--blue);
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# INTERVIEW QUESTION BANK
# ==========================================================

QUESTION_BANK = {

    "HR / Behavioral": [
        "Tell me about yourself and what makes you suitable for this role?",
        "What are your greatest strengths, and how have you demonstrated them?",
        "Describe a challenge you faced and how you overcame it.",
        "Tell me about a time you worked successfully in a team.",
        "Describe a mistake you made and what you learned from it.",
        "How do you manage multiple deadlines?",
        "Tell me about a time you handled disagreement with a teammate.",
        "Why do you want this role?",
        "Describe a situation where you took initiative.",
        "Where do you see yourself in five years?",
        "How do you respond to constructive criticism?",
        "What motivates you to perform your best?",
    ],

    "Technical": [
        "Explain a technical project you have worked on and your contribution.",
        "Describe how you would debug a problem you cannot immediately solve.",
        "Explain a technical concept in your field to a beginner.",
        "How do you test your work and ensure its quality?",
        "Describe a technical challenge and the steps you took to solve it.",
        "How do you learn a new programming language or technology?",
        "How would you investigate a slow-running application?",
        "Explain a project decision and the alternatives you considered.",
        "How do you approach a problem when requirements are unclear?",
        "Describe a time you improved an existing solution.",
        "How would you explain a trade-off between performance and maintainability?",
        "What technical skill are you currently improving, and why?",
    ],

    "Situational": [
        "What would you do if you were given a task with unclear instructions?",
        "How would you handle a disagreement with your manager?",
        "What would you do if you realised you might miss a deadline?",
        "How would you respond to a dissatisfied customer?",
        "What would you do if a teammate was not contributing?",
        "How would you prioritise two urgent tasks?",
        "What would you do if you discovered an error in your work after submission?",
        "How would you handle an unfamiliar task with a short deadline?",
        "What would you do if you received conflicting feedback?",
        "How would you respond if you did not know the answer to an interview question?",
        "How would you communicate a project delay to stakeholders?",
        "How would you approach a task when success criteria are unclear?",
    ],
}


ROLE_QUESTIONS = {

    "Software / IT": [
        "Explain a project where you used programming to solve a real problem.",
        "How would you find and fix a bug that occurs only occasionally?",
        "How do you choose suitable data structures for a problem?",
        "How would you collaborate with a team using Git?",
    ],

    "Data Science / Analytics": [
        "How would you handle missing values in a dataset?",
        "Explain the difference between classification and regression.",
        "How would you communicate a complex data insight to a non-technical audience?",
        "How would you check whether a model is overfitting?",
    ],

    "Business / Management": [
        "How would you prioritise competing business objectives?",
        "Describe how you would resolve a disagreement within a team.",
        "How would you measure whether a project was successful?",
        "How would you communicate an unpopular decision?",
    ],

    "Marketing / Sales": [
        "How would you identify the target audience for a new product?",
        "How would you measure the success of a marketing campaign?",
        "How would you respond to a potential customer who rejects your proposal?",
        "How would you use customer feedback to improve a campaign?",
    ],

    "General / Student": [
        "Tell me about an academic project you are proud of.",
        "Describe a time you learned a difficult skill.",
        "How do you manage your studies and other responsibilities?",
        "What would you contribute to this organisation?",
    ],
}


FILLERS = [
    "um",
    "uh",
    "erm",
    "actually",
    "basically",
    "literally",
    "you know",
    "i mean",
    "like",
]


# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULTS = {
    "page": "Setup",
    "name": "",
    "role": "General / Student",
    "experience": "Student / Fresher",
    "interview_type": "HR / Behavioral",
    "question_count": 5,
    "questions": [],
    "index": 0,
    "answers": {},
    "audio": {},
    "audio_metrics": {},
    "history": [],
    "result": None,
    "active": False,
    "started": None,
    "session_id": 0,
    "start_error": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# ANSWER ANALYSIS FUNCTIONS
# ==========================================================

def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def filler_counts(text):
    low = (text or "").lower()

    return {
        word: len(
            re.findall(r"\b" + re.escape(word) + r"\b", low)
        )
        for word in FILLERS
        if re.search(r"\b" + re.escape(word) + r"\b", low)
    }


def evaluate_answer(question, answer):

    answer = (answer or "").strip()
    words = word_count(answer)

    if not answer:
        return {
            "score": 0,
            "development": 0,
            "structure": 0,
            "specificity": 0,
            "relevance": 0,
            "words": 0,
            "feedback": [
                "Write or transcribe an answer before finishing this question."
            ],
            "strengths": [],
            "fillers": {},
            "communication": [],
        }

    low = answer.lower()

    # Answer development: 25 marks

    if words < 10:
        development = 5
    elif words < 25:
        development = 12
    elif words < 45:
        development = 18
    elif words <= 160:
        development = 25
    else:
        development = 21

    # Structure: 25 marks

    groups = [
        ["situation", "context"],
        ["task", "goal", "responsible"],
        ["action", "implemented", "developed"],
        ["result", "outcome", "achieved", "improved", "learned"],
    ]

    hits = sum(
        any(term in low for term in group)
        for group in groups
    )

    sequence = any(
        word in low
        for word in [
            "first",
            "then",
            "after that",
            "finally",
            "as a result",
        ]
    )

    structure = (
        min(25, 7 + hits * 4 + (2 if sequence else 0))
        if words >= 10 else 3
    )

    # Specificity: 25 marks

    terms = [
        "project", "team", "customer", "deadline",
        "data", "developed", "created", "analysed",
        "analyzed", "tested", "measured", "implemented",
        "achieved", "improved", "reduced", "increased",
        "example", "result",
    ]

    specific_hits = sum(term in low for term in terms)

    has_number = bool(
        re.search(r"\b\d+(?:[.,]\d+)?%?\b", low)
    )

    specificity = (
        min(25, 5 + specific_hits * 2 + (4 if has_number else 0))
        if words >= 10 else 3
    )

    # Relevance: 25 marks (keyword-overlap estimate)

    stop = {
        "tell", "about", "what", "when", "where",
        "which", "would", "could", "should", "have",
        "your", "with", "that", "this", "from",
        "into", "describe", "explain", "time",
        "role", "work", "they", "them", "how",
    }

    qterms = (
        set(re.findall(r"\b[a-z]{4,}\b", question.lower()))
        - stop
    )

    aterms = set(
        re.findall(r"\b[a-z]{4,}\b", low)
    )

    relevance = (
        min(25, 9 + len(qterms & aterms) * 4)
        if words >= 10 else 3
    )

    score = min(
        100,
        development + structure + specificity + relevance
    )

    feedback = []
    strengths = []
    communication = []

    if words < 25:
        feedback.append(
            "Develop your answer with context, your actions and the outcome."
        )
    elif words <= 160:
        strengths.append(
            "Your answer has a useful amount of detail."
        )
    else:
        feedback.append(
            "Shorten the answer and remove repeated or less relevant details."
        )

    if hits >= 3:
        strengths.append(
            "Your answer contains several parts of a STAR-style structure."
        )
    else:
        feedback.append(
            "Use STAR: Situation, Task, Action and Result."
        )

    if specific_hits >= 4 or has_number:
        strengths.append(
            "You included concrete details or evidence."
        )
    else:
        feedback.append(
            "Add a real example, your personal contribution or a measurable result."
        )

    if relevance < 14:
        feedback.append(
            "Answer the exact question directly in your opening sentence."
        )

    fillers = filler_counts(answer)
    total_fillers = sum(fillers.values())

    if total_fillers >= 4:
        communication.append(
            f"Reduce filler words; {total_fillers} were found in the transcript."
        )
    elif total_fillers:
        communication.append(
            "A few filler words were found. Try a short pause instead."
        )
    else:
        communication.append(
            "No common filler-word pattern was found in the transcript."
        )

    if any(
        phrase in low
        for phrase in [
            "i think maybe",
            "i guess",
            "sort of",
            "kind of",
            "not sure",
        ]
    ):
        communication.append(
            "Replace vague phrases with a clear explanation while staying honest."
        )

    return {
        "score": score,
        "development": development,
        "structure": structure,
        "specificity": specificity,
        "relevance": relevance,
        "words": words,
        "feedback": feedback,
        "strengths": strengths,
        "fillers": fillers,
        "communication": communication,
    }


# ==========================================================
# AUDIO ANALYSIS AND SPEECH RECOGNITION
# ==========================================================

def audio_stats(data, transcript):

    try:
        with wave.open(io.BytesIO(data), "rb") as wav:

            duration = (
                wav.getnframes() / float(wav.getframerate())
            )

            frames = wav.readframes(wav.getnframes())
            width = wav.getsampwidth()

        peak = None

        if width == 2:
            import array

            values = array.array("h")
            values.frombytes(
                frames[:len(frames) - len(frames) % 2]
            )

            peak = (
                max((abs(v) for v in values), default=0)
                / 32768
            )

        words = word_count(transcript)

        wpm = (
            round(words / (duration / 60))
            if duration > 0 and words else None
        )

        return {
            "duration": round(duration, 1),
            "peak": round(peak, 3) if peak is not None else None,
            "wpm": wpm,
        }

    except Exception:
        return {
            "duration": None,
            "peak": None,
            "wpm": None,
        }


def transcribe(data, language):

    if sr is None:
        return None, (
            "SpeechRecognition is not installed. "
            "Install the packages listed below."
        )

    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(data)) as source:
            recording = recognizer.record(source)

        transcript = recognizer.recognize_google(
            recording,
            language=language,
        )

        return transcript, None

    except sr.UnknownValueError:
        return None, (
            "The service could not understand the recording. "
            "Try again in a quiet place."
        )

    except sr.RequestError as exc:
        return None, (
            f"Speech recognition service unavailable: {exc}. "
            "You can type your answer instead."
        )

    except Exception as exc:
        return None, f"Could not process this audio: {exc}"


# ==========================================================
# INTERVIEW CALLBACKS
# ==========================================================

def start_interview():

    if not st.session_state.name.strip():
        st.session_state.start_error = (
            "Please enter your name first."
        )
        return

    st.session_state.start_error = ""

    st.session_state.session_id += 1

    pool = (
        QUESTION_BANK[st.session_state.interview_type]
        + ROLE_QUESTIONS[st.session_state.role]
    )

    offset = (
        st.session_state.session_id - 1
    ) % len(pool)

    pool = pool[offset:] + pool[:offset]

    st.session_state.questions = pool[
        :st.session_state.question_count
    ]

    st.session_state.index = 0
    st.session_state.answers = {}
    st.session_state.audio = {}
    st.session_state.audio_metrics = {}
    st.session_state.active = True
    st.session_state.result = None
    st.session_state.started = datetime.now()
    st.session_state.page = "Mock Interview"


def save_answer():

    index = st.session_state.index
    key = f"answer_{index}"

    st.session_state.answers[index] = (
        st.session_state.get(key, "").strip()
    )


def next_question():

    save_answer()

    st.session_state.index = min(
        st.session_state.index + 1,
        len(st.session_state.questions) - 1,
    )


def previous_question():

    save_answer()

    st.session_state.index = max(
        0,
        st.session_state.index - 1,
    )


def finish_interview():

    save_answer()

    details = []

    for i, question in enumerate(
        st.session_state.questions
    ):

        answer = st.session_state.answers.get(i, "")

        details.append({
            "number": i + 1,
            "question": question,
            "answer": answer,
            **evaluate_answer(question, answer),
            "audio": st.session_state.audio_metrics.get(i, {}),
        })

    average = (
        round(
            sum(x["score"] for x in details)
            / len(details)
        )
        if details else 0
    )

    result = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": st.session_state.name,
        "role": st.session_state.role,
        "experience": st.session_state.experience,
        "type": st.session_state.interview_type,
        "count": len(details),
        "score": average,
        "answered": sum(
            bool(x["answer"]) for x in details
        ),
        "details": details,
    }

    st.session_state.result = result
    st.session_state.history.append(result)
    st.session_state.active = False
    st.session_state.page = "Results Dashboard"


def go_setup():
    st.session_state.page = "Setup"


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("# 🎯 InterviewReady")

    st.markdown(
        "**AI Interview Coach · Practice MVP**"
    )

    st.caption(
        "Practise. Improve. Build confidence."
    )

    st.divider()

    st.radio(
        "Navigate",
        [
            "Setup",
            "Mock Interview",
            "Results Dashboard",
        ],
        key="page",
    )

    st.divider()

    st.markdown("### 💡 STAR method")

    st.markdown(
        "**S**ituation · **T**ask · "
        "**A**ction · **R**esult"
    )

    st.caption(
        "Free-first demo · Practice guidance, not a hiring decision"
    )


# ==========================================================
# MAIN HEADER
# ==========================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">Your personal practice space</div>
    <h1>InterviewReady</h1>
    <p>
        Practise confidently. Communicate clearly.
        Turn every answer into progress.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# SETUP PAGE
# ==========================================================

if st.session_state.page == "Setup":

    left, right = st.columns(
        [1.45, 1],
        gap="large",
    )

    with left:

        st.subheader(
            "Set up your mock interview"
        )

        st.write(
            "Choose your target role and interview style."
        )

        st.text_input(
            "Your name",
            key="name",
            placeholder="Enter your name",
        )

        st.selectbox(
            "Target role",
            list(ROLE_QUESTIONS.keys()),
            key="role",
        )

        st.selectbox(
            "Experience level",
            [
                "Student / Fresher",
                "Entry level",
                "1–3 years",
                "3+ years",
            ],
            key="experience",
        )

        st.selectbox(
            "Interview type",
            list(QUESTION_BANK.keys()),
            key="interview_type",
        )

        st.slider(
            "Number of questions",
            3,
            10,
            key="question_count",
        )

        if st.session_state.start_error:
            st.error(st.session_state.start_error)

        st.button(
            "🚀 Start mock interview",
            type="primary",
            use_container_width=True,
            on_click=start_interview,
        )

    with right:

        st.subheader("What you will get")

        st.markdown("""
        <div class="panel">

        <h3>🧭 Guided interview</h3>
        <p>One question at a time with progress tracking.</p>

        <hr>

        <h3>🎙️ Voice-to-text practice</h3>
        <p>Record an answer and convert speech into editable text.</p>

        <hr>

        <h3>📝 Answer coaching</h3>
        <p>Review structure, detail, relevance and communication tips.</p>

        <hr>

        <h3>📊 Performance dashboard</h3>
        <p>Explore skill scores, voice indicators and practice history.</p>

        </div>

        <div class="tip">
        <b>Practice tip:</b>
        Give a real example, explain what you personally did
        and finish with the result.
        </div>
        """, unsafe_allow_html=True)

        if sr is None:
            st.warning(
                "Speech-to-text package is not available "
                "until requirements are installed."
            )

    st.markdown(
        '<div class="footer">InterviewReady MVP · Avoid entering confidential personal information.</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# MOCK INTERVIEW PAGE
# ==========================================================

elif st.session_state.page == "Mock Interview":

    if not st.session_state.active:

        st.info(
            "No active interview. Start a session from Setup."
        )

        st.button(
            "Go to Setup",
            on_click=go_setup,
        )

    else:

        i = st.session_state.index
        total = len(st.session_state.questions)
        question = st.session_state.questions[i]

        key = f"answer_{i}"
        pending = f"pending_transcript_{i}"

        # Apply transcript before creating the text-area widget.
        if pending in st.session_state:

            st.session_state[key] = (
                st.session_state.pop(pending)
            )

        elif key not in st.session_state:

            st.session_state[key] = (
                st.session_state.answers.get(i, "")
            )

        st.subheader("Mock interview")

        st.write(
            f"Hello, **{st.session_state.name.strip()}**. "
            "Take your time and answer naturally."
        )

        st.progress((i + 1) / total)

        st.caption(
            f"QUESTION {i + 1} OF {total} · "
            f"{st.session_state.role}"
        )

        st.markdown(
            f"""
            <div class="question">
                <span class="tag">
                    {st.session_state.interview_type}
                </span>
                <h3 style="margin-top:12px">
                    {question}
                </h3>
                <p style="color:#52627a">
                    Use a clear example and explain the outcome.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Your answer (type or edit your transcript)",
            key=key,
            height=175,
            placeholder="Write your answer here...",
        )

        current = st.session_state.get(
            key, ""
        ).strip()

        st.caption(
            f"Word count: {word_count(current)}"
        )

        # ---------------- VOICE INPUT ----------------

        st.markdown("### 🎙️ Record and transcribe")

        st.write(
            "Record your answer, then click Transcribe. "
            "Check the transcript for recognition errors."
        )

        language = st.selectbox(
            "Recognition language",
            [
                "English (India)",
                "English (US)",
                "English (UK)",
            ],
            key=f"language_{i}",
        )

        lang_code = {
            "English (India)": "en-IN",
            "English (US)": "en-US",
            "English (UK)": "en-GB",
        }[language]

        try:

            audio = st.audio_input(
                "Record your answer",
                key=f"audio_input_{i}",
            )

            if audio is not None:

                data = audio.getvalue()

                st.session_state.audio[i] = data

                st.audio(
                    data,
                    format="audio/wav",
                )

                if st.button(
                    "✨ Transcribe recording",
                    key=f"transcribe_{i}",
                    type="primary",
                ):

                    with st.spinner(
                        "Transcribing your speech..."
                    ):

                        transcript, error = transcribe(
                            data,
                            lang_code,
                        )

                    if transcript:

                        st.session_state[pending] = transcript

                        st.session_state.answers[i] = transcript

                        st.session_state.audio_metrics[i] = (
                            audio_stats(data, transcript)
                        )

                        st.session_state[
                            f"transcription_status_{i}"
                        ] = (
                            "Transcript added to the answer box. "
                            "Please review and edit it."
                        )

                        st.rerun()

                    else:

                        st.session_state[
                            f"transcription_status_{i}"
                        ] = error

                status = st.session_state.get(
                    f"transcription_status_{i}",
                    "",
                )

                if status:

                    if status.startswith("Transcript"):
                        st.success(status)
                    else:
                        st.warning(status)

                metrics = st.session_state.audio_metrics.get(
                    i, {}
                )

                if metrics:

                    a, b, c = st.columns(3)

                    a.metric(
                        "Recording length",
                        (
                            f"{metrics['duration']} sec"
                            if metrics["duration"] is not None
                            else "N/A"
                        ),
                    )

                    b.metric(
                        "Estimated pace",
                        (
                            f"{metrics['wpm']} WPM"
                            if metrics["wpm"]
                            else "N/A"
                        ),
                    )

                    c.metric(
                        "Audio peak",
                        (
                            f"{metrics['peak']}"
                            if metrics["peak"] is not None
                            else "N/A"
                        ),
                    )

        except Exception:

            st.info(
                "Audio recording is unavailable in this browser. "
                "You can still type your answer."
            )

        # ---------------- LIVE ANSWER REVIEW ----------------

        current = st.session_state.get(
            key, ""
        ).strip()

        if current:

            review = evaluate_answer(
                question,
                current,
            )

            st.markdown("### ⚡ Live answer review")

            a, b, c, d = st.columns(4)

            a.metric(
                "Practice score",
                f"{review['score']}/100",
            )

            b.metric(
                "Words",
                review["words"],
            )

            c.metric(
                "Structure",
                f"{review['structure']}/25",
            )

            d.metric(
                "Specificity",
                f"{review['specificity']}/25",
            )

            good, improve = st.columns(2)

            with good:

                st.markdown("**Strengths**")

                for item in review["strengths"]:
                    st.success(item)

                if not review["strengths"]:
                    st.caption(
                        "Add more detail to identify strengths."
                    )

            with improve:

                st.markdown("**Improvement actions**")

                for item in review["feedback"]:
                    st.warning(item)

            with st.expander(
                "🗣️ Communication and wording tips"
            ):

                for item in review["communication"]:
                    st.write("• " + item)

                if review["fillers"]:

                    st.caption(
                        "Detected in transcript: "
                        + ", ".join(
                            f"{w}: {n}"
                            for w, n in review["fillers"].items()
                        )
                    )

        # ---------------- NAVIGATION ----------------

        st.divider()

        pcol, ncol, fcol = st.columns(
            [1, 1, 1.2]
        )

        with pcol:

            st.button(
                "← Previous",
                disabled=(i == 0),
                use_container_width=True,
                on_click=previous_question,
            )

        with ncol:

            if i < total - 1:

                st.button(
                    "Next question →",
                    type="primary",
                    use_container_width=True,
                    on_click=next_question,
                )

        with fcol:

            st.button(
                "Finish interview",
                type="primary",
                use_container_width=True,
                on_click=finish_interview,
            )

        st.markdown(
            '<div class="footer">Review your transcript before finishing. Speech recognition can mishear words.</div>',
            unsafe_allow_html=True,
        )


# ==========================================================
# RESULTS DASHBOARD
# ==========================================================

elif st.session_state.page == "Results Dashboard":

    st.subheader("📊 Your performance dashboard")

    st.write(
        "Review your latest session and identify what to practise next."
    )

    result = st.session_state.result

    if not result:

        st.info(
            "Your dashboard will appear after you complete a mock interview."
        )

        st.button(
            "Start your first interview",
            type="primary",
            on_click=go_setup,
        )

    else:

        st.markdown(
            f"### Results for {result['name']}"
        )

        st.caption(
            f"{result['role']} · "
            f"{result['experience']} · "
            f"{result['type']} · "
            f"{result['date']}"
        )

        voice_count = sum(
            bool(x["audio"])
            for x in result["details"]
        )

        pace_values = [
            x["audio"].get("wpm")
            for x in result["details"]
            if x["audio"].get("wpm")
        ]

        avg_pace = (
            round(sum(pace_values) / len(pace_values))
            if pace_values else None
        )

        a, b, c, d, e = st.columns(5)

        a.metric(
            "Overall score",
            f"{result['score']}/100",
        )

        b.metric(
            "Answered",
            f"{result['answered']}/{result['count']}",
        )

        c.metric(
            "Recordings",
            voice_count,
        )

        d.metric(
            "Avg. speech pace",
            f"{avg_pace} WPM" if avg_pace else "N/A",
        )

        e.metric(
            "Sessions",
            len(st.session_state.history),
        )

        if result["score"] >= 80:

            st.success(
                "Strong practice result. Refine your examples "
                "and keep your delivery natural."
            )

        elif result["score"] >= 60:

            st.info(
                "Good foundation. Focus on stronger examples "
                "and clearer structure."
            )

        else:

            st.warning(
                "Keep practising complete answers with "
                "context, actions and outcomes."
            )

        # ---------------- SKILL BREAKDOWN ----------------

        st.markdown("### Skill breakdown")

        skill_rows = []

        for label, key in [
            ("Development", "development"),
            ("Structure", "structure"),
            ("Specificity", "specificity"),
            ("Relevance", "relevance"),
        ]:

            value = (
                round(
                    sum(x[key] for x in result["details"])
                    / len(result["details"])
                )
                if result["details"] else 0
            )

            skill_rows.append({
                "Skill": label,
                "Average score": value,
            })

        chart, priorities = st.columns(
            [1.2, 1]
        )

        with chart:

            chart_df = pd.DataFrame(
                skill_rows
            ).set_index("Skill")

            st.bar_chart(
                chart_df,
                height=290,
            )

        with priorities:

            st.markdown(
                '<div class="panel"><h3>Coaching priorities</h3>',
                unsafe_allow_html=True,
            )

            for row in sorted(
                skill_rows,
                key=lambda r: r["Average score"],
            )[:3]:

                st.write(
                    f"**{row['Skill']} — "
                    f"{row['Average score']} / 25**"
                )

                st.progress(
                    min(
                        1.0,
                        row["Average score"] / 25,
                    )
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        # ---------------- QUESTION FEEDBACK ----------------

        st.markdown(
            "### Question-by-question feedback"
        )

        for item in result["details"]:

            with st.expander(
                f"Q{item['number']}. "
                f"{item['question']} · "
                f"{item['score']}/100"
            ):

                st.markdown(
                    "**Your answer / transcript**"
                )

                st.write(
                    item["answer"]
                    if item["answer"]
                    else "No answer submitted."
                )

                x1, x2, x3, x4 = st.columns(4)

                x1.metric(
                    "Development",
                    f"{item['development']}/25",
                )

                x2.metric(
                    "Structure",
                    f"{item['structure']}/25",
                )

                x3.metric(
                    "Specificity",
                    f"{item['specificity']}/25",
                )

                x4.metric(
                    "Relevance",
                    f"{item['relevance']}/25",
                )

                if item["strengths"]:

                    st.markdown("**Strengths**")

                    for msg in item["strengths"]:
                        st.success(msg)

                if item["feedback"]:

                    st.markdown("**How to improve**")

                    for msg in item["feedback"]:
                        st.warning(msg)

                if item["communication"]:

                    st.markdown("**Communication tips**")

                    for msg in item["communication"]:
                        st.write("• " + msg)

                if item["audio"]:

                    am = item["audio"]

                    st.markdown(
                        "**Voice practice indicators**"
                    )

                    q1, q2, q3 = st.columns(3)

                    q1.metric(
                        "Duration",
                        (
                            f"{am['duration']} sec"
                            if am["duration"] is not None
                            else "N/A"
                        ),
                    )

                    q2.metric(
                        "Pace",
                        (
                            f"{am['wpm']} WPM"
                            if am["wpm"]
                            else "N/A"
                        ),
                    )

                    q3.metric(
                        "Peak level",
                        (
                            str(am["peak"])
                            if am["peak"] is not None
                            else "N/A"
                        ),
                    )

        # ---------------- PRACTICE HISTORY ----------------

        st.markdown("### Practice history")

        history_df = pd.DataFrame([
            {
                "Date": h["date"],
                "Candidate": h["name"],
                "Role": h["role"],
                "Interview type": h["type"],
                "Questions": h["count"],
                "Answered": h["answered"],
                "Score": h["score"],
            }
            for h in st.session_state.history
        ])

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        if len(history_df) > 1:

            st.markdown(
                "#### Score progression"
            )

            trend = history_df[["Score"]].copy()

            trend.index = [
                f"Session {i + 1}"
                for i in range(len(trend))
            ]

            st.line_chart(
                trend,
                height=230,
            )

        st.download_button(
            "⬇️ Download practice history (CSV)",
            history_df.to_csv(index=False).encode("utf-8"),
            "interviewready_history.csv",
            "text/csv",
            use_container_width=True,
        )

        st.button(
            "🔄 Start another interview",
            type="primary",
            use_container_width=True,
            on_click=go_setup,
        )

        st.markdown("""
        <div class="tip">
        <b>Important:</b>
        Scores use transparent text-pattern rules, not a trained AI model.
        Speech-to-text may make mistakes. Audio peak is not a measure
        of confidence, emotion or voice quality.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">InterviewReady MVP · Session history may reset when the app restarts. Do not enter confidential personal information.</div>',
        unsafe_allow_html=True,
    )

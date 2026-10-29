
import io
import math
import struct
import wave
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# INTERVIEWREADY — FREE AI INTERVIEW COACH MVP
# =========================================================

st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# High-contrast, consistent theme
st.markdown(
    """
    <style>
    :root {
        --navy: #14213d;
        --blue: #3159a8;
        --red: #ef5350;
        --ink: #18243a;
        --muted: #53627a;
        --paper: #f3f6fc;
        --white: #ffffff;
        --line: #d8e1ef;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(243,246,252,0.96);
    }

    [data-testid="stSidebar"] {
        background: var(--navy);
        border-right: 1px solid #283b60;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent;
        border-radius: 8px;
        padding: 5px;
    }

    h1, h2, h3, h4 {
        color: var(--navy) !important;
        letter-spacing: -0.3px;
    }

    p, li, label, .stMarkdown {
        color: var(--ink);
    }

    [data-testid="stWidgetLabel"] p {
        color: #243654 !important;
        font-weight: 600 !important;
    }

    input, textarea {
        color: #17233c !important;
        background: #ffffff !important;
        border: 1px solid #bac8dd !important;
        border-radius: 9px !important;
    }

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #bac8dd !important;
        color: #17233c !important;
    }

    [data-baseweb="select"] * {
        color: #17233c !important;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 17px;
        box-shadow: 0 2px 7px rgba(20,33,61,0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #52627a !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-weight: 750;
    }

    .hero {
        background: linear-gradient(115deg, #14213d, #3159a8);
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 24px;
        color: #ffffff !important;
    }

    .hero h1, .hero p, .hero span {
        color: #ffffff !important;
    }

    .hero h1 {
        margin-bottom: 8px;
        font-size: 2.1rem;
    }

    .hero p {
        margin-bottom: 0;
        font-size: 1rem;
    }

    .panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .eyebrow {
        color: #3159a8 !important;
        font-size: 0.78rem;
        font-weight: 750;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .notice {
        background: #e5efff;
        border-left: 4px solid #3159a8;
        color: #18345e !important;
        padding: 14px 17px;
        border-radius: 9px;
        margin: 12px 0;
    }

    .notice * {
        color: #18345e !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: var(--red);
        color: #ffffff !important;
        border: 1px solid var(--red);
        border-radius: 9px;
        min-height: 43px;
        font-weight: 650;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #d83e43;
        border-color: #d83e43;
        color: #ffffff !important;
    }

    .stProgress > div > div > div {
        background: var(--red);
    }

    hr {
        border-color: var(--line);
    }

    [data-testid="stAlert"] p {
        color: inherit !important;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------ QUESTION BANK ------------------

QUESTION_BANK = {
    "HR / Behavioral": {
        "General / Student": [
            ("Introduce yourself and explain your main strengths.", "Introduction"),
            ("Why do you want this opportunity?", "Motivation"),
            ("Describe a challenge you faced and how you handled it.", "Problem solving"),
            ("Tell me about a time you worked in a team.", "Teamwork"),
            ("What is one weakness you are actively improving?", "Self-awareness"),
            ("Describe a mistake and what you learned from it.", "Learning"),
            ("How do you manage deadlines and competing tasks?", "Time management"),
            ("Where do you see yourself in five years?", "Career goals"),
            ("Why should we select you?", "Role fit"),
            ("Tell me about an achievement you are proud of.", "Achievement"),
        ],
        "Software / IT": [
            ("Introduce yourself and your technical strengths.", "Introduction"),
            ("Describe a difficult technical problem you solved.", "Problem solving"),
            ("Tell me about a project you built and your contribution.", "Project"),
            ("How do you handle feedback on your code?", "Communication"),
            ("Describe a time you learned a new technology quickly.", "Learning"),
            ("How do you prioritize bugs and feature requests?", "Prioritization"),
            ("Tell me about a disagreement with a teammate.", "Teamwork"),
            ("Why are you interested in this software role?", "Motivation"),
            ("Describe a project failure and what you learned.", "Learning"),
            ("What would you improve in one of your projects?", "Reflection"),
        ],
        "Data / Analytics": [
            ("Explain a data project and the decision it supported.", "Project"),
            ("How would you handle missing values in a dataset?", "Technical reasoning"),
            ("Describe a time data changed your initial opinion.", "Evidence"),
            ("How would you explain a technical finding to a nontechnical person?", "Communication"),
            ("Tell me about a difficult analytical problem.", "Problem solving"),
            ("How do you validate your results?", "Quality"),
            ("Describe a time you worked with conflicting requirements.", "Teamwork"),
            ("Why are you interested in analytics?", "Motivation"),
            ("How do you avoid misleading visualizations?", "Ethics"),
            ("What skill are you currently developing?", "Learning"),
        ],
        "Business / Management": [
            ("Tell me about a time you influenced a group.", "Leadership"),
            ("How do you prioritize competing business needs?", "Prioritization"),
            ("Describe a conflict you helped resolve.", "Conflict"),
            ("Tell me about a decision you made with limited information.", "Decision making"),
            ("How would you handle an unhappy customer?", "Customer focus"),
            ("Describe a project you organized.", "Planning"),
            ("How do you measure whether a project succeeded?", "Results"),
            ("Why are you interested in this role?", "Motivation"),
            ("Tell me about a time you adapted to change.", "Adaptability"),
            ("Describe a time you took initiative.", "Leadership"),
        ],
    },
    "Technical": {
        "General / Student": [
            ("Explain a technical concept you know well.", "Technical explanation"),
            ("Describe a project you built and how it works.", "Project"),
            ("How do you debug a problem you cannot reproduce easily?", "Debugging"),
            ("How do you test whether a solution works correctly?", "Testing"),
            ("Explain a technical trade-off you have made.", "Trade-offs"),
            ("How do you learn an unfamiliar tool or framework?", "Learning"),
            ("Describe a difficult bug and how you solved it.", "Debugging"),
            ("How would you improve the performance of a slow program?", "Performance"),
            ("How do you keep your code maintainable?", "Code quality"),
            ("What would you change if you rebuilt your last project?", "Reflection"),
        ],
        "Software / IT": [
            ("Explain the difference between a list and a dictionary in Python.", "Programming"),
            ("How would you investigate a slow API endpoint?", "Performance"),
            ("What is the purpose of unit testing?", "Testing"),
            ("Explain how you would design a simple login flow.", "Design"),
            ("How do you manage errors and exceptions?", "Reliability"),
            ("What is the difference between SQL joins and filtering?", "Databases"),
            ("How would you troubleshoot a production bug?", "Debugging"),
            ("What makes an API easy to maintain?", "API design"),
            ("Explain one data structure and when you would use it.", "Data structures"),
            ("How do you protect sensitive information in an application?", "Security"),
        ],
        "Data / Analytics": [
            ("Explain the difference between supervised and unsupervised learning.", "Machine learning"),
            ("How would you detect outliers in a dataset?", "Statistics"),
            ("What is data leakage and why is it dangerous?", "Machine learning"),
            ("How do you choose an appropriate chart?", "Visualization"),
            ("How would you evaluate a classification model?", "Evaluation"),
            ("Explain correlation versus causation.", "Statistics"),
            ("How would you handle an imbalanced dataset?", "Data preparation"),
            ("Why should training and test data be separated?", "Validation"),
            ("How would you check data quality?", "Data preparation"),
            ("How would you explain a model's limitations?", "Communication"),
        ],
        "Business / Management": [
            ("How would you define measurable project requirements?", "Requirements"),
            ("How would you use data to prioritize a feature?", "Analytics"),
            ("Explain how you would map a business process.", "Process"),
            ("How would you investigate a drop in customer retention?", "Analysis"),
            ("How do you distinguish urgent work from important work?", "Prioritization"),
            ("How would you define success metrics for a new product?", "Metrics"),
            ("How would you communicate project risks?", "Risk"),
            ("How would you handle changing requirements?", "Planning"),
            ("Describe a useful process improvement.", "Improvement"),
            ("How would you evaluate a proposed business solution?", "Evaluation"),
        ],
    },
    "Situational": {
        "General / Student": [
            ("You have two deadlines on the same day. What do you do?", "Prioritization"),
            ("A teammate is not completing their work. How do you respond?", "Teamwork"),
            ("You receive criticism you disagree with. How do you handle it?", "Communication"),
            ("You do not understand a task. What is your next step?", "Initiative"),
            ("A plan fails just before a deadline. What do you do?", "Adaptability"),
            ("You notice an error in work already submitted. What do you do?", "Accountability"),
            ("You need to present on an unfamiliar topic. How do you prepare?", "Learning"),
            ("Two team members strongly disagree. How would you help?", "Conflict"),
            ("You are given several tasks without clear priorities. What do you ask?", "Planning"),
            ("You made a promise you may not meet. What do you do?", "Accountability"),
        ],
        "Software / IT": [
            ("A critical bug appears shortly before a release. What do you do?", "Incident response"),
            ("A stakeholder requests an unsafe shortcut. How do you respond?", "Security"),
            ("A code review blocks your change. What is your approach?", "Teamwork"),
            ("A feature is behind schedule. How do you communicate it?", "Planning"),
            ("An API fails intermittently. What do you investigate first?", "Debugging"),
            ("You discover a possible security issue. What do you do?", "Security"),
            ("A requirement conflicts with the current design. How do you proceed?", "Design"),
            ("A teammate proposes a solution you think will not scale. What do you do?", "Communication"),
            ("A deployment causes errors. What are your first actions?", "Reliability"),
            ("You inherit undocumented code. How do you begin?", "Learning"),
        ],
        "Data / Analytics": [
            ("A stakeholder asks for a conclusion the data does not support. What do you do?", "Ethics"),
            ("Two dashboards report different numbers. How do you investigate?", "Data quality"),
            ("A dataset contains sensitive personal information. What do you do?", "Privacy"),
            ("Your model performs poorly on a new group. What do you investigate?", "Fairness"),
            ("A deadline is near but data quality is poor. How do you respond?", "Quality"),
            ("A manager misinterprets a chart. How do you clarify it?", "Communication"),
            ("A key metric suddenly changes. How do you investigate?", "Analysis"),
            ("You cannot reproduce a previous result. What do you do?", "Validation"),
            ("A stakeholder requests a misleading visualization. How do you respond?", "Ethics"),
            ("You need to explain uncertainty in a forecast. How do you do it?", "Communication"),
        ],
        "Business / Management": [
            ("A client changes the scope near the deadline. What do you do?", "Scope"),
            ("Your team is over budget. How do you respond?", "Planning"),
            ("Two stakeholders demand different priorities. What do you do?", "Communication"),
            ("A customer complains publicly. How do you respond?", "Customer focus"),
            ("A project milestone is missed. What are your next steps?", "Accountability"),
            ("A teammate resists a new process. How do you approach them?", "Change management"),
            ("You have limited resources for a high-impact task. How do you prioritize?", "Prioritization"),
            ("A proposal has risks that are being ignored. What do you do?", "Risk"),
            ("A meeting is not producing decisions. How would you improve it?", "Leadership"),
            ("A project succeeds but its metrics are unclear. What do you do?", "Measurement"),
        ],
    },
}


# ------------------ SESSION STATE ------------------

DEFAULTS = {
    "navigation": "Setup",
    "candidate_name": "",
    "target_role": "General / Student",
    "experience_level": "Student / Fresher",
    "interview_type": "HR / Behavioral",
    "question_count": 5,
    "interview_questions": [],
    "answers": {},
    "audio_answers": {},
    "current_question": 0,
    "interview_active": False,
    "completed": False,
    "history": [],
    "last_result": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------ SCORING ENGINE ------------------

def analyze_answer(question, answer):
    """Transparent practice rubric; not a hiring decision."""
    text = (answer or "").strip()
    words = text.split()
    word_count = len(words)
    lower = text.lower()

    # 30 points: answer development
    length_score = min(30, round(word_count / 90 * 30))
    if word_count < 12:
        length_score = min(length_score, 8)

    # 25 points: relevance, estimated using question-topic words
    stop_words = {
        "what", "when", "where", "which", "would", "could", "should",
        "about", "your", "tell", "explain", "describe", "have", "with",
        "from", "that", "this", "they", "them", "then", "than", "into",
        "does", "do", "you", "how", "and", "the", "for", "are", "was",
        "were", "why", "one", "time", "work", "handle", "would",
    }
    q_terms = {
        word.strip(".,?!:;()").lower()
        for word in question.split()
        if len(word.strip(".,?!:;()")) >= 4
        and word.strip(".,?!:;()").lower() not in stop_words
    }
    a_terms = {
        word.strip(".,?!:;()").lower()
        for word in words
        if len(word.strip(".,?!:;()")) >= 4
    }
    overlap = len(q_terms & a_terms) / max(1, len(q_terms))
    relevance_score = min(25, round(8 + overlap * 40)) if word_count >= 8 else 5

    # 20 points: structure
    structure_cues = [
        "first", "then", "because", "therefore", "finally",
        "result", "learned", "situation", "task", "action",
        "outcome", "as a result", "for example",
    ]
    structure_count = sum(1 for cue in structure_cues if cue in lower)
    structure_score = min(20, 6 + structure_count * 3)
    if word_count < 18:
        structure_score = min(structure_score, 9)

    # 25 points: evidence, action and specificity
    evidence_cues = [
        "i built", "i led", "i created", "i improved", "i solved",
        "i tested", "i analyzed", "i organised", "i organized",
        "i designed", "i measured", "percent", "%", "increased",
        "reduced", "delivered", "completed", "deadline", "customer",
        "team", "project", "using", "result was", "for example",
    ]
    evidence_count = sum(1 for cue in evidence_cues if cue in lower)
    specificity_score = min(25, 5 + evidence_count * 4)
    if word_count < 18:
        specificity_score = min(specificity_score, 9)

    total = min(100, length_score + relevance_score + structure_score + specificity_score)

    strengths = []
    improvements = []

    if word_count >= 45:
        strengths.append("You developed your answer beyond a one-line response.")
    else:
        improvements.append("Add more detail: explain the context, your actions and the outcome.")

    if structure_count >= 2:
        strengths.append("You used some sequencing or explanation cues.")
    else:
        improvements.append("Make the answer easier to follow with a clear beginning, middle and result.")

    if evidence_count >= 2:
        strengths.append("You included examples or action-oriented details.")
    else:
        improvements.append("Include one concrete example, your individual contribution and a measurable result if available.")

    if any(word in lower for word in ["i", "my", "we"]):
        strengths.append("You described your own perspective or involvement.")
    else:
        improvements.append("Explain what you personally did rather than only describing the situation generally.")

    if word_count > 180:
        improvements.append("Try to be more concise and avoid repeating the same point.")

    if not strengths:
        strengths.append("You have a starting point to build on. Keep practising.")
    if not improvements:
        improvements.append("Add one more specific example to make the answer even stronger.")

    return {
        "score": total,
        "word_count": word_count,
        "development": length_score,
        "relevance": relevance_score,
        "structure": structure_score,
        "specificity": specificity_score,
        "strengths": strengths,
        "improvements": improvements,
        "feedback": (
            "Strong practice answer. Keep the specific evidence and make sure "
            "your conclusion directly answers the question."
            if total >= 75 else
            "Develop the answer with a clearer structure, a specific example "
            "and an outcome. Use the suggestions below as your revision plan."
        ),
    }


# ------------------ AUDIO ANALYSIS ------------------

def inspect_audio(audio_bytes, transcript=""):
    """Read common WAV recordings and calculate basic signal indicators."""
    if not audio_bytes:
        return None

    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav:
            frame_rate = wav.getframerate()
            frames = wav.readframes(wav.getnframes())
            sample_width = wav.getsampwidth()
            channels = wav.getnchannels()
            duration = len(frames) / max(1, frame_rate * sample_width * channels)

        if duration <= 0 or sample_width not in (1, 2, 4):
            return {"duration": duration, "volume_db": None, "peak_pct": None, "wpm": None}

        if sample_width == 1:
            values = [b - 128 for b in frames]
            max_amp = 127
        elif sample_width == 2:
            count = len(frames) // 2
            values = [v[0] for v in struct.iter_unpack("<h", frames[:count * 2])]
            max_amp = 32767
        else:
            count = len(frames) // 4
            values = [v[0] for v in struct.iter_unpack("<i", frames[:count * 4])]
            max_amp = 2147483647

        if not values:
            return {"duration": duration, "volume_db": None, "peak_pct": None, "wpm": None}

        rms = math.sqrt(sum(float(x) * float(x) for x in values) / len(values))
        peak = max(abs(x) for x in values)
        volume_db = 20 * math.log10(max(rms, 1) / max_amp)
        peak_pct = peak / max_amp * 100
        word_count = len((transcript or "").split())
        wpm = round(word_count / duration * 60) if duration > 0 and word_count else None

        return {
            "duration": round(duration, 1),
            "volume_db": round(volume_db, 1),
            "peak_pct": round(peak_pct, 1),
            "wpm": wpm,
        }

    except Exception:
        return None


def voice_tips(metrics):
    if not metrics:
        return ["Record a short answer to review basic audio characteristics."]

    tips = []
    volume = metrics.get("volume_db")
    peak = metrics.get("peak_pct")
    wpm = metrics.get("wpm")

    if volume is not None and volume < -32:
        tips.append("The recording level is quiet. Move closer to the microphone and speak clearly.")
    elif volume is not None and volume > -5:
        tips.append("The recording level is very strong. Move slightly away from the microphone to reduce distortion.")
    else:
        tips.append("The recording level appears usable. Listen back to confirm that your voice is clear.")

    if peak is not None and peak > 98:
        tips.append("Some audio peaks are near clipping. Reduce microphone gain or move farther from the microphone.")

    if wpm is not None and wpm < 100:
        tips.append("Your estimated speaking pace is slow. Try shorter pauses while keeping your words clear.")
    elif wpm is not None and wpm > 170:
        tips.append("Your estimated speaking pace is fast. Pause briefly between key points.")
    elif wpm is not None:
        tips.append("Your estimated speaking pace is within a practical interview-practice range.")

    tips.append("This tool does not identify emotion or vocal tone. Listen for a calm pace, clear pronunciation and confident emphasis.")
    return tips


# ------------------ HELPERS ------------------

def save_current_answer(index):
    answer_key = f"answer_text_{index}"
    audio_key = f"audio_recording_{index}"

    st.session_state.answers[str(index)] = st.session_state.get(answer_key, "").strip()

    recording = st.session_state.get(audio_key)
    if recording is not None:
        try:
            st.session_state.audio_answers[str(index)] = recording.getvalue()
        except Exception:
            pass


def calculate_results():
    results = []
    for index, item in enumerate(st.session_state.interview_questions):
        question, topic = item
        answer = st.session_state.answers.get(str(index), "")
        result = analyze_answer(question, answer)
        metrics = inspect_audio(
            st.session_state.audio_answers.get(str(index)),
            answer,
        )
        results.append({
            "question_number": index + 1,
            "topic": topic,
            "question": question,
            "answer": answer,
            **result,
            "audio_metrics": metrics,
            "voice_tips": voice_tips(metrics),
        })

    return results


def finish_interview():
    results = calculate_results()
    answered = sum(1 for item in results if item["answer"].strip())
    if answered == 0:
        return False, "Answer at least one question before finishing."

    average = round(sum(item["score"] for item in results) / len(results))
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "candidate": st.session_state.candidate_name or "Candidate",
        "role": st.session_state.target_role,
        "experience": st.session_state.experience_level,
        "interview_type": st.session_state.interview_type,
        "question_count": len(results),
        "answered_count": answered,
        "score": average,
        "results": results,
    }

    st.session_state.history.append(record)
    st.session_state.last_result = record
    st.session_state.completed = True
    st.session_state.interview_active = False
    return True, "Interview scored successfully."


# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.markdown("## 🎯 InterviewReady")
    st.caption("AI Interview Coach · Free MVP")
    st.divider()

    st.markdown("### YOUR WORKSPACE")
    st.radio(
        "Navigate",
        ["Setup", "Mock Interview", "Results Dashboard"],
        key="navigation",
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### PRACTICE TIP")
    st.write(
        "For behavioral questions, use STAR: "
        "**Situation, Task, Action, Result.**"
    )
    st.divider()
    st.caption("Free demo mode · No paid API key required")
    st.caption("Avoid entering confidential personal information.")


# ------------------ HERO ------------------

st.markdown(
    """
    <div class="hero">
        <p class="eyebrow" style="color:#dce8ff !important;">PRACTISE • REFLECT • IMPROVE</p>
        <h1>Interview practice, with purpose.</h1>
        <p>Build stronger answers, record your voice, and understand where to improve.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE 1: SETUP
# =========================================================

if st.session_state.navigation == "Setup":
    left, right = st.columns([1.55, 1], gap="large")

    with left:
        st.subheader("Set up your mock interview")
        st.write("Choose a role and interview style. Your questions will be tailored to your selection.")

        with st.form("setup_form", clear_on_submit=False):
            name = st.text_input(
                "Your name",
                value=st.session_state.candidate_name,
                placeholder="Enter your name",
            )

            role = st.selectbox(
                "Target role",
                list(QUESTION_BANK["HR / Behavioral"].keys()),
                index=list(QUESTION_BANK["HR / Behavioral"].keys()).index(
                    st.session_state.target_role
                ),
            )

            experience = st.selectbox(
                "Experience level",
                ["Student / Fresher", "Entry level", "1–3 years", "3+ years"],
                index=["Student / Fresher", "Entry level", "1–3 years", "3+ years"].index(
                    st.session_state.experience_level
                ),
            )

            interview_type = st.selectbox(
                "Interview type",
                list(QUESTION_BANK.keys()),
                index=list(QUESTION_BANK.keys()).index(st.session_state.interview_type),
            )

            count = st.slider(
                "Number of questions",
                min_value=3,
                max_value=10,
                value=st.session_state.question_count,
            )

            submitted = st.form_submit_button(
                "Start a new mock interview",
                use_container_width=True,
            )

        if submitted:
            bank = QUESTION_BANK[interview_type][role]
            questions = bank[:]
            # Rotate the bank for a little variety across sessions.
            if st.session_state.history:
                shift = len(st.session_state.history) % len(questions)
                questions = questions[shift:] + questions[:shift]

            st.session_state.candidate_name = name.strip() or "Candidate"
            st.session_state.target_role = role
            st.session_state.experience_level = experience
            st.session_state.interview_type = interview_type
            st.session_state.question_count = count
            st.session_state.interview_questions = questions[:count]
            st.session_state.answers = {}
            st.session_state.audio_answers = {}
            st.session_state.current_question = 0
            st.session_state.interview_active = True
            st.session_state.completed = False
            st.session_state.last_result = None
            st.success("Interview created! Select **Mock Interview** in the left sidebar to begin.")

    with right:
        st.subheader("Your practice toolkit")
        st.markdown(
            """
            <div class="panel">
                <h3>🧭 Guided mock interviews</h3>
                <p>Answer one tailored question at a time with a clear progress indicator.</p>
                <hr>
                <h3>🎙️ Voice recording</h3>
                <p>Record an answer, replay it, and review basic recording-level indicators.</p>
                <hr>
                <h3>📊 Transparent scoring</h3>
                <p>Review development, relevance, structure and specificity.</p>
                <hr>
                <h3>🚀 Actionable feedback</h3>
                <p>Get practical suggestions for improving your next answer.</p>
            </div>
            <div class="notice">
                <b>Free MVP:</b> Scoring uses a transparent practice rubric,
                not a hiring decision or a live generative-AI model.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.history:
            latest = st.session_state.history[-1]
            st.metric("Previous practice score", f'{latest["score"]}/100')


# =========================================================
# PAGE 2: MOCK INTERVIEW
# =========================================================

elif st.session_state.navigation == "Mock Interview":
    if not st.session_state.interview_active or not st.session_state.interview_questions:
        st.info("No active interview yet. Go to **Setup** and create a mock interview first.")
        if st.session_state.last_result:
            st.write("You can review your most recent completed interview in the Results Dashboard.")
    else:
        questions = st.session_state.interview_questions
        index = min(st.session_state.current_question, len(questions) - 1)
        question, topic = questions[index]

        st.subheader(f"Hello, {st.session_state.candidate_name} 👋")
        st.write(
            f'{st.session_state.target_role} · {st.session_state.interview_type} · '
            f'{st.session_state.experience_level}'
        )

        st.progress((index + 1) / len(questions))
        st.caption(f"QUESTION {index + 1} OF {len(questions)}")

        st.markdown(
            f"""
            <div class="panel">
                <p class="eyebrow">{topic}</p>
                <h2 style="color:#14213d !important;">{question}</h2>
                <p>Take a moment to organise your thoughts. Aim for a specific example and a clear outcome.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Need a structure? Use this answer guide", expanded=False):
            st.markdown(
                """
                - **Context:** What was happening?
                - **Your responsibility:** What needed to be done?
                - **Your action:** What did you personally do?
                - **Result:** What changed, and what did you learn?
                """
            )

        st.markdown("### Your answer")
        answer_key = f"answer_text_{index}"

        st.text_area(
            "Type your answer or enter a transcript of your spoken answer",
            key=answer_key,
            height=190,
            placeholder="Describe your approach, actions, examples and results...",
        )

        st.caption(
            "Voice option: record your spoken answer below. This MVP does not "
            "automatically transcribe speech, so enter the transcript above for text feedback."
        )

        recording = st.audio_input(
            "Record your spoken answer (optional)",
            key=f"audio_recording_{index}",
        )

        if recording is not None:
            st.audio(recording)
            st.caption("Listen back before saving your answer.")

        saved_audio = st.session_state.audio_answers.get(str(index))
        if saved_audio and recording is None:
            st.audio(saved_audio)

        nav1, nav2, nav3 = st.columns([1, 1, 1.25])

        with nav1:
            if st.button("← Previous", disabled=index == 0, use_container_width=True):
                save_current_answer(index)
                st.session_state.current_question = index - 1
                st.rerun()

        with nav2:
            if st.button("Save answer", use_container_width=True):
                save_current_answer(index)
                st.success("Answer saved.")

        with nav3:
            if index < len(questions) - 1:
                if st.button("Save & next →", type="primary", use_container_width=True):
                    save_current_answer(index)
                    st.session_state.current_question = index + 1
                    st.rerun()
            else:
                if st.button("Finish & score interview", type="primary", use_container_width=True):
                    save_current_answer(index)
                    ok, message = finish_interview()
                    if ok:
                        st.success(message)
                        st.info("Open **Results Dashboard** in the sidebar to view your feedback.")
                    else:
                        st.warning(message)

        answered_count = sum(
            1 for i in range(len(questions))
            if st.session_state.answers.get(str(i), "").strip()
        )
        st.caption(f"Saved answers: {answered_count} of {len(questions)}")


# =========================================================
# PAGE 3: RESULTS DASHBOARD
# =========================================================

elif st.session_state.navigation == "Results Dashboard":
    st.subheader("Your results dashboard")
    st.write("Review completed practice sessions, strengths and improvement areas.")

    history = st.session_state.history

    if not history:
        st.info("Your dashboard will appear here after you finish your first mock interview.")
        st.markdown(
            """
            <div class="panel">
                <h3>What your dashboard will show</h3>
                <p>Overall score · Skill breakdown · Question feedback · Voice recording indicators · CSV export</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        latest = history[-1]
        latest_results = latest["results"]

        scores = [item["score"] for item in latest_results]
        avg_score = round(sum(scores) / len(scores)) if scores else 0
        answered = latest["answered_count"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Latest score", f"{avg_score}/100")
        m2.metric("Questions answered", f"{answered}/{latest['question_count']}")
        m3.metric("Practice sessions", len(history))
        m4.metric("Latest date", latest["date"].split(" ")[0])

        st.markdown("### Latest session overview")
        st.markdown(
            f"""
            <div class="panel">
                <p class="eyebrow">CANDIDATE PROFILE</p>
                <h3>{latest["candidate"]}</h3>
                <p>{latest["role"]} · {latest["experience"]} · {latest["interview_type"]}</p>
                <p>{latest["date"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        skill_names = ["development", "relevance", "structure", "specificity"]
        skill_max = {"development": 30, "relevance": 25, "structure": 20, "specificity": 25}
        skill_rows = []
        for skill in skill_names:
            raw = sum(item[skill] for item in latest_results)
            maximum = skill_max[skill] * len(latest_results)
            skill_rows.append({
                "Skill": skill.title(),
                "Average points": round(raw / max(1, len(latest_results)), 1),
                "Maximum points": skill_max[skill],
                "Percentage": round(raw / max(1, maximum) * 100),
            })

        skill_df = pd.DataFrame(skill_rows)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("### Score by question")
            chart_df = pd.DataFrame([
                {
                    "Question": f'Q{item["question_number"]}',
                    "Score": item["score"],
                }
                for item in latest_results
            ])
            # No y_min/y_max arguments: works with standard Streamlit st.bar_chart.
            st.bar_chart(chart_df.set_index("Question"))

        with c2:
            st.markdown("### Skill breakdown")
            st.dataframe(
                skill_df[["Skill", "Average points", "Maximum points", "Percentage"]],
                hide_index=True,
                use_container_width=True,
            )

        st.markdown("### Question-by-question coaching")
        for item in latest_results:
            title = f'Q{item["question_number"]} · {item["topic"]} · {item["score"]}/100'
            with st.expander(title):
                st.markdown(f'**Question:** {item["question"]}')
                st.markdown("**Your answer:**")
                st.write(item["answer"] if item["answer"] else "_No answer was saved._")

                a, b, c, d = st.columns(4)
                a.metric("Development", f'{item["development"]}/30')
                b.metric("Relevance", f'{item["relevance"]}/25')
                c.metric("Structure", f'{item["structure"]}/20')
                d.metric("Specificity", f'{item["specificity"]}/25')

                st.markdown("**Feedback**")
                st.write(item["feedback"])

                st.markdown("**What worked**")
                for tip in item["strengths"]:
                    st.write(f"✓ {tip}")

                st.markdown("**How to improve**")
                for tip in item["improvements"]:
                    st.write(f"→ {tip}")

                if item["audio_metrics"]:
                    metrics = item["audio_metrics"]
                    st.markdown("**Recording review**")
                    x, y, z = st.columns(3)
                    x.metric("Duration", f'{metrics.get("duration", 0)} sec')
                    y.metric(
                        "Recording level",
                        f'{metrics["volume_db"]} dBFS'
                        if metrics.get("volume_db") is not None else "N/A",
                    )
                    z.metric(
                        "Estimated pace",
                        f'{metrics["wpm"]} words/min'
                        if metrics.get("wpm") is not None else "N/A",
                    )
                    st.caption(
                        "Speaking pace is estimated from the manually entered transcript "
                        "and recording duration. It is approximate, not speech recognition."
                    )
                    for tip in item["voice_tips"]:
                        st.write(f"🎙️ {tip}")

                    with st.expander("Replay recording"):
                        audio_bytes = st.session_state.audio_answers.get(
                            str(item["question_number"] - 1)
                        )
                        if audio_bytes:
                            st.audio(audio_bytes)
                        else:
                            st.caption("Recording is not available in the current session.")

        st.markdown("### Progress across sessions")
        trend_df = pd.DataFrame([
            {
                "Session": f'Session {i + 1}',
                "Score": record["score"],
            }
            for i, record in enumerate(history)
        ])
        st.line_chart(trend_df.set_index("Session"))

        st.markdown("### Export your results")
        export_rows = []
        for session_no, record in enumerate(history, start=1):
            for item in record["results"]:
                export_rows.append({
                    "Session": session_no,
                    "Date": record["date"],
                    "Candidate": record["candidate"],
                    "Role": record["role"],
                    "Experience": record["experience"],
                    "Interview type": record["interview_type"],
                    "Question number": item["question_number"],
                    "Topic": item["topic"],
                    "Question": item["question"],
                    "Answer": item["answer"],
                    "Score": item["score"],
                    "Development / 30": item["development"],
                    "Relevance / 25": item["relevance"],
                    "Structure / 20": item["structure"],
                    "Specificity / 25": item["specificity"],
                    "Feedback": item["feedback"],
                    "Improvements": " | ".join(item["improvements"]),
                })

        export_df = pd.DataFrame(export_rows)
        st.download_button(
            "⬇ Download all session results (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="interviewready_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown(
            """
            <div class="notice">
                <b>Interpret scores thoughtfully.</b> The rubric is a practice aid,
                not an objective measure of ability or a hiring decision.
                Session history is stored in memory and may reset after a restart or redeployment.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------ FOOTER ------------------

st.divider()
st.caption(
    "InterviewReady MVP · Free practice mode · Rule-based feedback · "
    "Do not enter confidential personal information."
)

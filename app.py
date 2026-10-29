
import streamlit as st
import pandas as pd
import re
import io
import wave
import struct
from datetime import datetime

# =========================================================
# INTERVIEWREADY — AI INTERVIEW COACH MVP
# Free demo: no paid API key required
# =========================================================

st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------- STYLING --------------------------

st.markdown("""
<style>
    :root {
        --navy: #14213d;
        --blue: #3159a8;
        --light-blue: #eaf1ff;
        --coral: #ff5757;
        --ink: #17243b;
        --muted: #52627a;
        --border: #d7e0ed;
        --surface: #ffffff;
    }

    .stApp {
        background: #f4f7fc;
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #14213d;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent;
        padding: 5px 8px;
        border-radius: 6px;
    }

    h1, h2, h3, h4 {
        color: #14213d !important;
        font-weight: 750 !important;
    }

    p, label, li, span {
        color: inherit;
    }

    [data-testid="stWidgetLabel"] p {
        color: #243650 !important;
        font-weight: 600;
    }

    input, textarea {
        color: #17243b !important;
        background: #ffffff !important;
        -webkit-text-fill-color: #17243b !important;
    }

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #17243b !important;
        border-color: #aebdd1 !important;
    }

    div[data-baseweb="select"] * {
        color: #17243b !important;
    }

    [data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: #17243b !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #26364d;
    }

    .hero {
        background: linear-gradient(120deg, #14213d, #3159a8);
        padding: 30px 32px;
        border-radius: 18px;
        margin-bottom: 24px;
        color: white;
    }

    .hero h1 {
        color: white !important;
        font-size: 2.2rem;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #edf3ff !important;
        margin: 0;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d7e0ed;
        border-radius: 14px;
        padding: 18px;
        min-height: 110px;
        box-shadow: 0 3px 12px rgba(20, 33, 61, 0.04);
    }

    .metric-label {
        font-size: 0.88rem;
        color: #52627a !important;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #14213d !important;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #d7e0ed;
        border-radius: 14px;
        padding: 22px;
        margin: 12px 0;
    }

    .question-tag {
        display: inline-block;
        background: #eaf1ff;
        color: #244b98 !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .tip {
        background: #eaf1ff;
        border-left: 4px solid #3159a8;
        border-radius: 8px;
        padding: 14px;
        color: #243650 !important;
        margin: 10px 0;
    }

    .warning-box {
        background: #fff4df;
        border-left: 4px solid #e6a23c;
        border-radius: 8px;
        padding: 13px;
        color: #634514 !important;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 43px;
        font-weight: 650;
        border: 1px solid #cbd6e5;
    }

    div.stButton > button[kind="primary"] {
        background: #ff5757;
        color: white;
        border: 0;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #e84444;
        color: white;
    }

    [data-testid="stProgress"] > div > div {
        background: #3159a8;
    }

    hr {
        border-color: #d7e0ed;
    }

    .footer {
        color: #61718a !important;
        font-size: 0.8rem;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ------------------- QUESTION BANK ------------------------

QUESTION_BANK = {
    "HR / Behavioral": [
        "Tell me about yourself and what makes you suitable for this role.",
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
        "How would you approach a task when the success criteria are unclear?",
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


# ------------------- SESSION STATE ------------------------

DEFAULTS = {
    "navigation": "Setup",
    "answers": {},
    "audio_answers": {},
    "current_question": 0,
    "interview_active": False,
    "completed": False,
    "last_result": None,
    "history": [],
    "interview_questions": [],
    "setup_name": "",
    "setup_role": "General / Student",
    "setup_experience": "Student / Fresher",
    "setup_type": "HR / Behavioral",
    "setup_count": 5,
    "interview_started_at": None,
    "interview_id": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------ SCORING FUNCTIONS ---------------------

def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def score_answer(question, answer):
    """Transparent practice rubric; this is not an AI model."""

    answer = (answer or "").strip()
    words = word_count(answer)
    lower = answer.lower()

    # Answer development: 0-30
    if words < 10:
        development = 5
    elif words < 25:
        development = 13
    elif words < 50:
        development = 21
    elif words <= 180:
        development = 30
    else:
        development = 26

    # Structure: 0-25
    structure_markers = [
        "first", "because", "therefore", "result", "finally",
        "for example", "as a result", "learned", "improved",
        "situation", "task", "action",
    ]
    markers_found = sum(marker in lower for marker in structure_markers)
    has_sequence = any(
        word in lower
        for word in ["first", "then", "next", "finally", "after that"]
    )
    structure = min(
        25,
        7 + markers_found * 3 + (5 if has_sequence else 0)
    ) if words >= 10 else 4

    # Specificity: 0-25
    specificity_terms = [
        "project", "team", "customer", "deadline", "data",
        "developed", "created", "analysed", "analyzed",
        "tested", "measured", "implemented", "achieved",
        "improved", "reduced", "increased", "learned",
        "example", "outcome", "result",
    ]
    specific_hits = sum(term in lower for term in specificity_terms)
    specificity = min(25, 5 + specific_hits * 4) if words >= 10 else 3

    # Relevance: lightweight heuristic, not semantic AI
    question_terms = set(
        re.findall(r"\b[a-z]{4,}\b", question.lower())
    )
    stop_words = {
        "tell", "about", "what", "when", "where", "which",
        "would", "could", "should", "have", "your", "with",
        "that", "this", "from", "into", "describe", "explain",
        "time", "how", "role", "work", "they", "them",
    }
    question_terms -= stop_words
    answer_terms = set(re.findall(r"\b[a-z]{4,}\b", lower))
    overlap = len(question_terms & answer_terms)
    relevance = min(20, 8 + overlap * 4) if words >= 10 else 3

    total = min(100, development + structure + specificity + relevance)

    feedback = []

    if words < 25:
        feedback.append(
            "Develop your answer with more context, actions, and outcomes."
        )
    elif words > 180:
        feedback.append(
            "Shorten your response and prioritise the most important points."
        )
    else:
        feedback.append(
            "Your answer has a reasonable amount of detail."
        )

    if structure < 17:
        feedback.append(
            "Improve structure: explain the situation, your task, your action, and the result (STAR)."
        )
    else:
        feedback.append(
            "Your answer includes some useful structural cues. Make the sequence even clearer."
        )

    if specificity < 17:
        feedback.append(
            "Add a concrete example, your personal contribution, or a measurable outcome."
        )
    else:
        feedback.append(
            "Add or retain specific details so the interviewer can understand your contribution."
        )

    if relevance < 12:
        feedback.append(
            "Answer the exact question more directly before adding background information."
        )

    if not answer:
        feedback = [
            "Write or record your answer before moving to the next question."
        ]
        total = 0

    return {
        "score": total,
        "development": development,
        "structure": structure,
        "specificity": specificity,
        "relevance": relevance,
        "words": words,
        "feedback": feedback,
    }


def build_result():
    questions = st.session_state.interview_questions
    answers = st.session_state.answers

    details = []

    for index, question in enumerate(questions):
        answer = answers.get(index, "")
        result = score_answer(question, answer)

        details.append({
            "question_number": index + 1,
            "question": question,
            "answer": answer,
            **result,
        })

    average = round(
        sum(item["score"] for item in details) / len(details)
    ) if details else 0

    result = {
        "interview_id": st.session_state.interview_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": st.session_state.setup_name or "Candidate",
        "role": st.session_state.setup_role,
        "experience": st.session_state.setup_experience,
        "interview_type": st.session_state.setup_type,
        "questions_count": len(questions),
        "overall_score": average,
        "details": details,
    }

    return result


def start_interview():
    """Button callback: update navigation before the next script run."""

    name = st.session_state.get("setup_name", "").strip()

    if not name:
        st.session_state["start_error"] = "Please enter your name first."
        return

    st.session_state["start_error"] = ""
    st.session_state.interview_id += 1
    st.session_state.answers = {}
    st.session_state.audio_answers = {}
    st.session_state.current_question = 0
    st.session_state.interview_active = True
    st.session_state.completed = False
    st.session_state.last_result = None
    st.session_state.interview_started_at = datetime.now().isoformat()

    role = st.session_state.setup_role
    interview_type = st.session_state.setup_type
    count = int(st.session_state.setup_count)

    questions = list(QUESTION_BANK[interview_type])

    if role in ROLE_QUESTIONS:
        questions.extend(ROLE_QUESTIONS[role])

    # Rotate questions on subsequent interviews.
    offset = (st.session_state.interview_id - 1) % len(questions)
    questions = questions[offset:] + questions[:offset]

    st.session_state.interview_questions = questions[:count]
    st.session_state["navigation"] = "Mock Interview"


def go_to_results():
    st.session_state["navigation"] = "Results Dashboard"


def save_current_answer():
    index = st.session_state.current_question
    key = f"answer_input_{index}"
    answer = st.session_state.get(key, "")
    st.session_state.answers[index] = answer


def go_next():
    save_current_answer()
    last_index = len(st.session_state.interview_questions) - 1

    if st.session_state.current_question < last_index:
        st.session_state.current_question += 1


def go_previous():
    save_current_answer()

    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1


def finish_interview():
    save_current_answer()
    result = build_result()

    st.session_state.last_result = result
    st.session_state.completed = True
    st.session_state.interview_active = False
    st.session_state.history.append(result)
    st.session_state["navigation"] = "Results Dashboard"


# ----------------------- SIDEBAR --------------------------

with st.sidebar:
    st.markdown("# 🎯 InterviewReady")
    st.markdown("**AI Interview Coach · MVP**")
    st.caption("Practise. Improve. Get interview-ready.")

    st.divider()

    st.radio(
        "Navigate",
        ["Setup", "Mock Interview", "Results Dashboard"],
        key="navigation",
    )

    st.divider()

    st.markdown("### 💡 Practice tip")
    st.markdown(
        "For behavioral questions, try the STAR method: "
        "**Situation, Task, Action, Result.**"
    )

    st.divider()

    st.caption("Free demo mode · No API key required")
    st.caption("Scores are practice guidance, not hiring decisions.")


# ------------------------- HEADER -------------------------

st.markdown("""
<div class="hero">
    <h1>InterviewReady</h1>
    <p>Practise confidently. Structure stronger answers. Track your progress.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SETUP PAGE
# =========================================================

if st.session_state.navigation == "Setup":

    left, right = st.columns([1.6, 1], gap="large")

    with left:
        st.subheader("Set up your mock interview")
        st.write(
            "Choose your target role and interview style, then begin your practice session."
        )

        st.text_input(
            "Your name",
            key="setup_name",
            placeholder="Enter your name",
        )

        st.selectbox(
            "Target role",
            [
                "General / Student",
                "Software / IT",
                "Data Science / Analytics",
                "Business / Management",
                "Marketing / Sales",
            ],
            key="setup_role",
        )

        st.selectbox(
            "Experience level",
            [
                "Student / Fresher",
                "Entry level",
                "1–3 years",
                "3+ years",
            ],
            key="setup_experience",
        )

        st.selectbox(
            "Interview type",
            ["HR / Behavioral", "Technical", "Situational"],
            key="setup_type",
        )

        st.slider(
            "Number of questions",
            min_value=3,
            max_value=10,
            value=5,
            key="setup_count",
        )

        if st.session_state.get("start_error"):
            st.error(st.session_state["start_error"])

        st.button(
            "🚀 Start mock interview",
            type="primary",
            use_container_width=True,
            on_click=start_interview,
        )

    with right:
        st.subheader("Your practice, at a glance")

        st.markdown("""
        <div class="panel">
            <h3>🧭 Guided practice</h3>
            <p>Answer interview questions one at a time.</p>
            <hr>
            <h3>📊 Clear scoring</h3>
            <p>Review answer development, relevance, structure, and specificity.</p>
            <hr>
            <h3>🎙️ Voice practice</h3>
            <p>Record answers and replay your delivery for self-review.</p>
            <hr>
            <h3>🚀 Actionable feedback</h3>
            <p>Discover practical ways to strengthen your responses.</p>
        </div>
        <div class="tip">
            <b>Practice responsibly</b><br>
            This demo uses a transparent rule-based scoring rubric.
            It does not make hiring decisions or guarantee eligibility.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">InterviewReady MVP · Avoid entering confidential personal information.</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# MOCK INTERVIEW PAGE
# =========================================================

elif st.session_state.navigation == "Mock Interview":

    if not st.session_state.interview_active:
        if st.session_state.completed and st.session_state.last_result:
            st.success("Your interview is complete.")
            st.button(
                "View results dashboard",
                type="primary",
                on_click=go_to_results,
            )
        else:
            st.info(
                "No active interview yet. Open Setup and start a new interview."
            )
            if st.button("Go to Setup", type="primary"):
                st.session_state["navigation"] = "Setup"
                st.rerun()

    else:
        questions = st.session_state.interview_questions
        index = st.session_state.current_question
        total = len(questions)
        question = questions[index]

        st.subheader("Mock interview")
        st.write(
            f"Hello, **{st.session_state.setup_name}**. "
            f"Take your time and answer as you would in a real interview."
        )

        st.progress((index + 1) / total)
        st.caption(f"Question {index + 1} of {total}")

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            f'<span class="question-tag">{st.session_state.setup_type}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"### {question}")
        st.markdown(
            "Try to give a clear answer with an example and a specific outcome."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        answer_key = f"answer_input_{index}"

        if answer_key not in st.session_state:
            st.session_state[answer_key] = st.session_state.answers.get(index, "")

        st.text_area(
            "Your answer",
            key=answer_key,
            height=190,
            placeholder=(
                "Write your answer here. For behavioral questions, "
                "explain the situation, your action, and the result."
            ),
        )

        word_total = word_count(st.session_state.get(answer_key, ""))
        st.caption(f"Word count: {word_total}")

        st.markdown("#### 🎙️ Voice practice")
        st.write(
            "Record an answer below if your browser supports microphone access. "
            "Your recording is available for playback in this session."
        )

        try:
            audio = st.audio_input(
                "Record your answer",
                key=f"audio_input_{index}",
            )

            if audio is not None:
                audio_bytes = audio.getvalue()
                st.session_state.audio_answers[index] = audio_bytes
                st.audio(audio_bytes)

                st.caption(
                    "Recording captured. This MVP does not automatically "
                    "transcribe speech or detect emotion."
                )

        except Exception:
            st.info(
                "Audio recording is not available in this browser or "
                "Streamlit version. You can still type your answer."
            )

        # Show a live, provisional assessment of the typed answer.
        current_answer = st.session_state.get(answer_key, "").strip()

        if current_answer:
            provisional = score_answer(question, current_answer)
            st.markdown("#### Quick answer check")
            c1, c2, c3 = st.columns(3)

            c1.metric("Practice score", f"{provisional['score']}/100")
            c2.metric("Words", provisional["words"])
            c3.metric("Structure", f"{provisional['structure']}/25")

            with st.expander("See improvement suggestions"):
                for item in provisional["feedback"]:
                    st.write(f"• {item}")

        st.divider()

        previous_col, next_col, finish_col = st.columns([1, 1, 1.2])

        with previous_col:
            st.button(
                "← Previous",
                disabled=(index == 0),
                use_container_width=True,
                on_click=go_previous,
            )

        with next_col:
            if index < total - 1:
                st.button(
                    "Next question →",
                    type="primary",
                    use_container_width=True,
                    on_click=go_next,
                )

        with finish_col:
            st.button(
                "Finish interview",
                type="primary",
                use_container_width=True,
                on_click=finish_interview,
            )

        st.markdown(
            '<div class="footer">Your answers are stored in the current app session. '
            'Avoid entering confidential personal information.</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# RESULTS DASHBOARD
# =========================================================

elif st.session_state.navigation == "Results Dashboard":

    st.subheader("📊 Results dashboard")
    st.write("Review your latest practice session and monitor your progress.")

    result = st.session_state.last_result
    history = st.session_state.history

    if not result:
        st.info(
            "Your dashboard will show results after you complete an interview."
        )

        if st.button("Start your first interview", type="primary"):
            st.session_state["navigation"] = "Setup"
            st.rerun()

    else:
        st.markdown(
            f"### Results for {result['name']}"
        )
        st.caption(
            f"{result['role']} · {result['interview_type']} · {result['date']}"
        )

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Overall score</div>'
                f'<div class="metric-value">{result["overall_score"]}/100</div></div>',
                unsafe_allow_html=True,
            )

        with metric2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Questions</div>'
                f'<div class="metric-value">{result["questions_count"]}</div></div>',
                unsafe_allow_html=True,
            )

        with metric3:
            answered = sum(
                bool(item["answer"].strip())
                for item in result["details"]
            )
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Answered</div>'
                f'<div class="metric-value">{answered}/{result["questions_count"]}</div></div>',
                unsafe_allow_html=True,
            )

        with metric4:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Sessions</div>'
                f'<div class="metric-value">{len(history)}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### Performance breakdown")

        categories = [
            ("Answer development", "development", 30),
            ("Structure", "structure", 25),
            ("Specificity", "specificity", 25),
            ("Relevance", "relevance", 20),
        ]

        breakdown = []

        for label, key, maximum in categories:
            value = round(
                sum(item[key] for item in result["details"])
                / len(result["details"])
            ) if result["details"] else 0

            breakdown.append({
                "Skill": label,
                "Score": value,
                "Maximum": maximum,
            })

        chart_col, summary_col = st.columns([1.2, 1])

        with chart_col:
            chart_df = pd.DataFrame(breakdown).set_index("Skill")
            st.bar_chart(chart_df[["Score"]], height=300)

        with summary_col:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("#### Your coaching summary")

            if result["overall_score"] >= 80:
                st.success(
                    "Strong practice performance. Keep refining examples and clarity."
                )
            elif result["overall_score"] >= 60:
                st.info(
                    "A good foundation. Work on specific examples and answer structure."
                )
            else:
                st.warning(
                    "Focus on answering every question with more detail and a clear structure."
                )

            st.write(
                "Use these results to guide your next practice session. "
                "The score is based on writing patterns, not an AI judgement "
                "of your personality or professional ability."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### Question-by-question feedback")

        for item in result["details"]:
            with st.expander(
                f"Q{item['question_number']}: {item['question']} — {item['score']}/100"
            ):
                st.markdown("**Your answer**")

                if item["answer"].strip():
                    st.write(item["answer"])
                else:
                    st.write("_No typed answer was saved for this question._")

                a, b, c, d = st.columns(4)

                a.metric("Development", f"{item['development']}/30")
                b.metric("Structure", f"{item['structure']}/25")
                c.metric("Specificity", f"{item['specificity']}/25")
                d.metric("Relevance", f"{item['relevance']}/20")

                st.markdown("**Suggestions**")

                for suggestion in item["feedback"]:
                    st.write(f"• {suggestion}")

                if item["words"] < 25:
                    st.markdown(
                        '<div class="tip"><b>Try this:</b> '
                        'Use the STAR method: Situation, Task, Action, Result. '
                        'Explain what you personally did and what happened.</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("### Practice history")

        history_df = pd.DataFrame([
            {
                "Date": item["date"],
                "Candidate": item["name"],
                "Role": item["role"],
                "Interview type": item["interview_type"],
                "Questions": item["questions_count"],
                "Score": item["overall_score"],
            }
            for item in history
        ])

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        if len(history_df) > 1:
            st.markdown("#### Score progression")
            progress_df = history_df[["Date", "Score"]].copy()
            progress_df["Session"] = [
                f"Session {i + 1}"
                for i in range(len(progress_df))
            ]
            st.line_chart(
                progress_df.set_index("Session")[["Score"]],
                height=250,
            )

        csv_data = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download practice history (CSV)",
            data=csv_data,
            file_name="interviewready_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.button(
            "🔄 Start another interview",
            type="primary",
            use_container_width=True,
            on_click=lambda: (
                st.session_state.update({"navigation": "Setup"})
            ),
        )

    st.markdown(
        '<div class="footer">InterviewReady MVP · Results are session-based and '
        'may be lost when the app session resets. Scores are indicative practice '
        'feedback, not hiring decisions.</div>',
        unsafe_allow_html=True,
    )

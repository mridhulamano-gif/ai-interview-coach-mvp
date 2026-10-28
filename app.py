
import random
import re
from datetime import datetime
from html import escape

import pandas as pd
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. COMPLETE THEME: NAVY, WHITE AND RED ACCENT
# =========================================================
st.markdown(
    """
    <style>
    /* Main application background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #F4F7FC !important;
        color: #172B4D !important;
    }

    [data-testid="stHeader"] {
        background-color: #F4F7FC !important;
    }

    /* Main text and headings */
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li {
        color: #263957 !important;
        -webkit-text-fill-color: #263957 !important;
    }

    .stApp [data-testid="stMarkdownContainer"] h1,
    .stApp [data-testid="stMarkdownContainer"] h2,
    .stApp [data-testid="stMarkdownContainer"] h3,
    .stApp [data-testid="stMarkdownContainer"] h4,
    .stApp [data-testid="stMarkdownContainer"] h5 {
        color: #172B4D !important;
        -webkit-text-fill-color: #172B4D !important;
    }

    /* Hero banner */
    .stApp .hero {
        background: linear-gradient(120deg, #14213D, #294B80);
        padding: 28px;
        border-radius: 17px;
        margin-bottom: 24px;
    }

    .stApp .hero h1,
    .stApp [data-testid="stMarkdownContainer"] .hero h1 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0 0 12px 0;
    }

    .stApp .hero p,
    .stApp [data-testid="stMarkdownContainer"] .hero p {
        color: #F1F5FF !important;
        -webkit-text-fill-color: #F1F5FF !important;
        margin-bottom: 0;
    }

    /* Sidebar: white text on navy */
    [data-testid="stSidebar"] {
        background-color: #14213D !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #F4F7FF !important;
        -webkit-text-fill-color: #F4F7FF !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #465675 !important;
    }

    /* Sidebar navigation labels */
    [data-testid="stSidebar"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: #F4F7FF !important;
        -webkit-text-fill-color: #F4F7FF !important;
    }

    /* Widget labels */
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp .stTextInput label,
    .stApp .stSelectbox label,
    .stApp .stTextArea label,
    .stApp .stSlider label,
    .stApp .stNumberInput label {
        color: #263957 !important;
        -webkit-text-fill-color: #263957 !important;
    }

    /* Text fields */
    .stApp input,
    .stApp textarea {
        background-color: #FFFFFF !important;
        color: #172B4D !important;
        -webkit-text-fill-color: #172B4D !important;
        border: 1px solid #BCCADF !important;
        border-radius: 9px !important;
    }

    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: #71809A !important;
        -webkit-text-fill-color: #71809A !important;
        opacity: 1 !important;
    }

    /* Dropdown fields */
    .stApp div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #BCCADF !important;
    }

    .stApp div[data-baseweb="select"] span,
    .stApp div[data-baseweb="select"] input {
        color: #172B4D !important;
        -webkit-text-fill-color: #172B4D !important;
    }

    /* Dropdown menu options */
    [role="listbox"],
    [role="option"] {
        background-color: #FFFFFF !important;
        color: #172B4D !important;
    }

    [role="option"] * {
        color: #172B4D !important;
    }

    /* Feature and question cards */
    .stApp .question-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE4F0;
        border-left: 5px solid #315DAB;
        border-radius: 13px;
        padding: 21px;
        margin: 12px 0 18px 0;
        box-shadow: 0 2px 8px rgba(24, 44, 80, 0.04);
    }

    .stApp .question-card h4,
    .stApp [data-testid="stMarkdownContainer"] .question-card h4 {
        color: #172B4D !important;
        -webkit-text-fill-color: #172B4D !important;
    }

    .stApp .question-card p,
    .stApp [data-testid="stMarkdownContainer"] .question-card p {
        color: #334563 !important;
        -webkit-text-fill-color: #334563 !important;
        font-size: 1.05rem;
        line-height: 1.65;
    }

    .stApp .question-card strong {
        color: #315DAB !important;
    }

    /* Dashboard metric cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE4F0;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
        box-shadow: 0 2px 8px rgba(24, 44, 80, 0.04);
    }

    .metric-label {
        color: #52627D !important;
        font-size: 0.85rem;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #172B52 !important;
        font-size: 1.4rem;
        font-weight: 750;
        overflow-wrap: anywhere;
    }

    /* Buttons */
    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
        color: #FFFFFF !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #244F91 !important;
        border: 1px solid #A9BCD9 !important;
    }

    /* Notices */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    [data-testid="stAlert"] p {
        color: #172B4D !important;
    }

    /* Slider labels and value */
    .stApp [data-testid="stSlider"] * {
        accent-color: #315DAB;
    }

    /* Progress bars */
    [data-testid="stProgressBar"] {
        background-color: #DCE5F3;
    }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background-color: #244F91 !important;
        color: #FFFFFF !important;
        border-radius: 9px;
        border: 1px solid #244F91 !important;
    }

    /* Captions in the main area */
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] p {
        color: #586A85 !important;
        -webkit-text-fill-color: #586A85 !important;
    }

    /* Make focus indicators visible */
    .stApp input:focus,
    .stApp textarea:focus {
        border-color: #315DAB !important;
        box-shadow: 0 0 0 2px rgba(49, 93, 171, 0.18) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 3. INTERVIEW QUESTION BANK
# =========================================================
QUESTION_BANK = {
    "HR / Behavioral": [
        (
            "Tell me about yourself.",
            "Introduce your background, relevant skills, an achievement, and why the role fits your goals.",
            ["background", "skills", "experience", "role", "goal"],
        ),
        (
            "Describe a challenge you faced and how you handled it.",
            "Use STAR: Situation, Task, Action, Result.",
            ["challenge", "situation", "action", "result", "learned"],
        ),
        (
            "Tell me about a time you worked in a team.",
            "Explain the shared goal, your responsibility, collaboration, and outcome.",
            ["team", "collaborat", "responsib", "result", "communicat"],
        ),
        (
            "What is one strength you would bring to this role?",
            "Name a relevant strength and support it with an example.",
            ["strength", "example", "skill", "result"],
        ),
        (
            "Describe a mistake or failure and what you learned.",
            "Explain the mistake, your response, and what changed.",
            ["mistake", "learn", "improv", "responsib", "change"],
        ),
        (
            "Why do you want this role?",
            "Connect your skills and interests to the role.",
            ["role", "interest", "skill", "contribut", "company"],
        ),
        (
            "How do you manage deadlines and competing priorities?",
            "Describe how you prioritize, plan, and track progress.",
            ["priorit", "deadline", "plan", "communicat", "progress"],
        ),
        (
            "Tell me about a time you received feedback.",
            "Explain the feedback, your response, and the improvement.",
            ["feedback", "respond", "improv", "learn"],
        ),
    ],
    "Technical": [
        (
            "Explain a technical project you have worked on.",
            "Describe the problem, tools, your contribution, and results.",
            ["project", "problem", "approach", "tool", "result"],
        ),
        (
            "How would you debug a program with an unexpected result?",
            "Reproduce the issue, inspect inputs, isolate the cause, and test.",
            ["reproduce", "debug", "test", "cause", "fix"],
        ),
        (
            "Explain the difference between a list and a tuple in Python.",
            "Explain mutability, use cases, and an example.",
            ["mutable", "immutable", "change", "example", "python"],
        ),
        (
            "What is an API, and when would you use one?",
            "Explain how software communicates through requests and responses.",
            ["request", "response", "system", "data", "example"],
        ),
        (
            "How would you make a slow data-processing task faster?",
            "Measure performance, identify bottlenecks, optimize, and benchmark.",
            ["measure", "bottleneck", "algorithm", "optimiz", "test"],
        ),
        (
            "How do you test code before releasing it?",
            "Discuss unit tests, edge cases, integration, and regression tests.",
            ["test", "edge", "unit", "integration", "regression"],
        ),
        (
            "Explain a database index in simple terms.",
            "Explain faster lookups, storage needs, and write overhead.",
            ["lookup", "search", "speed", "storage", "write"],
        ),
        (
            "What is the purpose of version control?",
            "Explain change history, collaboration, branches, and recovery.",
            ["change", "collaborat", "branch", "history", "version"],
        ),
    ],
    "Situational": [
        (
            "A teammate disagrees with your approach. What would you do?",
            "Listen, compare options using evidence, and agree on a solution.",
            ["listen", "reason", "evidence", "goal", "solution"],
        ),
        (
            "You receive a task with unclear requirements. How do you proceed?",
            "Clarify the outcome, assumptions, and priorities.",
            ["clarif", "question", "assumption", "priorit", "confirm"],
        ),
        (
            "You may miss an important deadline. What do you do?",
            "Communicate the risk early and propose realistic options.",
            ["communicat", "early", "impact", "plan", "priorit"],
        ),
        (
            "A customer reports a problem you cannot solve immediately.",
            "Gather details, set expectations, and follow up.",
            ["acknowledge", "detail", "expectation", "investigat", "update"],
        ),
        (
            "You have several urgent tasks. How do you choose what comes first?",
            "Compare impact, urgency, dependencies, and available time.",
            ["impact", "urgent", "priorit", "depend", "communicat"],
        ),
        (
            "You notice an error in work already submitted. What do you do?",
            "Verify it, notify the appropriate person, correct it, and learn.",
            ["verify", "notify", "correct", "responsib", "prevent"],
        ),
    ],
}

ROLE_EXTRAS = {
    "Software Developer": [
        (
            "How would you explain a technical issue to a non-technical teammate?",
            "Use plain language, an example, and the practical impact.",
            ["plain", "impact", "example", "understand"],
        ),
        (
            "What trade-offs matter when designing a software feature?",
            "Consider user needs, maintainability, performance, security, and time.",
            ["user", "maintain", "performance", "security", "trade"],
        ),
    ],
    "Data Analyst": [
        (
            "How would you handle missing values in a dataset?",
            "Investigate missingness, assess impact, choose a method, and document it.",
            ["missing", "investigat", "method", "assumption", "document"],
        ),
        (
            "How would you explain a data insight to a business stakeholder?",
            "Present the finding, evidence, impact, and limitations.",
            ["insight", "evidence", "impact", "visual", "limitation"],
        ),
    ],
    "Marketing": [
        (
            "How would you measure whether a campaign was successful?",
            "Connect campaign objectives to KPIs, results, and costs.",
            ["objective", "metric", "kpi", "baseline", "cost"],
        ),
        (
            "How would you adapt a campaign for a different audience?",
            "Research the audience, test messages, and improve using results.",
            ["audience", "research", "message", "test", "result"],
        ),
    ],
    "Customer Support": [
        (
            "How would you handle an upset customer?",
            "Listen calmly, acknowledge the concern, offer next steps, and follow up.",
            ["listen", "acknowledge", "calm", "solution", "follow"],
        ),
        (
            "How would you identify a recurring customer issue?",
            "Review tickets, find patterns, investigate causes, and share findings.",
            ["ticket", "pattern", "frequency", "cause", "share"],
        ),
    ],
    "General / Student": [],
}

# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================
def get_questions(role, category, count, seed):
    pool = list(QUESTION_BANK[category])

    if category == "Technical":
        pool.extend(ROLE_EXTRAS.get(role, []))

    rng = random.Random(seed)
    rng.shuffle(pool)

    original = list(pool)
    while len(pool) < count:
        pool.extend(original[:count - len(pool)])

    return pool[:count]


def evaluate_answer(answer, keywords):
    cleaned = re.sub(r"\s+", " ", answer).strip()
    words = re.findall(r"\b[\w'-]+\b", cleaned)
    lower = cleaned.lower()
    word_count = len(words)

    # Answer development: 30 points
    if word_count < 8:
        length_score = 5
    elif word_count < 25:
        length_score = 15
    elif word_count < 55:
        length_score = 23
    elif word_count <= 180:
        length_score = 30
    else:
        length_score = 26

    # Relevance: 35 points
    hits = [word for word in keywords if word in lower]
    relevance_score = round(
        len(hits) / max(len(keywords), 1) * 35
    )

    # Structure: 20 points
    structure_terms = [
        "because", "first", "then", "for example", "result",
        "therefore", "learned", "finally", "however", "so that",
    ]
    structure_hits = sum(term in lower for term in structure_terms)
    structure_score = min(20, 5 + structure_hits * 3)

    # Specificity: 15 points
    specificity_terms = [
        "i ", "we ", "my ", "our ", "example", "project",
        "customer", "team", "measured", "improved", "learned", "%",
    ]
    specificity_hits = sum(term in lower for term in specificity_terms)
    specificity_score = min(15, 3 + specificity_hits * 2)

    total = min(
        100,
        length_score + relevance_score + structure_score + specificity_score,
    )

    if word_count < 8:
        feedback = (
            "Your answer is very brief. Add context, your actions, "
            "and the outcome."
        )
    elif len(hits) / max(len(keywords), 1) < 0.35:
        feedback = (
            "Connect your answer more directly to the question. "
            "Include relevant concepts, skills, or actions."
        )
    elif structure_score < 11:
        feedback = (
            "Improve the structure. Explain the situation, your actions, "
            "and the result or lesson."
        )
    elif specificity_score < 9:
        feedback = (
            "Add a concrete example and explain your contribution and outcome."
        )
    else:
        feedback = (
            "Good foundation. Make sure your example clearly demonstrates "
            "the skill the question is testing."
        )

    return {
        "score": total,
        "word_count": word_count,
        "keyword_hits": hits,
        "length_score": length_score,
        "relevance_score": relevance_score,
        "structure_score": structure_score,
        "specificity_score": specificity_score,
        "feedback": feedback,
    }


def save_current_answer():
    interview = st.session_state.get("interview")
    if not interview:
        return

    index = st.session_state.get("selected_question", 0)
    key = f"answer_input_{index}"

    if key in st.session_state:
        st.session_state.answers[index] = (
            st.session_state[key].strip()
        )


def previous_question():
    save_current_answer()
    st.session_state.selected_question = max(
        0, st.session_state.selected_question - 1
    )


def next_question():
    save_current_answer()
    interview = st.session_state.get("interview")

    if interview:
        st.session_state.selected_question = min(
            len(interview["questions"]) - 1,
            st.session_state.selected_question + 1,
        )


def metric_card(label, value, suffix=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(str(label))}</div>
            <div class="metric-value">{escape(str(value))}{escape(suffix)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 5. SESSION STATE INITIALIZATION
# =========================================================
if "interview" not in st.session_state:
    st.session_state.interview = None

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "results" not in st.session_state:
    st.session_state.results = None

if "selected_question" not in st.session_state:
    st.session_state.selected_question = 0

# Change navigation before the radio widget is created.
if "next_navigation" in st.session_state:
    st.session_state["navigation"] = st.session_state.pop(
        "next_navigation"
    )

if "navigation" not in st.session_state:
    st.session_state.navigation = "Setup"


# =========================================================
# 6. SIDEBAR NAVIGATION
# =========================================================
st.sidebar.markdown("## 🎯 InterviewReady")
st.sidebar.caption("AI Interview Coach · MVP")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Setup", "Mock Interview", "Results Dashboard"],
    key="navigation",
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Practice tip**")
st.sidebar.caption(
    "For behavioral questions, try Situation, Task, Action, and Result."
)
st.sidebar.markdown("---")
st.sidebar.caption("Free demo mode · No API key required")


# =========================================================
# 7. SETUP PAGE
# =========================================================
if page == "Setup":
    st.markdown(
        """
        <div class="hero">
            <h1>Practice with purpose.</h1>
            <p>Build interview confidence, improve your answers, and track progress.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.25, 0.75], gap="large")

    with left:
        st.subheader("Set up your mock interview")

        with st.form("setup_form"):
            name = st.text_input(
                "Your name",
                placeholder="Enter your name",
            )

            role = st.selectbox(
                "Target role",
                [
                    "General / Student",
                    "Software Developer",
                    "Data Analyst",
                    "Marketing",
                    "Customer Support",
                ],
            )

            experience = st.selectbox(
                "Experience level",
                ["Student / Fresher", "Entry level", "Experienced"],
            )

            category = st.selectbox(
                "Interview type",
                ["HR / Behavioral", "Technical", "Situational"],
            )

            count = st.slider(
                "Number of questions",
                min_value=3,
                max_value=8,
                value=5,
            )

            submitted = st.form_submit_button(
                "Start mock interview",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not name.strip():
                st.error("Please enter your name before starting.")
            else:
                interview_id = datetime.now().strftime("%Y%m%d%H%M%S")

                st.session_state.interview = {
                    "name": name.strip(),
                    "role": role,
                    "experience": experience,
                    "category": category,
                    "questions": get_questions(
                        role, category, count, interview_id
                    ),
                    "started_at": datetime.now().strftime("%d %b %Y, %H:%M"),
                    "id": interview_id,
                }

                st.session_state.answers = {}
                st.session_state.results = None
                st.session_state.selected_question = 0

                st.session_state.next_navigation = "Mock Interview"
                st.rerun()

    with right:
        st.subheader("Your practice, at a glance")

        st.markdown(
            """
            <div class="question-card">
                <h4>🧭 Guided practice</h4>
                <p>Answer interview questions one at a time.</p>
                <br>
                <h4>📊 Clear scoring</h4>
                <p>Review answer development, relevance, structure, and specificity.</p>
                <br>
                <h4>🚀 Actionable feedback</h4>
                <p>Discover ways to make your answers stronger.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "This version uses a rule-based scoring rubric. "
            "Scores are practice guidance, not a hiring decision."
        )


# =========================================================
# 8. MOCK INTERVIEW PAGE
# =========================================================
elif page == "Mock Interview":
    interview = st.session_state.interview

    if not interview:
        st.warning("Please set up an interview first.")

        if st.button("Go to setup", type="primary"):
            st.session_state.next_navigation = "Setup"
            st.rerun()

    else:
        questions = interview["questions"]
        total_questions = len(questions)

        selected_q = min(
            max(0, st.session_state.selected_question),
            total_questions - 1,
        )

        st.markdown(f"## Mock interview: {interview['role']}")

        st.caption(
            f"{interview['name']} · {interview['experience']} · "
            f"{interview['category']} · Started {interview['started_at']}"
        )

        completed = sum(
            bool(st.session_state.answers.get(i, "").strip())
            for i in range(total_questions)
        )

        st.progress(
            completed / total_questions,
            text=f"{completed} of {total_questions} answers saved",
        )

        # The selectbox key is the selected question index.
        selected_q = st.selectbox(
            "Choose a question",
            options=list(range(total_questions)),
            index=selected_q,
            format_func=lambda i: f"Question {i + 1}: {questions[i][0]}",
            key="selected_question",
        )

        question_text, guidance, keywords = questions[selected_q]
        answer_key = f"answer_input_{selected_q}"

        if answer_key not in st.session_state:
            st.session_state[answer_key] = (
                st.session_state.answers.get(selected_q, "")
            )

        st.markdown(
            f"""
            <div class="question-card">
                <strong>Question {selected_q + 1} of {total_questions}</strong>
                <p>{escape(question_text)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Your answer",
            key=answer_key,
            height=220,
            placeholder="Write your answer here. Include your reasoning and an example.",
            help="Your answers are kept in the active session.",
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button(
                "← Previous",
                use_container_width=True,
                disabled=(selected_q == 0),
                on_click=previous_question,
            )

        with col2:
            st.button(
                "Save answer",
                use_container_width=True,
                on_click=save_current_answer,
            )

        with col3:
            st.button(
                "Next →",
                use_container_width=True,
                disabled=(selected_q >= total_questions - 1),
                on_click=next_question,
            )

        st.markdown("---")

        if st.button(
            "Finish interview and view results",
            type="primary",
            use_container_width=True,
        ):
            save_current_answer()
            rows = []

            for i, (question, guidance, keywords) in enumerate(questions):
                answer = st.session_state.answers.get(i, "").strip()

                if answer:
                    evaluation = evaluate_answer(answer, keywords)
                else:
                    evaluation = {
                        "score": 0,
                        "word_count": 0,
                        "keyword_hits": [],
                        "length_score": 0,
                        "relevance_score": 0,
                        "structure_score": 0,
                        "specificity_score": 0,
                        "feedback": (
                            "No answer provided. Try answering this question next time."
                        ),
                    }

                rows.append(
                    {
                        "Question": question,
                        "Answer": answer,
                        "Score": evaluation["score"],
                        "Words": evaluation["word_count"],
                        "Feedback": evaluation["feedback"],
                        "Model answer guidance": guidance,
                        "Matched topics": (
                            ", ".join(evaluation["keyword_hits"])
                            or "None detected"
                        ),
                        "Breakdown": evaluation,
                    }
                )

            average_score = round(
                sum(row["Score"] for row in rows) / len(rows)
            )

            st.session_state.results = {
                "name": interview["name"],
                "role": interview["role"],
                "experience": interview["experience"],
                "category": interview["category"],
                "date": datetime.now().strftime("%d %b %Y, %H:%M"),
                "rows": rows,
                "average": average_score,
                "id": interview["id"],
            }

            st.session_state.next_navigation = "Results Dashboard"
            st.rerun()


# =========================================================
# 9. RESULTS DASHBOARD
# =========================================================
elif page == "Results Dashboard":
    results = st.session_state.results

    if not results:
        st.info(
            "Your results will appear here after you finish an interview."
        )

        if st.button("Start a mock interview", type="primary"):
            st.session_state.next_navigation = "Setup"
            st.rerun()

    else:
        st.markdown(
            f"""
            <div class="hero">
                <h1>Interview performance report</h1>
                <p>Well done, {escape(results['name'])}! Here is your practice summary.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("Overall practice score", results["average"], "/100")

        with c2:
            metric_card("Questions", len(results["rows"]))

        with c3:
            metric_card(
                "Answered",
                sum(bool(row["Answer"].strip()) for row in results["rows"]),
            )

        with c4:
            metric_card("Target role", results["role"])

        st.caption(
            f"{results['category']} · {results['experience']} · "
            f"Completed {results['date']}"
        )

        st.subheader("Score by question")

        score_df = pd.DataFrame(
            [
                {"Question": f"Q{i + 1}", "Score": row["Score"]}
                for i, row in enumerate(results["rows"])
            ]
        )

        # Compatible with Streamlit versions without y_min/y_max support.
        st.bar_chart(
            score_df.set_index("Question"),
            y="Score",
        )

        st.subheader("Question-by-question feedback")

        for i, row in enumerate(results["rows"]):
            with st.expander(
                f"Q{i + 1}. {row['Question']} — {row['Score']}/100",
                expanded=(i == 0),
            ):
                st.markdown("**Your answer**")
                st.write(row["Answer"] or "_No answer provided._")

                st.markdown("**Feedback**")
                st.write(row["Feedback"])

                st.markdown("**Suggested answer direction**")
                st.write(row["Model answer guidance"])

                st.caption(
                    f"Words: {row['Words']} · "
                    f"Topics detected: {row['Matched topics']}"
                )

                breakdown = row["Breakdown"]

                st.markdown("**Score breakdown**")

                st.progress(
                    breakdown["length_score"] / 30,
                    text=f"Answer development: {breakdown['length_score']}/30",
                )

                st.progress(
                    breakdown["relevance_score"] / 35,
                    text=f"Topic relevance: {breakdown['relevance_score']}/35",
                )

                st.progress(
                    breakdown["structure_score"] / 20,
                    text=f"Structure: {breakdown['structure_score']}/20",
                )

                st.progress(
                    breakdown["specificity_score"] / 15,
                    text=f"Specificity: {breakdown['specificity_score']}/15",
                )

        export_rows = [
            {
                "Question number": i + 1,
                "Question": row["Question"],
                "Answer": row["Answer"],
                "Score out of 100": row["Score"],
                "Word count": row["Words"],
                "Feedback": row["Feedback"],
                "Suggested answer direction": row["Model answer guidance"],
            }
            for i, row in enumerate(results["rows"])
        ]

        csv_bytes = (
            pd.DataFrame(export_rows)
            .to_csv(index=False)
            .encode("utf-8-sig")
        )

        st.download_button(
            "Download results as CSV",
            data=csv_bytes,
            file_name="interview_coach_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button(
            "Start a new interview",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.interview = None
            st.session_state.answers = {}
            st.session_state.results = None
            st.session_state.selected_question = 0

            st.session_state.next_navigation = "Setup"
            st.rerun()


# =========================================================
# 10. FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "InterviewReady MVP · Free demo mode. Feedback is based on a "
    "rule-based scoring rubric, not a live AI model. "
    "Avoid entering confidential personal information."
)

import html
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

import streamlit as st

st.set_page_config(
    page_title="PromptMaster AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 32%),
                radial-gradient(circle at top right, rgba(168, 85, 247, 0.15), transparent 28%),
                linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%);
            color: #f8fafc;
        }

        .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px; }
        section[data-testid="stSidebar"] { background: rgba(2, 6, 23, 0.96); border-right: 1px solid rgba(148, 163, 184, 0.12); }

        div[data-testid="stTextArea"] textarea {
            background-color: rgba(2, 6, 23, 0.88);
            color: #f8fafc;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 18px;
            padding: 18px;
            font-size: 0.98rem;
            line-height: 1.55;
        }

        .hero {
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.75)),
                linear-gradient(90deg, rgba(56, 189, 248, 0.12), rgba(168, 85, 247, 0.12));
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 30px;
            padding: 42px;
            box-shadow: 0 22px 70px rgba(0, 0, 0, 0.38);
            margin-bottom: 28px;
        }

        .hero-title {
            font-size: clamp(2.4rem, 5vw, 4.8rem);
            font-weight: 900;
            line-height: 1.02;
            margin-bottom: 16px;
            letter-spacing: -0.06em;
            background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle { font-size: 1.12rem; color: #cbd5e1; max-width: 820px; line-height: 1.7; margin-bottom: 24px; }

        .badge {
            display: inline-block;
            padding: 8px 13px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.12);
            color: #7dd3fc;
            border: 1px solid rgba(56, 189, 248, 0.28);
            margin: 5px 6px 5px 0;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .pink-badge { background: rgba(244, 114, 182, 0.12); color: #f9a8d4; border: 1px solid rgba(244, 114, 182, 0.28); }
        .purple-badge { background: rgba(167, 139, 250, 0.12); color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.28); }
        .green-badge { background: rgba(34, 197, 94, 0.12); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.28); }

        .card, .glass-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.86), rgba(30, 41, 59, 0.72));
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 16px 44px rgba(0, 0, 0, 0.28);
            margin-bottom: 18px;
        }

        .feature-card {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 22px;
            padding: 22px;
            min-height: 150px;
            box-shadow: 0 14px 38px rgba(0,0,0,0.24);
        }

        .feature-icon { font-size: 2rem; margin-bottom: 10px; }
        .feature-title { font-size: 1.08rem; font-weight: 800; color: #f8fafc; margin-bottom: 7px; }
        .feature-text { color: #94a3b8; font-size: 0.92rem; line-height: 1.55; }

        .metric-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(56, 189, 248, 0.20);
            border-radius: 22px;
            padding: 21px;
            text-align: center;
            box-shadow: 0 12px 32px rgba(0,0,0,0.28);
        }

        .metric-number { font-size: 1.85rem; font-weight: 900; color: #38bdf8; line-height: 1.15; word-break: break-word; }
        .metric-label { font-size: 0.9rem; color: #cbd5e1; margin-top: 9px; font-weight: 650; }
        .metric-helper { font-size: 0.76rem; color: #94a3b8; margin-top: 4px; }

        .meter-wrap { display: flex; justify-content: center; align-items: center; padding: 8px 0 14px 0; }
        .circular-meter {
            width: 230px; height: 230px; border-radius: 50%;
            background: conic-gradient(#38bdf8 var(--score), rgba(51, 65, 85, 0.75) 0);
            display: flex; justify-content: center; align-items: center; position: relative;
            box-shadow: inset 0 0 30px rgba(56, 189, 248, 0.16), 0 0 40px rgba(56, 189, 248, 0.16);
        }
        .circular-meter::before { content: ""; width: 168px; height: 168px; background: #020617; border-radius: 50%; position: absolute; border: 1px solid rgba(148, 163, 184, 0.16); }
        .meter-content { position: relative; text-align: center; z-index: 1; }
        .meter-score { font-size: 3.2rem; font-weight: 900; color: #f8fafc; line-height: 1; }
        .meter-label { color: #94a3b8; font-size: 0.9rem; margin-top: 8px; font-weight: 650; }

        .status-good { color: #22c55e; font-weight: 800; }
        .status-average { color: #f59e0b; font-weight: 800; }
        .status-weak { color: #ef4444; font-weight: 800; }

        .weakness-box { background: rgba(239, 68, 68, 0.10); border: 1px solid rgba(239, 68, 68, 0.24); color: #fecaca; padding: 13px 15px; border-radius: 16px; margin-bottom: 11px; line-height: 1.55; }
        .suggestion-box { background: rgba(34, 197, 94, 0.10); border: 1px solid rgba(34, 197, 94, 0.24); color: #bbf7d0; padding: 13px 15px; border-radius: 16px; margin-bottom: 11px; line-height: 1.55; }

        .prompt-box {
            background: rgba(2, 6, 23, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 20px;
            padding: 18px;
            color: #e2e8f0;
            min-height: 250px;
            white-space: pre-wrap;
            line-height: 1.65;
            font-size: 0.94rem;
        }

        .section-title { font-size: 1.65rem; font-weight: 900; color: #f8fafc; margin-top: 16px; margin-bottom: 14px; letter-spacing: -0.03em; }
        .mini-title { font-weight: 800; color: #f8fafc; font-size: 1.05rem; margin-bottom: 8px; }
        .footer { color: #64748b; text-align: center; font-size: 0.86rem; margin-top: 2rem; padding: 20px 0; }

        .stButton button { background: linear-gradient(90deg, #0284c7, #7c3aed); color: white; border: none; border-radius: 14px; padding: 0.75rem 1rem; font-weight: 800; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.18); }
        .stDownloadButton button { background: rgba(15, 23, 42, 0.95); color: #e0f2fe; border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 14px; padding: 0.75rem 1rem; font-weight: 800; }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass
class CriterionResult:
    name: str
    score: int
    max_score: int
    status: str
    feedback: str


class PromptAnalyzer:
    def __init__(self, prompt: str):
        self.prompt = prompt.strip()
        self.lower_prompt = self.prompt.lower()
        self.words = re.findall(r"\b\w+\b", self.prompt)
        self.word_count = len(self.words)

    def contains_any(self, keywords: List[str]) -> bool:
        return any(keyword in self.lower_prompt for keyword in keywords)

    def analyze_clarity(self) -> CriterionResult:
        score = 0
        if self.word_count >= 4:
            score += 4
        if self.word_count >= 8:
            score += 4
        if self.word_count >= 18:
            score += 4
        if any(char in self.prompt for char in [".", "?", ":", "-"]):
            score += 3
        if not self.contains_any(["something", "stuff", "anything", "make it better"]):
            score += 5
        return CriterionResult("Clarity", min(score, 20), 20, self._status(score, 20), "Checks whether the prompt is clear, complete, and easy to understand.")

    def analyze_context(self) -> CriterionResult:
        score = 0
        context_markers = ["context", "background", "for", "about", "based on", "scenario", "project", "topic", "purpose", "goal", "problem", "case", "situation", "essay on", "report on"]
        if self.contains_any(context_markers):
            score += 7
        if self.word_count >= 12:
            score += 4
        if self.word_count >= 25:
            score += 4
        if self.contains_any(["university", "business", "student", "teacher", "customer", "beginner", "expert", "client", "audience"]):
            score += 5
        return CriterionResult("Context", min(score, 20), 20, self._status(score, 20), "Checks whether the prompt provides enough background and purpose.")

    def analyze_specificity(self) -> CriterionResult:
        score = 0
        specificity_markers = ["include", "must", "should", "avoid", "minimum", "maximum", "step by step", "examples", "points", "headings", "format", "compare", "explain", "generate", "analyze", "create", "requirements", "features", "deliverables", "essay", "report"]
        if self.contains_any(specificity_markers):
            score += 8
        if re.search(r"\d+", self.prompt):
            score += 3
        if self.contains_any(["bullet", "table", "paragraph", "code", "report", "summary", "dashboard", "essay"]):
            score += 4
        if self.word_count >= 15:
            score += 3
        if self.contains_any(["no", "without", "do not", "don't"]):
            score += 2
        return CriterionResult("Specificity", min(score, 20), 20, self._status(score, 20), "Checks whether the instructions are detailed, measurable, and specific.")

    def analyze_role_assignment(self) -> CriterionResult:
        role_patterns = ["act as", "you are", "as a", "behave as", "take the role", "senior", "expert", "teacher", "developer", "researcher", "consultant", "writer", "designer", "engineer", "strategist"]
        score = 10 if self.contains_any(role_patterns) else 0
        return CriterionResult("Role Assignment", score, 10, self._status(score, 10), "Checks whether a clear role is assigned to the AI.")

    def analyze_target_audience(self) -> CriterionResult:
        audience_patterns = ["for students", "for beginners", "for experts", "for children", "for university", "for customers", "for developers", "for teachers", "target audience", "audience", "beginner", "intermediate", "advanced", "class", "client", "user", "learners", "instructors"]
        score = 10 if self.contains_any(audience_patterns) else 0
        return CriterionResult("Target Audience", score, 10, self._status(score, 10), "Checks whether the intended audience is mentioned.")

    def analyze_output_format(self) -> CriterionResult:
        format_patterns = ["table", "bullet", "bullets", "points", "json", "markdown", "headings", "sections", "paragraph", "list", "code", "step by step", "report", "format", "dashboard", "cards", "essay"]
        score = 20 if self.contains_any(format_patterns) else 0
        return CriterionResult("Output Format", score, 20, self._status(score, 20), "Checks whether the desired response format is specified.")

    def full_analysis(self) -> Dict[str, CriterionResult]:
        return {
            "Clarity": self.analyze_clarity(),
            "Context": self.analyze_context(),
            "Specificity": self.analyze_specificity(),
            "Role Assignment": self.analyze_role_assignment(),
            "Target Audience": self.analyze_target_audience(),
            "Output Format": self.analyze_output_format(),
        }

    def total_score(self) -> int:
        return sum(item.score for item in self.full_analysis().values())

    def detect_category(self) -> Tuple[str, str]:
        category_keywords = {
            "Coding / Software Development": ["python", "code", "streamlit", "app", "developer", "function", "bug", "api", "html", "css", "javascript", "database", "github"],
            "Academic / Education": ["student", "university", "teacher", "assignment", "report", "exam", "lecture", "explain", "oel", "course", "marks", "essay", "paragraph"],
            "Business / Marketing": ["business", "marketing", "campaign", "brand", "customer", "sales", "client", "product", "strategy", "startup"],
            "Creative Writing": ["story", "poem", "script", "caption", "creative", "novel", "dialogue", "ad copy", "rewrite"],
            "Data Analysis": ["data", "csv", "excel", "chart", "visualization", "dashboard", "statistics", "analysis", "dataset", "graph"],
            "Generative AI / Prompt Engineering": ["prompt", "generative ai", "gen ai", "llm", "chatgpt", "optimize prompt", "prompt engineering"],
        }
        best_category = "General Prompt"
        best_count = 0
        for category, keywords in category_keywords.items():
            count = sum(1 for keyword in keywords if keyword in self.lower_prompt)
            if count > best_count:
                best_category = category
                best_count = count
        confidence = "High" if best_count >= 3 else "Medium" if best_count >= 1 else "Low"
        return best_category, confidence

    @staticmethod
    def _status(score: int, max_score: int) -> str:
        percentage = score / max_score
        if percentage >= 0.75:
            return "Good"
        if percentage >= 0.45:
            return "Average"
        return "Weak"


class PromptOptimizer:
    def __init__(self, prompt: str, analysis: Dict[str, CriterionResult], category: str, mode: str = "Simple"):
        self.prompt = prompt.strip()
        self.lower = self.prompt.lower()
        self.analysis = analysis
        self.category = category
        self.mode = mode

    def generate_weaknesses(self) -> List[str]:
        weaknesses = []
        for name, result in self.analysis.items():
            if result.status == "Weak":
                weaknesses.append(f"{name} is weak. {result.feedback}")
            elif result.status == "Average":
                weaknesses.append(f"{name} can be improved. {result.feedback}")
        if not weaknesses:
            weaknesses.append("No major weakness detected. The prompt is already well structured.")
        return weaknesses

    def generate_suggestions(self) -> List[str]:
        suggestions = []
        if self.analysis["Role Assignment"].score < 10:
            suggestions.append("Add a clear role such as expert writer, teacher, developer, or marketing strategist.")
        if self.analysis["Context"].score < 15:
            suggestions.append("Add background context, project purpose, topic, or goal.")
        if self.analysis["Specificity"].score < 15:
            suggestions.append("Add exact requirements, sections, examples, number of points, or deliverables.")
        if self.analysis["Target Audience"].score < 10:
            suggestions.append("Mention who the response is for, such as students, beginners, clients, or developers.")
        if self.analysis["Output Format"].score < 20:
            suggestions.append("Specify the output format such as essay, report, bullet points, table, or code.")
        if self.analysis["Clarity"].score < 15:
            suggestions.append("Use complete sentences and avoid vague wording.")
        if not suggestions:
            suggestions.append("The prompt is strong. You can improve it further by adding success criteria or examples.")
        return suggestions

    def optimize_prompt(self) -> str:
        if self.mode == "Advanced":
            return self._advanced_prompt()
        return self._simple_prompt()

    def _simple_prompt(self) -> str:
        if "essay" in self.lower:
            topic = self._extract_topic(["essay on", "essay about", "essay regarding", "write essay on", "write an essay on", "write a essay on"])
            topic = self._clean_topic(topic or "Artificial Intelligence")
            return f"""
Act as an expert academic writer.

Write a well-structured essay on {topic} for university students.

Include:
1. Introduction
2. Meaning and background of {topic}
3. Applications or uses
4. Benefits and importance
5. Challenges or limitations
6. Conclusion

Use simple, clear, and academic language.
Write the essay in proper paragraphs.
""".strip()

        if "report" in self.lower:
            topic = self._extract_topic(["report on", "report about", "make report on", "create report on"])
            topic = self._clean_topic(topic or "the given topic")
            return f"""
Act as an expert academic report writer.

Create a professional report on {topic}.

The report should include:
1. Title
2. Introduction
3. Background
4. Main discussion
5. Key findings
6. Conclusion
7. Recommendations

Use clear headings and formal academic language.
""".strip()

        if any(word in self.lower for word in ["python", "streamlit", "code", "app", "dashboard", "github"]):
            return f"""
Act as a senior Python and Streamlit developer.

{self.prompt}

Requirements:
- Write clean, readable, and well-commented code.
- Use a modern and user-friendly interface.
- Handle errors properly.
- Include all required files and setup instructions.
- Explain how to run and deploy the project.

Output Format:
Provide complete code with clear headings and instructions.
""".strip()

        if "explain" in self.lower:
            topic = self._clean_topic(re.sub(r"(?i)^explain\s+", "", self.prompt).strip() or "the given topic")
            return f"""
Act as an expert teacher.

Explain {topic} in a simple and easy-to-understand way.

Include:
- Definition
- Key points
- Real-life example
- Advantages or uses
- Short summary

Use clear headings and bullet points.
""".strip()

        if any(word in self.lower for word in ["marketing", "campaign", "business", "brand", "sales"]):
            return f"""
Act as a professional marketing strategist.

{self.prompt}

Include:
- Target audience
- Main objective
- Strategy
- Content ideas
- Expected results
- Key performance indicators

Use professional and practical language.
""".strip()

        return f"""
Act as an expert assistant.

Improve and complete this task:
{self.prompt}

Make the response clear, specific, well-structured, and easy to understand.
Use headings and bullet points where helpful.
""".strip()

    def _advanced_prompt(self) -> str:
        simple = self._simple_prompt()
        return f"""
{simple}

Additional Quality Requirements:
- Keep the answer relevant to the user's purpose.
- Avoid vague or unnecessary information.
- Add examples where helpful.
- Mention assumptions if any information is missing.
- Ensure the final response is ready to use.
""".strip()

    def _extract_topic(self, patterns: List[str]) -> str:
        for pattern in patterns:
            index = self.lower.find(pattern)
            if index != -1:
                return self.prompt[index + len(pattern):].strip(" .:-")
        words = self.prompt.split()
        if len(words) >= 3:
            return " ".join(words[2:]).strip(" .:-")
        return ""

    @staticmethod
    def _clean_topic(topic: str) -> str:
        replacements = {
            "ai": "Artificial Intelligence",
            "AI": "Artificial Intelligence",
            "a.i": "Artificial Intelligence",
        }
        stripped = topic.strip()
        return replacements.get(stripped, stripped)


def get_score_label(score: int) -> Tuple[str, str]:
    if score >= 85:
        return "Excellent", "status-good"
    if score >= 70:
        return "Strong", "status-good"
    if score >= 50:
        return "Needs Improvement", "status-average"
    return "Weak", "status-weak"


def render_metric_card(label: str, value: str, helper: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{html.escape(str(value))}</div>
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-helper">{html.escape(str(helper))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_circular_meter(score: int, label: str):
    degrees = int((score / 100) * 360)
    st.markdown(
        f"""
        <div class="meter-wrap">
            <div class="circular-meter" style="--score: {degrees}deg;">
                <div class="meter-content">
                    <div class="meter-score">{score}</div>
                    <div class="meter-label">{html.escape(label)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sample_prompts() -> Dict[str, str]:
    return {
        "Weak Essay Prompt": "write essay on AI",
        "Academic Prompt": "You are an expert teacher. Explain diffusion models for university students. Include definition, working, advantages, limitations, and examples in bullet points.",
        "Coding Prompt": "You are a senior Python and Streamlit developer. Build a dashboard app that uploads CSV files, shows charts, displays summary statistics, and uses a professional dark UI.",
        "Marketing Prompt": "Act as a digital marketing strategist. Create a social media campaign for a new coffee shop. Target audience is university students. Include content ideas, captions, posting schedule, and KPIs.",
        "Data Analysis Prompt": "You are a data analyst. Analyze a sales dataset and create a report with trends, charts, insights, and business recommendations for managers.",
    }


def generate_quality_report(original_prompt, optimized_prompt, original_score, optimized_score, category, confidence, analysis, weaknesses, suggestions, mode) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "PROMPTMASTER AI - PROMPT QUALITY REPORT",
        "=" * 55,
        f"Generated At: {now}",
        f"Optimization Mode: {mode}",
        f"Detected Category: {category}",
        f"Category Confidence: {confidence}",
        f"Original Score: {original_score}/100",
        f"Optimized Score: {optimized_score}/100",
        f"Score Improvement: +{optimized_score - original_score}",
        "",
        "DETAILED CRITERIA ANALYSIS",
        "-" * 55,
    ]
    for item in analysis.values():
        lines.append(f"{item.name}: {item.score}/{item.max_score} - {item.status}")
        lines.append(f"Feedback: {item.feedback}\n")
    lines.append("DETECTED WEAKNESSES")
    lines.append("-" * 55)
    for weakness in weaknesses:
        lines.append(f"- {weakness}")
    lines.append("\nIMPROVEMENT SUGGESTIONS")
    lines.append("-" * 55)
    for suggestion in suggestions:
        lines.append(f"- {suggestion}")
    lines.append("\nORIGINAL PROMPT")
    lines.append("-" * 55)
    lines.append(original_prompt)
    lines.append("\nOPTIMIZED PROMPT")
    lines.append("-" * 55)
    lines.append(optimized_prompt)
    lines.append("\nThis report was generated using rule-based prompt engineering logic. No external AI API was used.")
    return "\n".join(lines)


with st.sidebar:
    st.markdown("## 🧠 PromptMaster AI")
    st.caption("Professional Rule-Based Prompt Optimizer")
    st.divider()
    selected_sample = st.selectbox("Try sample prompt", options=["None"] + list(sample_prompts().keys()))
    optimization_mode = st.radio("Optimization Mode", options=["Simple", "Advanced"], help="Simple gives short natural optimized prompts. Advanced adds extra quality instructions.")
    st.divider()
    st.markdown("### Scoring Model")
    st.caption("Clarity: 20")
    st.caption("Context: 20")
    st.caption("Specificity: 20")
    st.caption("Role Assignment: 10")
    st.caption("Target Audience: 10")
    st.caption("Output Format: 20")

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">PromptMaster AI</div>
        <div class="hero-subtitle">
            A professional SaaS-style Prompt Quality Analyzer and Auto Prompt Optimizer.
            Analyze prompts, detect weaknesses, improve structure, and generate optimized prompts
            using rule-based Generative AI prompt engineering techniques.
        </div>
        <div>
            <span class="badge">No External AI API</span>
            <span class="badge purple-badge">Prompt Engineering</span>
            <span class="badge pink-badge">Quality Scoring</span>
            <span class="badge green-badge">OEL Ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown('<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Quality Score</div><div class="feature-text">Get a 0-100 score based on six prompt quality factors.</div></div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="feature-card"><div class="feature-icon">🎯</div><div class="feature-title">Category Detection</div><div class="feature-text">Detect whether the prompt is coding, academic, marketing, data, or creative.</div></div>', unsafe_allow_html=True)
with f3:
    st.markdown('<div class="feature-card"><div class="feature-icon">⚡</div><div class="feature-title">Smart Optimizer</div><div class="feature-text">Generate short and understandable optimized prompts, not unnecessary long templates.</div></div>', unsafe_allow_html=True)
with f4:
    st.markdown('<div class="feature-card"><div class="feature-icon">📄</div><div class="feature-title">Quality Report</div><div class="feature-text">Download complete analysis, suggestions, and optimized prompt.</div></div>', unsafe_allow_html=True)

st.write("")
default_text = sample_prompts()[selected_sample] if selected_sample != "None" else ""
st.markdown('<div class="section-title">Analyze Your Prompt</div>', unsafe_allow_html=True)
input_col, info_col = st.columns([2, 1])
with input_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    prompt = st.text_area("Prompt Input Box", value=default_text, height=230, placeholder="Example: write essay on AI", label_visibility="collapsed")
    analyze_button = st.button("🚀 Analyze & Optimize Prompt", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with info_col:
    st.markdown('<div class="glass-card"><div class="mini-title">How to get a high score?</div><div class="feature-text">A strong prompt should include a clear role, context, specific instructions, target audience, and output format. Use Simple mode for clean short optimized prompts.</div><br><span class="badge">Role</span><span class="badge">Context</span><span class="badge">Specificity</span><span class="badge">Audience</span><span class="badge">Format</span></div>', unsafe_allow_html=True)

if analyze_button:
    if not prompt.strip():
        st.error("Please enter a prompt first.")
    else:
        analyzer = PromptAnalyzer(prompt)
        analysis = analyzer.full_analysis()
        original_score = analyzer.total_score()
        category, confidence = analyzer.detect_category()
        optimizer = PromptOptimizer(prompt, analysis, category, optimization_mode)
        weaknesses = optimizer.generate_weaknesses()
        suggestions = optimizer.generate_suggestions()
        optimized_prompt = optimizer.optimize_prompt()
        optimized_analyzer = PromptAnalyzer(optimized_prompt)
        optimized_score = optimized_analyzer.total_score()
        score_label, score_class = get_score_label(original_score)
        improvement = optimized_score - original_score
        report = generate_quality_report(prompt, optimized_prompt, original_score, optimized_score, category, confidence, analysis, weaknesses, suggestions, optimization_mode)

        st.markdown('<div class="section-title">Prompt Quality Dashboard</div>', unsafe_allow_html=True)
        meter_col, metric_col = st.columns([1, 2])
        with meter_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            render_circular_meter(original_score, score_label)
            st.markdown(f"<p style='text-align:center;color:#94a3b8;'>Current status: <span class='{score_class}'>{score_label}</span></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with metric_col:
            m1, m2, m3 = st.columns(3)
            with m1:
                render_metric_card("Original Score", f"{original_score}/100", "Before optimization")
            with m2:
                render_metric_card("Optimized Score", f"{optimized_score}/100", "After optimization")
            with m3:
                render_metric_card("Improvement", f"+{improvement}", "Score increase")
            c1, c2 = st.columns(2)
            with c1:
                render_metric_card("Category", category, f"Confidence: {confidence}")
            with c2:
                render_metric_card("Mode", optimization_mode, "Prompt style")

        st.markdown(f'<div class="card"><div class="mini-title">🎯 Detected Prompt Category</div><span class="badge purple-badge">{html.escape(category)}</span><span class="badge">Confidence: {html.escape(confidence)}</span><p style="color:#94a3b8; margin-top:12px;">Category detection helps the optimizer choose a better role, audience, and response structure.</p></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)
        for criterion, result in analysis.items():
            status_class = "status-good" if result.status == "Good" else "status-average" if result.status == "Average" else "status-weak"
            st.markdown('<div class="card">', unsafe_allow_html=True)
            left, right = st.columns([1, 3])
            with left:
                st.markdown(f"### {result.name}")
                st.markdown(f"Status: <span class='{status_class}'>{result.status}</span>", unsafe_allow_html=True)
                st.markdown(f"**{result.score}/{result.max_score}**")
            with right:
                st.progress(result.score / result.max_score)
                st.caption(result.feedback)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">AI Prompt Improvement Insights</div>', unsafe_allow_html=True)
        weak_col, sug_col = st.columns(2)
        with weak_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("⚠️ Detected Weaknesses")
            for weakness in weaknesses:
                st.markdown(f'<div class="weakness-box">❌ {html.escape(weakness)}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with sug_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("💡 Improvement Suggestions")
            for suggestion in suggestions:
                st.markdown(f'<div class="suggestion-box">✅ {html.escape(suggestion)}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Original vs Optimized Prompt</div>', unsafe_allow_html=True)
        original_col, optimized_col = st.columns(2)
        with original_col:
            st.markdown("### Original Prompt")
            st.markdown(f'<div class="prompt-box">{html.escape(prompt)}</div>', unsafe_allow_html=True)
        with optimized_col:
            st.markdown("### Optimized Prompt")
            st.markdown(f'<div class="prompt-box">{html.escape(optimized_prompt)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            st.download_button("⬇️ Download Optimized Prompt", data=optimized_prompt, file_name="optimized_prompt.txt", mime="text/plain", use_container_width=True)
        with d2:
            st.download_button("📄 Download Prompt Quality Report", data=report, file_name="prompt_quality_report.txt", mime="text/plain", use_container_width=True)
else:
    st.info("Choose a sample prompt or enter your own prompt, then click Analyze & Optimize Prompt.")

st.markdown('<div class="section-title">Project Methodology</div>', unsafe_allow_html=True)
with st.expander("How PromptMaster AI Works"):
    st.markdown(
        """
        PromptMaster AI uses a rule-based prompt engineering approach.

        It does not use OpenAI, Gemini, Claude, or any external AI API.

        The system evaluates prompts using six quality factors:

        | Factor | Marks |
        |---|---:|
        | Clarity | 20 |
        | Context | 20 |
        | Specificity | 20 |
        | Role Assignment | 10 |
        | Target Audience | 10 |
        | Output Format | 20 |
        | **Total** | **100** |

        The optimizer now supports two modes:

        - **Simple Mode:** short, natural, easy-to-understand optimized prompts.
        - **Advanced Mode:** detailed optimized prompts with extra quality instructions.
        """
    )

st.markdown('<div class="footer">PromptMaster AI — Rule-Based Generative AI OEL Project | Python 3.11+ | Streamlit | No External AI API</div>', unsafe_allow_html=True)

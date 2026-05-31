import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

import streamlit as st

st.set_page_config(page_title="PromptMaster AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp {background: radial-gradient(circle at top left, rgba(56,189,248,.18), transparent 32%), radial-gradient(circle at top right, rgba(168,85,247,.15), transparent 28%), linear-gradient(135deg,#020617 0%,#0f172a 50%,#111827 100%); color:#f8fafc;}
.block-container {padding-top:2rem; padding-bottom:3rem; max-width:1300px;}
section[data-testid="stSidebar"] {background:rgba(2,6,23,.96); border-right:1px solid rgba(148,163,184,.12);}
div[data-testid="stTextArea"] textarea {background-color:rgba(2,6,23,.88); color:#f8fafc; border:1px solid rgba(56,189,248,.35); border-radius:18px; padding:18px; font-size:.98rem; line-height:1.55;}
.hero {background:linear-gradient(135deg,rgba(15,23,42,.92),rgba(30,41,59,.75)); border:1px solid rgba(148,163,184,.16); border-radius:30px; padding:42px; box-shadow:0 22px 70px rgba(0,0,0,.38); margin-bottom:28px;}
.hero-title {font-size:clamp(2.4rem,5vw,4.8rem); font-weight:900; line-height:1.02; margin-bottom:16px; letter-spacing:-.06em; background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.hero-subtitle {font-size:1.12rem; color:#cbd5e1; max-width:820px; line-height:1.7; margin-bottom:24px;}
.badge {display:inline-block; padding:8px 13px; border-radius:999px; background:rgba(56,189,248,.12); color:#7dd3fc; border:1px solid rgba(56,189,248,.28); margin:5px 6px 5px 0; font-size:.82rem; font-weight:700;}
.pink-badge {background:rgba(244,114,182,.12); color:#f9a8d4; border:1px solid rgba(244,114,182,.28);} .purple-badge {background:rgba(167,139,250,.12); color:#c4b5fd; border:1px solid rgba(167,139,250,.28);} .green-badge {background:rgba(34,197,94,.12); color:#86efac; border:1px solid rgba(34,197,94,.28);}
.card,.glass-card {background:linear-gradient(145deg,rgba(15,23,42,.86),rgba(30,41,59,.72)); border:1px solid rgba(148,163,184,.16); border-radius:24px; padding:24px; box-shadow:0 16px 44px rgba(0,0,0,.28); margin-bottom:18px;}
.feature-card {background:rgba(15,23,42,.78); border:1px solid rgba(148,163,184,.14); border-radius:22px; padding:22px; min-height:150px; box-shadow:0 14px 38px rgba(0,0,0,.24);} .feature-icon{font-size:2rem;margin-bottom:10px}.feature-title{font-size:1.08rem;font-weight:800;color:#f8fafc;margin-bottom:7px}.feature-text{color:#94a3b8;font-size:.92rem;line-height:1.55}
.metric-card {background:linear-gradient(145deg,rgba(30,41,59,.95),rgba(15,23,42,.95)); border:1px solid rgba(56,189,248,.20); border-radius:22px; padding:21px; text-align:center; box-shadow:0 12px 32px rgba(0,0,0,.28);} .metric-number{font-size:2.1rem;font-weight:900;color:#38bdf8;line-height:1}.metric-label{font-size:.9rem;color:#cbd5e1;margin-top:9px;font-weight:650}.metric-helper{font-size:.76rem;color:#94a3b8;margin-top:4px}
.meter-wrap{display:flex;justify-content:center;align-items:center;padding:8px 0 14px}.circular-meter{width:230px;height:230px;border-radius:50%;background:conic-gradient(#38bdf8 var(--score),rgba(51,65,85,.75) 0);display:flex;justify-content:center;align-items:center;position:relative;box-shadow:inset 0 0 30px rgba(56,189,248,.16),0 0 40px rgba(56,189,248,.16)}.circular-meter::before{content:"";width:168px;height:168px;background:#020617;border-radius:50%;position:absolute;border:1px solid rgba(148,163,184,.16)}.meter-content{position:relative;text-align:center;z-index:1}.meter-score{font-size:3.2rem;font-weight:900;color:#f8fafc;line-height:1}.meter-label{color:#94a3b8;font-size:.9rem;margin-top:8px;font-weight:650}
.status-good{color:#22c55e;font-weight:800}.status-average{color:#f59e0b;font-weight:800}.status-weak{color:#ef4444;font-weight:800}.weakness-box{background:rgba(239,68,68,.10);border:1px solid rgba(239,68,68,.24);color:#fecaca;padding:13px 15px;border-radius:16px;margin-bottom:11px;line-height:1.55}.suggestion-box{background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.24);color:#bbf7d0;padding:13px 15px;border-radius:16px;margin-bottom:11px;line-height:1.55}.prompt-box{background:rgba(2,6,23,.72);border:1px solid rgba(148,163,184,.20);border-radius:20px;padding:18px;color:#e2e8f0;min-height:250px;white-space:pre-wrap;line-height:1.65;font-size:.94rem}.section-title{font-size:1.65rem;font-weight:900;color:#f8fafc;margin-top:16px;margin-bottom:14px;letter-spacing:-.03em}.mini-title{font-weight:800;color:#f8fafc;font-size:1.05rem;margin-bottom:8px}.footer{color:#64748b;text-align:center;font-size:.86rem;margin-top:2rem;padding:20px 0}.stButton button{background:linear-gradient(90deg,#0284c7,#7c3aed);color:white;border:none;border-radius:14px;padding:.75rem 1rem;font-weight:800}.stDownloadButton button{background:rgba(15,23,42,.95);color:#e0f2fe;border:1px solid rgba(56,189,248,.35);border-radius:14px;padding:.75rem 1rem;font-weight:800}
</style>
""", unsafe_allow_html=True)

@dataclass
class CriterionResult:
    name: str
    score: int
    max_score: int
    status: str
    feedback: str

class PromptAnalyzer:
    def __init__(self, prompt: str):
        self.prompt = prompt.strip(); self.lower_prompt = self.prompt.lower(); self.words = re.findall(r"\b\w+\b", self.prompt); self.word_count = len(self.words)
    def contains_any(self, keywords: List[str]) -> bool: return any(k in self.lower_prompt for k in keywords)
    @staticmethod
    def _status(score: int, max_score: int) -> str:
        p = score / max_score
        return "Good" if p >= .75 else "Average" if p >= .45 else "Weak"
    def analyze_clarity(self):
        score = 0
        if self.word_count >= 8: score += 5
        if self.word_count >= 20: score += 5
        if self.word_count >= 35: score += 3
        if any(c in self.prompt for c in [".", "?", ":", "-"]): score += 3
        if not self.contains_any(["something","stuff","anything","good prompt","make it better"]): score += 4
        return CriterionResult("Clarity", min(score,20), 20, self._status(score,20), "Checks whether the prompt is clear, complete, and easy to understand.")
    def analyze_context(self):
        score = 0
        if self.contains_any(["context","background","for","about","based on","scenario","project","topic","purpose","goal","problem","case","situation"]): score += 7
        if self.word_count >= 25: score += 5
        if self.word_count >= 45: score += 3
        if self.contains_any(["university","business","student","teacher","customer","beginner","expert","client"]): score += 5
        return CriterionResult("Context", min(score,20), 20, self._status(score,20), "Checks whether the prompt provides enough background and purpose.")
    def analyze_specificity(self):
        score = 0
        if self.contains_any(["include","must","should","avoid","minimum","maximum","step by step","examples","points","headings","format","compare","explain","generate","analyze","create","requirements","features","deliverables"]): score += 8
        if re.search(r"\d+", self.prompt): score += 3
        if self.contains_any(["bullet","table","paragraph","code","report","summary","dashboard"]): score += 4
        if self.word_count >= 30: score += 3
        if self.contains_any(["no","without","do not","don't"]): score += 2
        return CriterionResult("Specificity", min(score,20), 20, self._status(score,20), "Checks whether the instructions are detailed, measurable, and specific.")
    def analyze_role_assignment(self):
        score = 10 if self.contains_any(["act as","you are","as a","behave as","take the role","senior","expert","teacher","developer","researcher","consultant","writer","designer","engineer","strategist"]) else 0
        return CriterionResult("Role Assignment", score, 10, self._status(score,10), "Checks whether a clear role is assigned to the AI.")
    def analyze_target_audience(self):
        score = 10 if self.contains_any(["for students","for beginners","for experts","for children","for university","for customers","for developers","for teachers","target audience","audience","beginner","intermediate","advanced","class","client","user","learners","instructors"]) else 0
        return CriterionResult("Target Audience", score, 10, self._status(score,10), "Checks whether the intended audience is mentioned.")
    def analyze_output_format(self):
        score = 20 if self.contains_any(["table","bullet","bullets","points","json","markdown","headings","sections","paragraph","list","code","step by step","report","format","dashboard","cards"]) else 0
        return CriterionResult("Output Format", score, 20, self._status(score,20), "Checks whether the desired response format is specified.")
    def full_analysis(self):
        return {"Clarity": self.analyze_clarity(), "Context": self.analyze_context(), "Specificity": self.analyze_specificity(), "Role Assignment": self.analyze_role_assignment(), "Target Audience": self.analyze_target_audience(), "Output Format": self.analyze_output_format()}
    def total_score(self): return sum(i.score for i in self.full_analysis().values())
    def detect_category(self):
        cats = {"Coding / Software Development":["python","code","streamlit","app","developer","function","bug","api","html","css","javascript","database","github"],"Academic / Education":["student","university","teacher","assignment","report","exam","lecture","explain","oel","course","marks"],"Business / Marketing":["business","marketing","campaign","brand","customer","sales","client","product","strategy","startup"],"Creative Writing":["story","poem","script","caption","creative","novel","dialogue","ad copy","rewrite"],"Data Analysis":["data","csv","excel","chart","visualization","dashboard","statistics","analysis","dataset","graph"],"Generative AI / Prompt Engineering":["prompt","generative ai","gen ai","llm","chatgpt","optimize prompt","prompt engineering"]}
        best, count = "General Prompt", 0
        for cat, keys in cats.items():
            c = sum(1 for k in keys if k in self.lower_prompt)
            if c > count: best, count = cat, c
        return best, "High" if count >= 3 else "Medium" if count >= 1 else "Low"

class PromptOptimizer:
    def __init__(self, prompt, analysis, category): self.prompt = prompt.strip(); self.analysis = analysis; self.category = category
    def generate_weaknesses(self):
        w = []
        for name, r in self.analysis.items():
            if r.status == "Weak": w.append(f"{name} is weak. {r.feedback}")
            elif r.status == "Average": w.append(f"{name} can be improved. {r.feedback}")
        return w or ["No major weakness detected. The prompt is already well structured."]
    def generate_suggestions(self):
        s = []
        if self.analysis["Role Assignment"].score < 10: s.append("Add a role such as: 'You are an expert teacher' or 'Act as a senior developer'.")
        if self.analysis["Context"].score < 15: s.append("Add background context, project purpose, scenario, or goal.")
        if self.analysis["Specificity"].score < 15: s.append("Add exact requirements, constraints, examples, number of points, or deliverables.")
        if self.analysis["Target Audience"].score < 10: s.append("Mention the target audience such as students, beginners, clients, or developers.")
        if self.analysis["Output Format"].score < 20: s.append("Specify output format such as bullet points, table, report, code, or step-by-step answer.")
        if self.analysis["Clarity"].score < 15: s.append("Use complete sentences and avoid vague words such as 'something' or 'make it better'.")
        return s or ["The prompt is strong. You can improve it further by adding evaluation criteria."]
    def _role(self):
        return {"Coding / Software Development":"a senior software engineer and Python developer","Academic / Education":"an expert academic teacher","Business / Marketing":"a professional business and marketing strategist","Creative Writing":"a professional creative writer","Data Analysis":"a senior data analyst","Generative AI / Prompt Engineering":"a Generative AI prompt engineering expert"}.get(self.category,"an expert assistant")
    def _audience(self):
        low = self.prompt.lower()
        if "student" in low or "university" in low or "oel" in low: return "University students and instructors"
        if "beginner" in low: return "Beginners"
        if "client" in low or "customer" in low: return "Clients or customers"
        if "developer" in low or "python" in low or "code" in low: return "Developers and technical learners"
        return "A general audience"
    def _format(self):
        low = self.prompt.lower()
        if "table" in low: return "Use a clean table with short explanations."
        if "code" in low or "python" in low or "streamlit" in low: return "Provide clean code with comments, headings, and short explanations."
        if "report" in low: return "Use a professional report format with headings and bullet points."
        if "step by step" in low: return "Use a step-by-step format."
        return "Use clear headings, bullet points, and short paragraphs."
    def optimize_prompt(self):
        return f"""You are {self._role()}.

Task:
{self.prompt}

Prompt Category:
{self.category}

Context:
The goal is to generate a high-quality, practical, accurate, and well-structured response. The response should directly solve the user's request and avoid vague or unnecessary content.

Target Audience:
{self._audience()}

Detailed Requirements:
- Understand the task carefully before answering.
- Provide a clear, complete, and useful response.
- Include relevant details, examples, and practical guidance.
- Avoid generic explanations.
- Keep the language professional and easy to understand.
- Organize the answer logically.
- Mention assumptions if any information is missing.
- Ensure the final answer is ready to use.

Output Format:
{self._format()}

Quality Checklist:
- Clear
- Specific
- Context-aware
- Audience-friendly
- Properly formatted
- Actionable"""

def get_score_label(score): return ("Excellent","status-good") if score >= 85 else ("Strong","status-good") if score >= 70 else ("Needs Improvement","status-average") if score >= 50 else ("Weak","status-weak")
def metric(label, value, helper=""): st.markdown(f'<div class="metric-card"><div class="metric-number">{value}</div><div class="metric-label">{label}</div><div class="metric-helper">{helper}</div></div>', unsafe_allow_html=True)
def meter(score, label): st.markdown(f'<div class="meter-wrap"><div class="circular-meter" style="--score:{int(score/100*360)}deg;"><div class="meter-content"><div class="meter-score">{score}</div><div class="meter-label">{label}</div></div></div></div>', unsafe_allow_html=True)
def samples(): return {"Weak Prompt":"Write something about AI.","Academic Prompt":"You are an expert teacher. Explain diffusion models for university students. Include definition, working, advantages, limitations, and examples in bullet points.","Coding Prompt":"You are a senior Python and Streamlit developer. Build a dashboard app that uploads CSV files, shows charts, displays summary statistics, and uses a professional dark UI.","Marketing Prompt":"Act as a digital marketing strategist. Create a social media campaign for a new coffee shop. Target audience is university students. Include content ideas, captions, posting schedule, and KPIs.","Data Analysis Prompt":"You are a data analyst. Analyze a sales dataset and create a report with trends, charts, insights, and business recommendations for managers."}
def report_text(original, optimized, os, ns, cat, conf, analysis, weaknesses, suggestions):
    lines=["PROMPTMASTER AI - PROMPT QUALITY REPORT","="*55,f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",f"Detected Category: {cat}",f"Category Confidence: {conf}",f"Original Score: {os}/100",f"Optimized Score: {ns}/100",f"Score Improvement: +{ns-os}","\nDETAILED CRITERIA ANALYSIS","-"*55]
    for i in analysis.values(): lines += [f"{i.name}: {i.score}/{i.max_score} - {i.status}", f"Feedback: {i.feedback}\n"]
    lines += ["DETECTED WEAKNESSES","-"*55] + [f"- {x}" for x in weaknesses] + ["\nIMPROVEMENT SUGGESTIONS","-"*55] + [f"- {x}" for x in suggestions] + ["\nORIGINAL PROMPT","-"*55,original,"\nOPTIMIZED PROMPT","-"*55,optimized,"\nThis report was generated using rule-based prompt engineering logic. No external AI API was used."]
    return "\n".join(lines)

with st.sidebar:
    st.markdown("## 🧠 PromptMaster AI"); st.caption("Professional Rule-Based Prompt Optimizer"); st.divider(); selected = st.selectbox("Try sample prompt", ["None"] + list(samples().keys())); st.divider(); st.markdown("### Scoring Model"); st.caption("Clarity: 20"); st.caption("Context: 20"); st.caption("Specificity: 20"); st.caption("Role Assignment: 10"); st.caption("Target Audience: 10"); st.caption("Output Format: 20")

st.markdown('<div class="hero"><div class="hero-title">PromptMaster AI</div><div class="hero-subtitle">A professional SaaS-style Prompt Quality Analyzer and Auto Prompt Optimizer. Analyze prompts, detect weaknesses, improve structure, and generate optimized prompts using rule-based Generative AI prompt engineering techniques.</div><div><span class="badge">No External AI API</span><span class="badge purple-badge">Prompt Engineering</span><span class="badge pink-badge">Quality Scoring</span><span class="badge green-badge">OEL Ready</span></div></div>', unsafe_allow_html=True)
cols = st.columns(4)
features=[("📊","Quality Score","Get a 0-100 score based on six prompt quality factors."),("🎯","Category Detection","Detect whether the prompt is coding, academic, marketing, data, or creative."),("⚡","Auto Optimizer","Rewrite weak prompts into structured, professional prompts automatically."),("📄","Quality Report","Download complete analysis, suggestions, and optimized prompt.")]
for col, f in zip(cols, features):
    with col: st.markdown(f'<div class="feature-card"><div class="feature-icon">{f[0]}</div><div class="feature-title">{f[1]}</div><div class="feature-text">{f[2]}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Analyze Your Prompt</div>', unsafe_allow_html=True)
input_col, info_col = st.columns([2,1])
with input_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    prompt = st.text_area("Prompt Input Box", value=samples()[selected] if selected != "None" else "", height=230, placeholder="Example: You are an expert teacher. Explain neural networks for university students using bullet points and examples...", label_visibility="collapsed")
    analyze = st.button("🚀 Analyze & Optimize Prompt", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with info_col: st.markdown('<div class="glass-card"><div class="mini-title">How to get a high score?</div><div class="feature-text">A strong prompt should include a clear role, context, specific instructions, target audience, and output format.</div><br><span class="badge">Role</span><span class="badge">Context</span><span class="badge">Specificity</span><span class="badge">Audience</span><span class="badge">Format</span></div>', unsafe_allow_html=True)

if analyze:
    if not prompt.strip(): st.error("Please enter a prompt first.")
    else:
        a=PromptAnalyzer(prompt); analysis=a.full_analysis(); original_score=a.total_score(); cat,conf=a.detect_category(); opt=PromptOptimizer(prompt,analysis,cat); weaknesses=opt.generate_weaknesses(); suggestions=opt.generate_suggestions(); optimized=opt.optimize_prompt(); new_score=PromptAnalyzer(optimized).total_score(); label, cls=get_score_label(original_score); rpt=report_text(prompt,optimized,original_score,new_score,cat,conf,analysis,weaknesses,suggestions)
        st.markdown('<div class="section-title">Prompt Quality Dashboard</div>', unsafe_allow_html=True)
        mc, mt = st.columns([1,2])
        with mc: st.markdown('<div class="glass-card">', unsafe_allow_html=True); meter(original_score,label); st.markdown(f"<p style='text-align:center;color:#94a3b8;'>Current status: <span class='{cls}'>{label}</span></p>", unsafe_allow_html=True); st.markdown('</div>', unsafe_allow_html=True)
        with mt:
            c=st.columns(3); 
            with c[0]: metric("Original Score",f"{original_score}/100","Before optimization")
            with c[1]: metric("Optimized Score",f"{new_score}/100","After optimization")
            with c[2]: metric("Improvement",f"+{new_score-original_score}","Score increase")
            c=st.columns(2)
            with c[0]: metric("Category",cat,f"Confidence: {conf}")
            with c[1]: metric("Prompt Words",str(a.word_count),"Input length")
        st.markdown(f'<div class="card"><div class="mini-title">🎯 Detected Prompt Category</div><span class="badge purple-badge">{cat}</span><span class="badge">Confidence: {conf}</span><p style="color:#94a3b8; margin-top:12px;">Category detection helps the optimizer choose a better role, audience, and response structure.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)
        for _,r in analysis.items():
            scls = "status-good" if r.status=="Good" else "status-average" if r.status=="Average" else "status-weak"
            st.markdown('<div class="card">', unsafe_allow_html=True); l,rcol=st.columns([1,3])
            with l: st.markdown(f"### {r.name}"); st.markdown(f"Status: <span class='{scls}'>{r.status}</span>", unsafe_allow_html=True); st.markdown(f"**{r.score}/{r.max_score}**")
            with rcol: st.progress(r.score/r.max_score); st.caption(r.feedback)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Prompt Improvement Insights</div>', unsafe_allow_html=True)
        wc, sc = st.columns(2)
        with wc:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.subheader("⚠️ Detected Weaknesses")
            for w in weaknesses: st.markdown(f'<div class="weakness-box">❌ {w}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with sc:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.subheader("💡 Improvement Suggestions")
            for s in suggestions: st.markdown(f'<div class="suggestion-box">✅ {s}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Original vs Optimized Prompt</div>', unsafe_allow_html=True)
        oc, pc = st.columns(2)
        with oc: st.markdown("### Original Prompt"); st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
        with pc: st.markdown("### Optimized Prompt"); st.markdown(f'<div class="prompt-box">{optimized}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)
        d1,d2=st.columns(2)
        with d1: st.download_button("⬇️ Download Optimized Prompt", data=optimized, file_name="optimized_prompt.txt", mime="text/plain", use_container_width=True)
        with d2: st.download_button("📄 Download Prompt Quality Report", data=rpt, file_name="prompt_quality_report.txt", mime="text/plain", use_container_width=True)
else: st.info("Choose a sample prompt or enter your own prompt, then click Analyze & Optimize Prompt.")

st.markdown('<div class="section-title">Project Methodology</div>', unsafe_allow_html=True)
with st.expander("How PromptMaster AI Works"):
    st.markdown("""
PromptMaster AI uses a rule-based prompt engineering approach. It does not use OpenAI, Gemini, Claude, or any external AI API.

| Factor | Marks |
|---|---:|
| Clarity | 20 |
| Context | 20 |
| Specificity | 20 |
| Role Assignment | 10 |
| Target Audience | 10 |
| Output Format | 20 |
| **Total** | **100** |
""")
st.markdown('<div class="footer">PromptMaster AI — Rule-Based Generative AI OEL Project | Python 3.11+ | Streamlit | No External AI API</div>', unsafe_allow_html=True)

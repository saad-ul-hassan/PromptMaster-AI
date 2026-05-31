# PromptMaster AI: Prompt Quality Analyzer & Auto Prompt Optimizer

PromptMaster AI is a professional Streamlit-based Generative AI OEL project that analyzes prompt quality and automatically optimizes prompts using rule-based prompt engineering techniques.

## Key Features

- Modern SaaS-style Streamlit interface
- Circular score meter
- Prompt quality score from 0 to 100
- Prompt category detection
- Detailed analysis of clarity, context, specificity, role assignment, target audience, and output format
- Detected weaknesses and improvement suggestions
- Auto prompt optimizer
- Original prompt vs optimized prompt comparison
- Download optimized prompt
- Download prompt quality report
- Dark professional UI
- Responsive layout
- Sample prompts
- No external AI API

## Project Structure

```text
PromptMaster-AI/
├── app.py
├── requirements.txt
├── README.md
├── assets/
```

## Tech Stack

- Python 3.11+
- Streamlit
- Rule-based prompt engineering logic

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Upload this project to GitHub.
2. Go to Streamlit Cloud.
3. Click New App.
4. Select your repository.
5. Main file path: `app.py`
6. Click Deploy.

## Important Note

This project does not use OpenAI, Gemini, Claude, or any external AI API. It is fully rule-based and suitable for a university Generative AI OEL.

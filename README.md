# 🏥 AI Healthcare Kiosk

An intelligent multi-agent AI system for automated patient pre-screening and triage.

## Features
- Multi-agent pipeline (ID → Intake → ML → Triage → AI → Safety → Recommendation → Record → Queue)
- ML-based disease prediction (scikit-learn)
- GPT-4o-mini powered clinical insights
- Priority queue management
- PDF appointment slip generation
- Voice input support

## Setup
1. Clone the repo
2. Install dependencies:
```bash
   pip install streamlit joblib scikit-learn requests reportlab SpeechRecognition python-dotenv
```
3. Create a `.env` file:
```
   OPENAI_API_KEY='your-key-here'
```
4. Run:
```bash
   streamlit run app.py
```

## Tech Stack
- Python 3.13, Streamlit, scikit-learn, OpenAI GPT-4o-mini, ReportLab, SpeechRecognition

## ⚠️ Disclaimer
This system is for informational purposes only and is not a substitute for professional medical advice.
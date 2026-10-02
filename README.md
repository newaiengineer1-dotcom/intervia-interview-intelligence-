# Intervia — Ultra Premium Modular

A Streamlit interview-intelligence MVP with five modular agents.

## UI changes
- Interview Categories and Interview Mode are consolidated into one sidebar tab: **Interview Categories & Mode**.
- The **Industry** field is removed completely.
- Candidate/role and evidence are separate from interview configuration.

## Agents
- EvidenceAgent: deterministic evidence separation.
- ResearchAgent: isolated optional company/role research adapter.
- StrategyAgent: deterministic adaptive policy.
- InterviewerAgent: question generation + Whisper transcription.
- PerformanceCoachAgent: answer evaluation.

## Run
`pip install -r requirements.txt`
`streamlit run app.py`

## Secrets
Set `GROQ_API_KEY` in Streamlit Cloud Secrets. Never commit the real key.

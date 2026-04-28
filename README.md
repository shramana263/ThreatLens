# ThreatLens: Agentic AI Security Analyst

ThreatLens is an autonomous AI-powered security analyst designed to help users investigate suspicious emails for potential threats such as phishing, scams, and malicious links. It combines a user-friendly Streamlit interface with advanced AI and cybersecurity tools to deliver clear, actionable safety verdicts.

## Features

- **Streamlit Web UI**: Paste suspicious emails and get instant analysis in your browser.
- **Autonomous Investigation**: Uses Gemini AI (Google Generative AI) to analyze email content and decide which tools to use.
- **Integrated Security Tools**:
  - **VirusTotal Scan**: Checks URLs/domains for malicious or suspicious flags.
  - **WHOIS Lookup**: Determines the age of domains to spot newly registered (potentially malicious) sites.
- **Clear Verdicts**: Provides non-technical, user-friendly recommendations (e.g., "DELETE IMMEDIATELY", "LIKELY SAFE").
- **Technical Logs**: View detailed investigation steps in an expandable section for transparency.

## How It Works

1. **User Input**: Enter the sender's email and the suspicious email content in the Streamlit UI.
2. **AI Analysis**: The Gemini-powered agent reviews the email, invokes security tools as needed, and synthesizes the results.
3. **Safety Verdict**: The app displays a clear verdict and recommendation, with technical details available for advanced users.

## Project Structure

- `main.py` — Streamlit UI and main entry point.
- `agent.py` — Defines the AI agent, workflow, and integration with Gemini and tools.
- `tools.py` — Implements security tools (VirusTotal scan, WHOIS lookup) and exposes them for the agent.
- `requirements.txt` — Python dependencies.

## Setup & Installation

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys**:
     - `VIRUSTOTAL_API_KEY` — Get from [VirusTotal](https://www.virustotal.com/gui/join-us)
     - `GEMINI_API_KEY` — Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
4. **Run the app**:
   ```bash
   streamlit run main.py
   ```

## Example .env
```
VIRUSTOTAL_API_KEY=your_virustotal_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Requirements
- Python 3.8+
- API keys for VirusTotal and Gemini

## Security & Privacy
- No email data is stored; all analysis is performed in-memory.
- API keys are loaded from your local `.env` file and never shared.

Thank you for your time and engagement.

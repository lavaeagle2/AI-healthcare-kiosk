import os
import requests
from utils import log
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def simulate_llm_triage(symptoms):
    """Uses OpenAI API to provide AI-powered triage analysis."""
    log("AI Agent", "Generating AI analysis...")
    
    prompt = f"""
    Patient symptoms: {', '.join(symptoms)}
    
    Provide a brief medical assessment in 2-3 sentences:
    1. What condition(s) these symptoms might indicate
    2. Why this matters clinically
    3. Any critical considerations
    """

    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        log("AI Agent", "Warning: No API key found")
        return f"[AI Analysis] Based on symptoms ({', '.join(symptoms)}), professional medical evaluation is recommended. Multiple conditions could present with these symptoms."

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150,
                "temperature": 0.7
            },
            timeout=10
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
        
    except requests.exceptions.Timeout:
        log("AI Agent", "Request timeout")
        return f"[AI Analysis] Timeout occurred. Based on reported symptoms, medical consultation is advised."
    except requests.exceptions.RequestException as e:
        log("AI Agent", f"API error: {str(e)}")
        return f"[AI Analysis] Based on symptoms ({', '.join(symptoms)}), professional evaluation recommended."
    except (KeyError, IndexError) as e:
        log("AI Agent", f"Parse error: {str(e)}")
        return f"[AI Analysis] Unable to generate detailed analysis. Please consult a healthcare provider."

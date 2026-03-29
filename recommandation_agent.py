
from utils import log
class RecommendationAgent:
    
    """Suggests next steps based on risk level."""

    PLANS = {
        "LOW": {
            "action": "Home Care",
            "advice": [
                "Rest and stay hydrated.",
                "Monitor your symptoms for 24–48 hours.",
                "Use over-the-counter remedies as appropriate.",
                "Contact a doctor if symptoms worsen.",
            ],
        },
        "MEDIUM": {
            "action": "Schedule a Doctor Visit",
            "advice": [
                "Book an appointment with your primary care physician within 24 hours.",
                "Avoid strenuous activity until evaluated.",
                "Keep a symptom diary (onset, duration, severity).",
                "Go to urgent care if symptoms escalate.",
            ],
        },
        "HIGH": {
            "action": "Seek Emergency Care Immediately",
            "advice": [
                "Call 911 or go to the nearest emergency room NOW.",
                "Do not drive yourself — ask someone to take you or call an ambulance.",
                "If conscious, sit or lie in a comfortable position.",
                "Do not eat or drink anything until seen by a medical professional.",
            ],
        },
    }

    def process(self, triage: dict) -> dict:
        log("Recommandation Agent", "Processing user input...")
        print("\n" + "=" * 60)
        print("💊  RECOMMENDATION AGENT")
        print("=" * 60)
        plan = self.PLANS[triage["risk_level"]]
        print(f"  Recommended Action: {plan['action']}")
        for i, tip in enumerate(plan["advice"], 1):
            print(f"    {i}. {tip}")
        return {
            "action": plan["action"],
            "advice": plan["advice"],
            }
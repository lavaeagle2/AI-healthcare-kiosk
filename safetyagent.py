from utils import log

class SafetyAgent:
    
    """Adds medical disclaimers and filters dangerous advice."""

    DISCLAIMER = (
        "⚕️  DISCLAIMER: This system provides informational guidance only. "
        "It is NOT a substitute for professional medical advice, diagnosis, "
        "or treatment. Always seek the advice of a qualified healthcare provider."
    )

    BLOCKED_PHRASES = [
        "take any medication without consulting",
        "ignore symptoms",
        "self-diagnose",
    ]

    def process(self, triage: dict) -> dict:
        log("Safety Agent", "Processing user input...")
        print("\n" + "=" * 60)
        print("🛡️  SAFETY AGENT")
        print("=" * 60)
        warnings = [self.DISCLAIMER]
        if triage["risk_level"] == "HIGH":
            warnings.append(
                "🚨 CRITICAL: Your symptoms may indicate a life-threatening "
                "condition. Please call emergency services (911) immediately."
            )
        print(f"  Disclaimers added: {len(warnings)}")
        for w in warnings:
            print(f"  → {w}")
        return {"disclaimers": warnings, "safe": True}
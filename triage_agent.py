from utils import log

class TriageAgent:
    """Classifies risk level using rule-based keyword detection + scoring."""
   
    HIGH_KEYWORDS = [
        "chest pain", "difficulty breathing", "unconscious", "seizure",
        "severe bleeding", "stroke", "heart attack", "anaphylaxis",
        "suicidal", "overdose", "collapsed",
    ]
    MEDIUM_KEYWORDS = [
        "fever", "vomiting", "persistent cough", "abdominal pain",
        "dizziness", "blood in urine", "blood in stool", "swelling",
        "rash", "infection", "migraine", "dehydration",
    ]

    def process(self, intake: dict, predicted_disease: str = None) -> dict:
        """Process intake data and calculate risk score.
        
        Args:
            intake: Dictionary containing symptoms and raw input
            predicted_disease: Optional ML-predicted disease for risk adjustment
        """
        log("Triage Agent", "Calculating risk score...")
        print("\n" + "=" * 60)
        print("🔍  TRIAGE AGENT")
        print("=" * 60)
        
        symptoms = intake.get("symptoms", [])
        if not symptoms:
            return self._default_response()
        
        score = 0
        matched_high, matched_medium = [], []
        reasons = []

        # Keyword-based scoring
        for s in symptoms:
            s_lower = s.lower()
            found = False

            for kw in self.HIGH_KEYWORDS:
                if kw in s_lower:
                    score += 4
                    matched_high.append(kw)
                    reasons.append(f"High-risk keyword detected: '{kw}'")
                    found = True
                    break

            if not found:
                for kw in self.MEDIUM_KEYWORDS:
                    if kw in s_lower:
                        score += 2
                        matched_medium.append(kw)
                        reasons.append(f"Moderate keyword detected: '{kw}'")
                        found = True
                        break

            if not found:
                score += 1
                reasons.append(f"Unrecognized symptom: '{s}'")

        # ML-based adjustment
        if predicted_disease:
            ml_hint = predicted_disease.lower()
            if any(term in ml_hint for term in ["heart", "attack", "cardiac", "stroke"]):
                score += 3
                reasons.append(f"ML prediction indicates serious condition: {predicted_disease}")
            elif any(term in ml_hint for term in ["infection", "flu", "cold"]):
                score += 1
                reasons.append(f"ML prediction suggests common illness: {predicted_disease}")
            else:
                reasons.append(f"ML prediction: {predicted_disease}")

        # Bonus for many symptoms (indicates complexity)
        symptom_count = intake.get("count", len(symptoms))
        if symptom_count >= 4:
            score += 2
            reasons.append(f"Multiple symptoms detected ({symptom_count} total)")

        # Clamp score to 1-10 range
        score = max(1, min(score, 10))

        # Determine risk level
        if score >= 7:
            level = "HIGH"
        elif score >= 4:
            level = "MEDIUM"
        else:
            level = "LOW"

        # Ensure explanation is never empty
        if not reasons:
            reasons = ["General symptom assessment performed"]

        result = {
            "agent": "Triage Agent",
            "risk_level": level,
            "risk_score": score,
            "high_matches": list(set(matched_high)),
            "medium_matches": list(set(matched_medium)),
            "explanation": reasons,
            "predicted_disease": predicted_disease or "Unknown"
        }
        
        # Print summary
        print(f"  Risk Level : {level}")
        print(f"  Risk Score : {score}/10")
        if matched_high:
            print(f"  ⚠ Emergency keywords: {matched_high}")
        if matched_medium:
            print(f"  ⚡ Moderate keywords: {matched_medium}")
        if predicted_disease:
            print(f"  🧠 ML Prediction: {predicted_disease}")
        
        return result

    def _default_response(self):
        """Return safe default when no symptoms provided."""
        return {
            "agent": "Triage Agent",
            "risk_level": "LOW",
            "risk_score": 1,
            "high_matches": [],
            "medium_matches": [],
            "explanation": ["No specific symptoms identified"],
            "predicted_disease": "Unknown"
        }
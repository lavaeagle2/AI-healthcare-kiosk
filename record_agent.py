from utils import log

class RecordAgent:
    """Stores interactions and generates structured summary reports."""

    def __init__(self):
        self.records = []

    def process(self, intake, triage, safety, recommendation, patient, predicted_disease, ai_note) -> dict:
        """Create a complete patient record from all agent outputs.
        
        Args:
            intake: Intake agent output
            triage: Triage agent output
            safety: Safety agent output
            recommendation: Recommendation agent output
            patient: Patient information dictionary
            predicted_disease: ML-predicted disease
            ai_note: AI-generated analysis
            
        Returns:
            Complete structured record dictionary
        """
        log("Record Agent", "Generating patient record...")
        print("\n" + "=" * 60)
        print("📋  RECORD AGENT")
        print("=" * 60)
        
        from datetime import datetime

        # Build comprehensive record
        record = {
            "timestamp": datetime.now().isoformat(),
            "patient": patient,
            "ai_analysis": ai_note if ai_note else "AI analysis not available",
            "predicted_disease": predicted_disease if predicted_disease else "Unknown",
            "symptoms": intake.get("symptoms", []),
            "risk_level": triage.get("risk_level", "MEDIUM"),
            "risk_score": triage.get("risk_score", 5),
            "explanation": triage.get("explanation", ["No explanation provided"]),
            "action": recommendation.get("action", "Consult Healthcare Provider"),
            "advice": recommendation.get("advice", ["No specific advice available"]),
            "disclaimers": safety.get("disclaimers", ["Medical disclaimer: Consult a healthcare professional."]),
        }
        
        # Store in records list
        self.records.append(record)
        
        print(f"  Record #{len(self.records)} saved at {record['timestamp']}")
        print(f"  Patient: {patient.get('name', 'Unknown')}")
        print(f"  Symptoms: {len(record['symptoms'])} recorded")
        print(f"  Risk: {record['risk_level']} ({record['risk_score']}/10)")
        
        return record

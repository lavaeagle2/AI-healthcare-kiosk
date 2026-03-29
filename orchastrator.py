from intake_agent import IntakeAgent
from triage_agent import TriageAgent
from safetyagent import SafetyAgent
from recommandation_agent import RecommendationAgent
from record_agent import RecordAgent
from sim_ai import simulate_llm_triage
from utils import log
from idagent import IDAgent
from queue_manager import QueueManager
from mlmodel import predict_disease


class HealthcareKiosk:
    """Orchestrates the multi-agent pipeline."""

    def __init__(self):
        self.queue = QueueManager()
        self.id_agent = IDAgent()
        self.intake = IntakeAgent()
        self.triage = TriageAgent()
        self.safety = SafetyAgent()
        self.recommendation = RecommendationAgent()
        self.record = RecordAgent()

    def run(self, user_input: str, patient_id: str = "1234", approve: bool = True) -> dict:
        """Run the complete healthcare kiosk pipeline.
        
        Args:
            user_input: Symptom description from user
            patient_id: Patient ID for lookup (default: "1234")
            approve: Whether to generate recommendations (default: True)
            
        Returns:
            Complete patient record dictionary
        """
        log("Kiosk Agent", "Starting pipeline...")
        
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║   MULTI-AGENT HEALTHCARE AI KIOSK — SESSION START       ║")
        print("╚" + "═" * 58 + "╝")
        
        # Step 1: ID Verification
        id_data = self.id_agent.process(patient_id)
        patient = id_data["patient"]
        
        print(f"\n🪪 Patient Identified:")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")

        # Step 2: Intake Processing
        try:
            intake_data = self.intake.process(user_input)
        except Exception as e:
            log("Error", f"Intake failed: {e}")
            return self._error_response(patient, f"Intake processing error: {str(e)}")

        # Step 3: ML Disease Prediction
        try:
            predicted_disease = predict_disease(intake_data["symptoms"])
            print(f"\n🧠 ML Predicted Disease: {predicted_disease}")
        except Exception as e:
            log("Error", f"ML prediction failed: {e}")
            predicted_disease = "Unknown"

        # Step 4: Triage Assessment (with ML input)
        try:
            triage_data = self.triage.process(intake_data, predicted_disease)
        except Exception as e:
            log("Error", f"Triage failed: {e}")
            return self._error_response(patient, f"Triage processing error: {str(e)}")
        
        # Step 5: AI Analysis (ALWAYS runs)
        try:
            ai_note = simulate_llm_triage(intake_data["symptoms"])
            print(f"\n🤖 AI Insight:\n{ai_note}")
        except Exception as e:
            log("Error", f"AI analysis failed: {e}")
            ai_note = f"AI analysis unavailable. Based on symptoms, medical consultation is recommended."

        # Step 6: Safety Check
        try:
            safety_data = self.safety.process(triage_data)
        except Exception as e:
            log("Error", f"Safety check failed: {e}")
            safety_data = {"disclaimers": ["Medical disclaimer: Consult a healthcare professional."], "safe": True}

        # Step 7: Recommendation (conditional or automatic)
        if triage_data["risk_level"] == "HIGH":
            # Auto-approve for HIGH risk cases
            log("Orchestrator", "Auto-escalating due to HIGH risk")
            print("\n🚨 Emergency detected → Auto-triggering recommendation")
            rec_data = self.recommendation.process(triage_data)
        elif approve:
            # User approved recommendation
            rec_data = self.recommendation.process(triage_data)
        else:
            # User declined recommendation
            log("Orchestrator", "User skipped recommendation")
            rec_data = {"action": "Recommendation Skipped", "advice": ["User chose not to receive recommendations at this time."]}

        # Step 8: Record Generation
        try:
            record = self.record.process(
                intake_data, 
                triage_data, 
                safety_data, 
                rec_data, 
                patient, 
                predicted_disease, 
                ai_note
            )
        except Exception as e:
            log("Error", f"Record generation failed: {e}")
            return self._error_response(patient, f"Record generation error: {str(e)}")
        
        # Print summary
        self._print_summary(record)
        
        # Step 9: Queue Assignment
        try:
            queue_entry = self.queue.add_patient(record)
            record["token"] = queue_entry["token"]
            
            # Determine queue type
            queue_type = {
                "HIGH": "PRIORITY",
                "MEDIUM": "NORMAL",
                "LOW": "LOW"
            }.get(record["risk_level"], "NORMAL")
            
            print("\n✅ Workflow Status: COMPLETED")
            print("\n🧾 APPOINTMENT SLIP")
            print("=" * 40)
            print(f"Patient Name : {patient['name']}")
            print(f"Age/Gender   : {patient['age']} / {patient['gender']}")
            print(f"Symptoms     : {', '.join(record['symptoms'])}")
            print(f"Risk Level   : {record['risk_level']}")
            print(f"Action       : {record['action']}")
            print(f"Queue Type   : {queue_type}")
            print(f"Token Number : {record['token']}")
            print("=" * 40)
            
        except Exception as e:
            log("Error", f"Queue assignment failed: {e}")
            record["token"] = 0
       
        return record

    def _error_response(self, patient: dict, error_msg: str) -> dict:
        """Generate error response when pipeline fails."""
        from datetime import datetime
        return {
            "timestamp": datetime.now().isoformat(),
            "patient": patient,
            "symptoms": [],
            "predicted_disease": "Error",
            "ai_analysis": error_msg,
            "risk_level": "MEDIUM",
            "risk_score": 5,
            "explanation": [error_msg],
            "action": "System Error - Please Consult Staff",
            "advice": ["A system error occurred. Please speak with medical staff."],
            "disclaimers": ["This is an automated system. Always consult healthcare professionals."],
            "token": 0
        }

    @staticmethod
    def _print_summary(record: dict):
        """Print final summary report."""
        log("Orchestrator", "Generating final summary...")
        
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║              📝  FINAL SUMMARY REPORT                   ║")
        print("╠" + "═" * 58 + "╣")
        print(f"  Timestamp    : {record['timestamp']}")
        print(f"  Symptoms     : {', '.join(record['symptoms'])}")
        print(f"  Risk Level   : {record['risk_level']}")
        print(f"  Risk Score   : {record['risk_score']}/10")
        print(f"  Action       : {record['action']}")
        
        print("  Reasoning    :")
        if "explanation" in record and record["explanation"]:
            for r in record["explanation"]:
                print(f"    • {r}")
        
        print("  Advice       :")
        for a in record.get("advice", ["No advice available"]):
            print(f"    • {a}")
        
        print("  Disclaimers  :")
        for d in record.get("disclaimers", ["No disclaimers"]):
            print(f"    • {d}")
        
        print("╚" + "═" * 58 + "╝")










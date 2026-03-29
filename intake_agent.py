from utils import log

class IntakeAgent:
    """Cleans and structures raw user symptom input."""

    SYMPTOM_SYNONYMS = {
        "tummy ache": "abdominal pain",
        "stomach ache": "abdominal pain",
        "runny nose": "nasal congestion",
        "throwing up": "vomiting",
        "puking": "vomiting",
        "high temperature": "fever",
        "cant breathe": "difficulty breathing",
        "can't breathe": "difficulty breathing",
        "short of breath": "difficulty breathing",
    }

    def process(self, raw_input: str) -> dict:
        log("Intake Agent", "Processing user input...")
        print("\n" + "=" * 60)
        print("🏥  INTAKE AGENT")
        print("=" * 60)
        text = raw_input.strip().lower()
        # Normalize synonyms
        for syn, canonical in self.SYMPTOM_SYNONYMS.items():
            text = text.replace(syn, canonical)
        # Split into individual symptoms
        for sep in [",", ";", " and "]:
            text = text.replace(sep, "|")
        symptoms = [s.strip() for s in text.split("|") if s.strip()]
        result = {"raw": raw_input, "symptoms": symptoms, "count": len(symptoms)}
        print(f"  Raw input : {raw_input}")
        print(f"  Parsed    : {symptoms}")
        print(f"  Count     : {len(symptoms)}")
        return result
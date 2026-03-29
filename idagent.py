from utils import log

class IDAgent:
    """Simulates ID scanning and patient data extraction."""

    def process(self, id_input: str) -> dict:
        log("ID Agent", "Scanning ID...")

        # 🔥 Simulated database (replace later with OCR/API)
        mock_db = {
            "1234": {"name": "Rahul Sharma", "age": 28, "gender": "Male"},
            "5678": {"name": "Ayesha Khan", "age": 34, "gender": "Female"},
        }

        user = mock_db.get(id_input, {
            "name": "Unknown",
            "age": "N/A",
            "gender": "N/A"
        })

        return {
            "agent": "ID Agent",
            "patient": user,
            "id": id_input
        }
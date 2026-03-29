
"""
Multi-Agent Healthcare AI Kiosk System
=======================================
A modular multi-agent system that simulates an AI-powered healthcare kiosk.
Agents: Intake → Triage → Safety → Recommendation → Record
"""
from orchastrator import HealthcareKiosk
from sim_ai import simulate_llm_triage

if __name__ == "__main__":
    kiosk = HealthcareKiosk()

    # --- Demo with three test cases ---
    test_cases = [
        "I have a headache and a mild cough",
        "Fever, vomiting, and abdominal pain for 2 days",
        "Chest pain, difficulty breathing, and dizziness",
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n{'#' * 60}")
        print(f"  TEST CASE {i}: \"{case}\"")
        print(f"{'#' * 60}")

    # --- Interactive mode ---
    print("\n" + "=" * 60)
    print("  Enter your symptoms below (or 'quit' to exit)")
    print("=" * 60)
    while True:
        user = input("\n🩺 Your symptoms: ").strip()
        if user.lower() in ("quit", "exit", "q"):
            print("Thank you for using the Healthcare AI Kiosk. Stay healthy! 👋")
            break
        if user:
            kiosk.run(user)
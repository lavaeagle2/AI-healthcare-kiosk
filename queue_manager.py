class QueueManager:
    """Manages patient queue with priority-based ordering."""
    
    def __init__(self):
        self.queue = []

    def add_patient(self, record):
        """Add a patient to the queue.
        
        Args:
            record: Patient record dictionary
            
        Returns:
            Queue entry with token and priority
        """
        token = len(self.queue) + 1

        # Safe extraction of patient data
        patient = record.get("patient", {})
        name = patient.get("name", "Unknown Patient")
        risk_level = record.get("risk_level", "MEDIUM")

        entry = {
            "token": token,
            "name": name,
            "priority": risk_level,
        }

        self.queue.append(entry)
        return entry

    def get_queue(self):
        """Get current queue sorted by priority.
        
        Returns:
            List of queue entries
        """
        # Sort by priority: HIGH > MEDIUM > LOW
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        sorted_queue = sorted(
            self.queue, 
            key=lambda x: priority_order.get(x["priority"], 1)
        )
        return sorted_queue
    
    def clear_queue(self):
        """Clear all entries from queue."""
        self.queue = []
import re
import dateparser

def validate_json(json_data: dict, memory_service=None):
    """
    Normalize and validate the agent's JSON output.
    - Fill patient_email from memory if missing
    - Save patient_email back to memory if provided
    - Extract patient_name if present in raw_text
    - Normalize reminders (recurrence + datetime)
    - Normalize medications (defaults if missing)
    - Normalize conditions (lowercase)
    """

    # --- Patient email handling ---
    if not json_data.get("patient_email") and memory_service:
        remembered_email = memory_service.get("patient_email")
        if remembered_email:
            json_data["patient_email"] = remembered_email

    if json_data.get("patient_email") and memory_service:
        memory_service.set("patient_email", json_data["patient_email"])

    # --- Patient name extraction ---
    if "Patient:" in json_data.get("raw_text", ""):
        match = re.search(r"Patient:\s*([A-Za-z\s]+)", json_data["raw_text"])
        if match:
            json_data["patient_name"] = match.group(1).strip()
    else:
        json_data.setdefault("patient_name", "Patient")

    # --- Reminders normalization ---
    for reminder in json_data.get("reminders", []):
        phrase = reminder.get("timeframe", "").lower()

        if "every" in phrase or "daily" in phrase:
            reminder["recurrence"] = "daily"
        elif "weekly" in phrase:
            reminder["recurrence"] = "weekly"
        elif "monthly" in phrase:
            reminder["recurrence"] = "monthly"
        else:
            reminder["recurrence"] = None

        # Parse datetime if not already normalized and not recurring
        if not reminder.get("normalized_datetime") and not reminder["recurrence"]:
            dt = dateparser.parse(reminder["timeframe"])
            if dt:
                reminder["normalized_datetime"] = dt.isoformat()

    # --- Medications normalization ---
    for med in json_data.get("medications", []):
        med.setdefault("drug", "Unknown")
        med.setdefault("dose", "Unknown")
        med.setdefault("route", "PO")
        med.setdefault("frequency", "unspecified")

    # --- Conditions normalization ---
    json_data["conditions"] = [c.lower() for c in json_data.get("conditions", [])]

    return json_data

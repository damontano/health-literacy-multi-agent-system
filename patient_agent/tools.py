from .agent_utils import scheduler, schedule_email_job

def build_email_content(patient_name, reminder=None, med=None):
    if med:
        subject = f"Time for your medication, {patient_name}"
        body = (
            f"Hi {patient_name},\n\n"
            f"It’s time to take {med['dose']} of {med['drug']} {med['route']} {med['frequency']}.\n"
            f"Staying consistent helps manage your condition."
        )
    elif reminder and reminder.get("recurrence"):
        subject = "Daily health check reminder"
        body = (
            f"Hi {patient_name},\n\n"
            f"Don’t forget to {reminder['task']} ({reminder['timeframe']}).\n"
            f"Keeping track daily helps you stay on top of your health."
        )
    elif reminder:
        subject = "Upcoming appointment reminder"
        body = (
            f"Hi {patient_name},\n\n"
            f"Just a reminder: you have a {reminder['task']} scheduled for {reminder['normalized_datetime']}.\n"
            f"Please plan to arrive a few minutes early."
        )
    else:
        subject = "Health Reminder"
        body = f"Hi {patient_name},\n\nThis is a general health reminder."
    return subject, body


def reminder_tool(json_data: dict):
    patient_email = json_data.get("patient_email")
    patient_name = json_data.get("patient_name", "Patient")

    if not patient_email:
        return "⚠️ No email found. Please provide your email address."

    # Medication reminders
    for med in json_data.get("medications", []):
        if med.get("frequency") == "daily":
            subject, body = build_email_content(patient_name, med=med)
            scheduler.add_job(
                schedule_email_job(patient_email, subject, body),
                "cron", hour=8, minute=0
            )

    # General reminders
    for reminder in json_data.get("reminders", []):
        subject, body = build_email_content(patient_name, reminder=reminder)
        recurrence = reminder.get("recurrence")
        run_date = reminder.get("normalized_datetime")

        if recurrence == "daily":
            scheduler.add_job(schedule_email_job(patient_email, subject, body), "cron", hour=8, minute=0)
        elif recurrence == "weekly":
            scheduler.add_job(schedule_email_job(patient_email, subject, body), "cron", day_of_week="mon", hour=9, minute=0)
        elif recurrence == "monthly":
            scheduler.add_job(schedule_email_job(patient_email, subject, body), "cron", day=1, hour=9, minute=0)
        elif run_date:
            scheduler.add_job(schedule_email_job(patient_email, subject, body), "date", run_date=run_date)

    scheduler.start()
    return f"✅ Reminders scheduled for {patient_email}."


def education_tool(json_data: dict):
    explanations = []
    for med in json_data.get("medications", []):
        explanation = (
            f"Take {med['dose']} of {med['drug']} {med['route'].lower()} {med['frequency']}. "
            f"This helps manage your condition safely."
        )
        explanations.append(explanation)
    return "\n".join(explanations)


def resource_tool(json_data: dict):
    resources = []
    for condition in json_data.get("conditions", []):
        link = f"https://medlineplus.gov/{condition.replace(' ', '').lower()}.html"
        resources.append(f"- {condition.capitalize()}: {link}")
    return "\n".join(resources)

def get_manual_answer(question):
    question = question.strip().lower()

    static_answers = {
        "what is ai?": "AI stands for Artificial Intelligence.",
        "who is the dean?": "The dean is Dr. John Smith.",
        "when is the exam?": "The exam is scheduled for next Friday at 10 AM.",
        "what are the office hours?": "Office hours are Monday–Friday, 2 PM–4 PM.",
        "how can i contact support?": "You can email support at support@example.com."
        # Add more Q&A pairs here as needed
    }

    answer = static_answers.get(question)
    if answer:
        return {"answer": answer}
    return None


def get_mode_or_student_response(question):
    q = question.strip().lower()

    if q == "professor123":
        return {"mode": "professor"}

    elif q == "dean321":
        return {"mode": "dean"}

    elif "|" in q:
        parts = q.split("|")
        if len(parts) == 2:
            index = parts[0].strip()
            birthday = parts[1].strip().lower()
            if index == "12345" and birthday == "may":
                return {
                    "mode": "student",
                    "name": "Alice Smith",
                    "courses": ["Math", "Physics", "AI"],
                    "schedule": "Mon-Wed-Fri 10:00–13:00"
                }

    return None

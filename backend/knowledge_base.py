def get_manual_answer(question):
    static_answers = {
        "what is ai?": "AI stands for Artificial Intelligence.",
        "who is the dean?": "The dean is Dr. John Smith.",
        "when is the exam?": "The exam is scheduled for next Friday at 10 AM.",
        "what are the office hours?": "Office hours are Monday–Friday, 2 PM–4 PM.",
        "how can i contact support?": "You can email support at support@example.com."
    }
    return {"answer": static_answers.get(question)} if question in static_answers else None


def get_mode_or_student_response(question):
    q = question.strip().lower()

    if q == "professor123":
        return {"mode": "professor"}

    if q == "dean321":
        return {"mode": "dean"}

    if "|" in q:
        index, birthday = map(str.strip, q.split("|"))
        valid_students = {
            "12345": "may 15",
            "67890": "june 10"
        }
        if index in valid_students and valid_students[index] == birthday.lower():
            return {
                "student_id": index,
                "verified": True,
                "mode": "student",
                "message": "Welcome, student!"
            }

    return None

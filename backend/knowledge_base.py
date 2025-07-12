import csv

def get_manual_answer(question):
    question = question.strip().lower()
    try:
        with open("answers.csv", mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["question"].strip().lower() == question:
                    return {"answer": row["answer"]}
    except FileNotFoundError:
        return None

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

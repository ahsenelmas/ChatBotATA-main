from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from knowledge_base import get_manual_answer, get_mode_or_student_response

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    data_in = request.json
    question = data_in.get('question', '').strip().lower()

    # Önce özel modlara veya öğrenciye geçiş kontrolü
    mode_or_student = get_mode_or_student_response(question)
    if mode_or_student:
        return jsonify(mode_or_student)

    # CSV’den yanıt ara
    answer = get_manual_answer(question)
    if answer:
        return jsonify(answer)

    # Hiçbir eşleşme yoksa varsayılan mesaj dön
    return jsonify({"answer": "Sorry, I don't know the answer to that question."})

if __name__ == '__main__':
    app.run(debug=True)

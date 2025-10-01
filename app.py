#!/usr/bin/env python3
"""
Flask Web UI for Grade 3 Question Generator
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from database import QuestionDatabase
from generator import QuestionGenerator
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'grade3-quiz-secret-key')
CORS(app)

# Default configuration
DB_PATH = "questions.db"
LLAMA_URL = "http://localhost:11434"

db = QuestionDatabase(DB_PATH)
generator = QuestionGenerator(LLAMA_URL)


@app.route('/')
def index():
    """Home page with navigation to all features."""
    return render_template('index.html')


@app.route('/generate')
def generate_page():
    """Generate questions page."""
    return render_template('generate.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate questions."""
    data = request.json
    subject = data.get('subject', 'math')
    count = int(data.get('count', 5))
    grade = int(data.get('grade', 3))

    try:
        # Create generator with specified grade
        grade_generator = QuestionGenerator(LLAMA_URL, grade=grade)
        questions = grade_generator.generate_batch(subject, count)

        # Save to database
        saved_questions = []
        for q in questions:
            question_id = db.add_question(
                subject=q["subject"],
                question=q["question"],
                answer=q["answer"]
            )
            saved_questions.append({
                'id': question_id,
                'subject': q['subject'],
                'question': q['question'],
                'answer': q['answer']
            })

        return jsonify({
            'success': True,
            'questions': saved_questions,
            'count': len(saved_questions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/list')
def list_page():
    """List questions page."""
    return render_template('list.html')


@app.route('/api/questions', methods=['GET'])
def api_questions():
    """API endpoint to get questions."""
    subject = request.args.get('subject', None)
    limit = int(request.args.get('limit', 50))

    if subject == 'all':
        subject = None

    questions = db.get_questions(subject=subject, limit=limit)

    return jsonify({
        'success': True,
        'questions': questions,
        'count': len(questions)
    })


@app.route('/practice')
def practice_page():
    """Practice mode page."""
    return render_template('practice.html')


@app.route('/api/practice/start', methods=['POST'])
def api_practice_start():
    """API endpoint to start practice session."""
    data = request.json
    subject = data.get('subject', None)
    count = int(data.get('count', 5))

    if subject == 'all':
        subject = None

    questions = db.get_random_questions(subject=subject, count=count)

    if not questions:
        return jsonify({
            'success': False,
            'error': 'No questions found. Generate some first!'
        }), 404

    return jsonify({
        'success': True,
        'questions': questions,
        'count': len(questions)
    })


@app.route('/quiz')
def quiz_page():
    """Quiz mode page."""
    return render_template('quiz.html')


@app.route('/api/quiz/question', methods=['POST'])
def api_quiz_question():
    """API endpoint to get next quiz question."""
    data = request.json
    subject = data.get('subject', None)
    multiple_choice = data.get('multiple_choice', False)
    grade = int(data.get('grade', 3))

    if subject == 'all':
        subject = None

    # Get a random question
    questions = db.get_random_questions(subject=subject, count=1)

    if not questions:
        # Generate a new question if database is empty
        # Create generator with specified grade
        grade_generator = QuestionGenerator(LLAMA_URL, grade=grade)

        if subject:
            if subject == 'math':
                q_data = grade_generator.generate_math_question()
            else:
                q_data = grade_generator.generate_grammar_question()
        else:
            # Random subject
            subj = random.choice(["math", "grammar"])
            if subj == "math":
                q_data = grade_generator.generate_math_question()
            else:
                q_data = grade_generator.generate_grammar_question()

        # Save to database
        question_id = db.add_question(
            subject=q_data["subject"],
            question=q_data["question"],
            answer=q_data["answer"]
        )
        q = {
            'id': question_id,
            'subject': q_data['subject'],
            'question': q_data['question'],
            'answer': q_data['answer']
        }
    else:
        q = questions[0]

    response = {
        'success': True,
        'question': q
    }

    # Generate multiple choice options if requested
    if multiple_choice:
        options = _generate_multiple_choice_options(q['answer'], q['subject'])
        response['options'] = options
        response['correct_index'] = options.index(q['answer'])

    return jsonify(response)


@app.route('/api/quiz/check', methods=['POST'])
def api_quiz_check():
    """API endpoint to check quiz answer."""
    data = request.json
    user_answer = data.get('answer', '').strip()
    correct_answer = data.get('correct_answer', '').strip()

    is_correct = user_answer.lower() == correct_answer.lower()

    return jsonify({
        'success': True,
        'correct': is_correct,
        'correct_answer': correct_answer
    })


def _generate_multiple_choice_options(correct_answer: str, subject: str) -> list:
    """Generate 3 wrong options based on the correct answer."""
    options = [correct_answer]

    if subject == "math":
        # Try to parse the answer as a number
        try:
            correct_num = int(correct_answer)
            # Generate nearby wrong answers
            wrong_options = set()
            while len(wrong_options) < 3:
                offset = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                wrong_num = correct_num + offset
                if wrong_num > 0 and wrong_num != correct_num:
                    wrong_options.add(str(wrong_num))
            options.extend(list(wrong_options))
        except ValueError:
            # If answer is not a simple number, generate generic wrong options
            options.extend(["Not enough information", "Cannot be determined", "None of the above"])
    else:
        # Grammar questions - generate plausible wrong answers
        grammar_wrong = [
            "adjective", "noun", "verb", "adverb", "pronoun",
            "preposition", "conjunction", "interjection",
            "mice", "childs", "mouses", "children", "goose", "geese",
            "period", "comma", "question mark", "exclamation point"
        ]
        # Filter out the correct answer and pick 3 random wrong ones
        available_wrong = [w for w in grammar_wrong if w.lower() != correct_answer.lower()]
        options.extend(random.sample(available_wrong, min(3, len(available_wrong))))

    # Shuffle so correct answer isn't always first
    random.shuffle(options)
    return options[:4]  # Ensure we have exactly 4 options


if __name__ == '__main__':
    # Railway provides PORT via environment variable
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

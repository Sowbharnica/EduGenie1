from flask import Flask, render_template, request, jsonify
import json
import urllib.request
import urllib.error

app = Flask(__name__)

# -----------------------------
# Ollama Configuration
# -----------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


# -----------------------------
# Send Prompt to Ollama
# -----------------------------

def ask_local_ai(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            }
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        return result.get(
            "response",
            "Sorry, I could not generate an answer."
        )

    except urllib.error.URLError:
        return "Ollama is not running. Please start Ollama and try again."

    except Exception as e:
        return f"Something went wrong: {str(e)}"


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Ask ANY Question
# -----------------------------

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "response": "Please enter a question."
        })

    prompt = f"""
You are EduGenie, a friendly AI-powered educational learning assistant.

The student can ask ANY question.

Answer the question directly and accurately.

Rules:
- Do not use prepared or hardcoded answers.
- Generate the answer based on the student's question.
- Explain in simple language.
- Give examples when useful.
- For programming questions, include a small code example when appropriate.
- For comparison questions, use clear points or a table.
- For academic questions, make the explanation suitable for a college student.
- If the question is outside academics, answer helpfully.
- If you are unsure, clearly say that you are unsure.
- Do not mention Ollama or the local model.

Student question:
{question}
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Simplify Concept
# -----------------------------

@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.get_json(silent=True) or {}

    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "response": "Please enter a concept."
        })

    prompt = f"""
You are EduGenie, an educational learning assistant.

Explain this concept to a college student in very simple language.

Concept:
{topic}

Give:

1. Simple definition
2. Easy explanation
3. Real-life example
4. Technical example if relevant
5. One important point to remember

Keep the answer clear and beginner-friendly.
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Learning Path
# -----------------------------

@app.route("/learning-path", methods=["POST"])
def learning_path():
    data = request.get_json(silent=True) or {}

    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "response": "Please enter a subject."
        })

    prompt = f"""
You are EduGenie, an educational learning assistant.

Create a beginner-friendly learning path for:

{topic}

Start from the basics and gradually move to intermediate topics.

Format:
Step 1: Topic - short explanation
Step 2: Topic - short explanation
Step 3: Topic - short explanation

Include the important topics in the correct learning order.
Keep the explanation short and clear.
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Generate Quiz
# -----------------------------

@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json(silent=True) or {}

    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "quiz": [],
            "message": "Please enter a topic."
        })

    prompt = f"""
Create exactly 5 multiple-choice questions about:

{topic}

The questions should be suitable for a college beginner.

Return ONLY valid JSON in this exact format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "A. Option 1",
                "B. Option 2",
                "C. Option 3",
                "D. Option 4"
            ],
            "answer": "A. Option 1"
        }}
    ]
}}

Do not include markdown.
Do not include explanations outside the JSON.
"""

    answer = ask_local_ai(prompt)

    try:
        quiz_data = json.loads(answer)

        questions = quiz_data.get("questions", [])

        return jsonify({
            "quiz": questions
        })

    except json.JSONDecodeError:

        return jsonify({
            "quiz": [],
            "message": "Could not generate the quiz correctly. Please try again."
        })


# -----------------------------
# Summarize Text
# -----------------------------

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "response": "Please enter some text to summarize."
        })

    prompt = f"""
You are EduGenie, an educational learning assistant.

Summarize the following educational text in simple language.

Give:

1. Main idea
2. Important points
3. Short summary

Text:
{text}

Keep the summary clear and concise.
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Run Flask
# -----------------------------

if __name__=="__main__" :
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
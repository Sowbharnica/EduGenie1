from flask import Flask, render_template, request, jsonify
import json
import urllib.request
import urllib.error

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


# -----------------------------
# Ask Local AI
# -----------------------------

def ask_local_ai(question):
    prompt = f"""
You are EduGenie, a friendly educational learning assistant.

Answer the student's question clearly and accurately.

Rules:
- Give a direct answer first.
- Explain in simple language.
- Use examples when useful.
- If the question is about programming, include a small example when appropriate.
- If the student asks for a comparison, use clear points or a table.
- If the student asks something outside academics, you can still answer helpfully.
- Do not say that you are using Ollama or a local model.
- Do not say that you only know prepared questions.
- If you are unsure about something, clearly say that you are unsure instead of inventing facts.

Student question:
{question}
"""

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result.get("response", "Sorry, I could not generate an answer.")

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
# Ask Question
# -----------------------------

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "response": "Please enter a question."
        })

    answer = ask_local_ai(question)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Simplify Concept
# -----------------------------

@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "response": "Please enter a concept."
        })

    prompt = f"""
Explain the following concept to a college student in very simple language.

Concept:
{topic}

Give:
1. Simple definition
2. Easy explanation
3. One real-life example
4. One small technical example if relevant

Keep it clear and easy to understand.
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
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "response": "Please enter a subject."
        })

    prompt = f"""
Create a beginner-friendly learning path for:

{topic}

Give the topics in the correct order from beginner to intermediate.
Number each step and keep the explanation short.
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Quiz
# -----------------------------

@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "quiz": [],
            "message": "Please enter a topic."
        })

    prompt = f"""
Create 5 multiple-choice quiz questions about:

{topic}

For every question provide:
- Question
- A
- B
- C
- D
- Correct answer

Make the questions suitable for a college beginner.
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "quiz": answer
    })


# -----------------------------
# Summarizer
# -----------------------------

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "response": "Please enter some text to summarize."
        })

    prompt = f"""
Summarize the following text in simple language.

Give:
- Main idea
- Important points
- Short summary

Text:
{text}
"""

    answer = ask_local_ai(prompt)

    return jsonify({
        "response": answer
    })


# -----------------------------
# Run Flask
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
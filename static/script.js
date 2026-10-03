// -----------------------------
// Ask Question
// -----------------------------

async function askQuestion() {

    const question = document.getElementById("question").value.trim();
    const result = document.getElementById("answer");

    if (!question) {
        result.innerText = "Please enter a question.";
        return;
    }

    result.innerText = "Thinking...";

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        result.innerText = data.response;

    } catch (error) {

        result.innerText =
            "Unable to connect to EduGenie. Please try again.";
    }
}


// -----------------------------
// Simplify Concept
// -----------------------------

async function simplifyConcept() {

    const topic = document.getElementById("concept").value.trim();
    const result = document.getElementById("simpleAnswer");

    if (!topic) {
        result.innerText = "Please enter a concept.";
        return;
    }

    result.innerText = "Preparing simple explanation...";

    try {

        const response = await fetch("/simplify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic
            })
        });

        const data = await response.json();

        result.innerText = data.response;

    } catch (error) {

        result.innerText =
            "Unable to connect to EduGenie.";
    }
}


// -----------------------------
// Generate Quiz
// -----------------------------

async function generateQuiz() {

    const topic = document.getElementById("quizTopic").value.trim();
    const result = document.getElementById("quizResult");

    if (!topic) {
        result.innerText = "Please enter a topic.";
        return;
    }

    result.innerText = "Generating quiz...";

    try {

        const response = await fetch("/quiz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic
            })
        });

        const data = await response.json();

        if (!data.quiz || data.quiz.length === 0) {
            result.innerText =
                data.message || "Could not generate quiz.";
            return;
        }

        let html = "";

        data.quiz.forEach((item, index) => {

            html += `
                <div class="quiz-question">

                    <strong>
                        ${index + 1}. ${item.question}
                    </strong>

                    <ul>
                        ${item.options.map(
                            option => `<li>${option}</li>`
                        ).join("")}
                    </ul>

                    <p>
                        <strong>Answer:</strong>
                        ${item.answer}
                    </p>

                </div>
            `;
        });

        result.innerHTML = html;

    } catch (error) {

        result.innerText =
            "Unable to generate quiz. Please try again.";
    }
}


// -----------------------------
// Learning Path
// -----------------------------

async function generatePath() {

    const topic = document.getElementById("pathTopic").value.trim();
    const result = document.getElementById("pathResult");

    if (!topic) {
        result.innerText = "Please enter a subject.";
        return;
    }

    result.innerText = "Creating learning path...";

    try {

        const response = await fetch("/learning-path", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic
            })
        });

        const data = await response.json();

        result.innerText = data.response;

    } catch (error) {

        result.innerText =
            "Unable to create learning path.";
    }
}


// -----------------------------
// Summarize Text
// -----------------------------

async function summarizeText() {

    const text = document.getElementById("summaryText").value.trim();
    const result = document.getElementById("summaryResult");

    if (!text) {
        result.innerText = "Please enter some text.";
        return;
    }

    result.innerText = "Creating summary...";

    try {

        const response = await fetch("/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        result.innerText = data.response;

    } catch (error) {

        result.innerText =
            "Unable to create summary.";
    }
}
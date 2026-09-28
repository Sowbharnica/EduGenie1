async function askQuestion() {

    const question = document.getElementById("question").value;

    const result = document.getElementById("answer");

    result.innerText = "Thinking...";

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
}


async function simplifyConcept() {

    const topic = document.getElementById("concept").value;

    const result = document.getElementById("simpleAnswer");

    result.innerText = "Preparing simple explanation...";

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
}


async function generateQuiz() {

    const topic = document.getElementById("quizTopic").value;

    const result = document.getElementById("quizResult");

    result.innerHTML = "Generating quiz...";

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

        result.innerText = data.message;

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
                    ${item.options.map(option => `<li>${option}</li>`).join("")}
                </ul>

                <p>
                    <strong>Answer:</strong> ${item.answer}
                </p>

            </div>
        `;
    });

    result.innerHTML = html;
}


async function generatePath() {

    const topic = document.getElementById("pathTopic").value;

    const result = document.getElementById("pathResult");

    result.innerText = "Creating learning path...";

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

    result.innerText = data.response.join("\n");
}


async function summarizeText() {

    const text = document.getElementById("summaryText").value;

    const result = document.getElementById("summaryResult");

    result.innerText = "Creating summary...";

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
}
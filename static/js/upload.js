document.addEventListener('DOMContentLoaded', () => {
  const uploadForm = document.getElementById('upload-form');
  if (uploadForm) {
    uploadForm.addEventListener('submit', () => {
      alert('📄 Uploading PDF and generating Q&A...');
    });
  }

  // 🔁 Submit answer form handler
  async function handleQuestionsSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    try {
      const response = await fetch('/submit_answers/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
      });

      const data = await response.json();

      if (data.error) {
        alert("❌ " + data.error);
        return;
      }

      alert(data.message || "✅ Answers submitted successfully.");
      document.getElementById("random-questions-container").style.display = "none";
      showResultsButton();

    } catch (err) {
      console.error("Error submitting answers:", err);
      alert("⚠️ Error submitting answers.");
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  const questionsForm = document.getElementById('questions-form');
  if (questionsForm) {
    questionsForm.addEventListener('submit', handleQuestionsSubmit);
  }

  // 🔁 Get random questions from backend
  async function fetchNewQuestions(pdfName) {
    try {
      const response = await fetch(`/get_random_questions/?pdf_name=${encodeURIComponent(pdfName)}`);
      const data = await response.json();

      if (data.error) {
        alert("⚠️ " + data.error);
        return;
      }

      showNextQuestions(data.questions, pdfName);
    } catch (err) {
      console.error("Error fetching questions:", err);
      alert("⚠️ Failed to fetch new questions.");
    }
  }

  // 🔁 Show 5 random questions to user
  function showNextQuestions(questions, pdfName) {
    const container = document.getElementById('random-questions-container');
    if (!container) return;

    container.innerHTML = '<h3>Please answer these questions:</h3>';

    const form = document.createElement('form');
    form.id = 'questions-form';

    // CSRF and hidden inputs
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCookie('csrftoken');
    form.appendChild(csrfInput);

    form.appendChild(createHiddenInput('pdf_name', pdfName));
    form.appendChild(createHiddenInput('total', questions.length));

    questions.forEach((q, i) => {
      const index = i + 1;
      const block = document.createElement('div');
      block.className = 'question-block';

      block.innerHTML = `
        <p><strong>${q.question_id}:</strong> ${q.question}</p>
        <input type="text" name="answer_${index}" required>
        <input type="hidden" name="question_id_${index}" value="${q.question_id}">
        <input type="hidden" name="question_text_${index}" value="${q.question}">
      `;

      form.appendChild(block);
    });

    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.textContent = 'Submit Answers';
    form.appendChild(submitBtn);

    container.innerHTML = '';
    container.appendChild(form);
    container.style.display = 'block';

    form.addEventListener('submit', handleQuestionsSubmit);
  }

  function createHiddenInput(name, value) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    return input;
  }

  // 🔁 Save + View answers after evaluation
  function showResultsButton() {
    const container = document.getElementById('results-button-container');
    if (!container) return;

    const pdfName = document.getElementById('global-pdf-name')?.value;
    if (!pdfName) {
      alert("⚠️ PDF name missing.");
      return;
    }

    const button = document.createElement('button');
    button.textContent = "📊 Show Results";
    button.onclick = async () => {
      try {
        const response = await fetch('/evaluate_answers/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: `pdf_name=${encodeURIComponent(pdfName)}`
        });

        const result = await response.json();

        if (result.error) return alert("❌ " + result.error);

        displayEvaluationTable(result.detailed_scores, result.average_score);

      } catch (err) {
        console.error("Evaluation error:", err);
        alert("⚠️ Evaluation failed.");
      }
    };

    container.innerHTML = '';
    container.appendChild(button);
  }

  // 🔁 Show Evaluation Table + View Answers/Save Report buttons
  function displayEvaluationTable(questions, avgScore) {
    const resultContainer = document.getElementById('evaluation-results');
    if (!resultContainer) return;

    let tableHTML = `
      <h3>📊 Evaluation Results</h3>
      <table border="1" cellpadding="10">
        <thead>
          <tr><th>Question</th><th>Accuracy (%)</th><th>Readability</th><th>Final Score</th></tr>
        </thead>
        <tbody>
          ${questions.map(q => `
            <tr>
              <td>${q.question}</td>
              <td>${q.accuracy}</td>
              <td>${q.readability}</td>
              <td>${q.final_score}</td>
            </tr>`).join('')}
        </tbody>
      </table>
      <p><strong>Average Score:</strong> ${avgScore} / 100</p>
    `;

    resultContainer.innerHTML = tableHTML;
    resultContainer.style.display = 'block';

    const buttonContainer = document.createElement('div');
    buttonContainer.style.marginTop = '20px';

    // Save Report button
    const saveBtn = document.createElement('button');
    saveBtn.textContent = "💾 Save Report";
    saveBtn.onclick = async () => {
      const pdfName = document.getElementById('global-pdf-name')?.value;
      if (!pdfName) return alert("PDF name missing!");

      try {
        const res = await fetch('/save_report/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: `pdf_name=${encodeURIComponent(pdfName)}&score=${encodeURIComponent(avgScore)}`
        });

        const data = await res.json();
        if (data.error) return alert("❌ " + data.error);
        alert("✅ Report saved successfully.");
      } catch (err) {
        console.error("Save report error:", err);
        alert("⚠️ Failed to save report.");
      }
    };

    // View Answers button
    const viewBtn = document.createElement('button');
    viewBtn.textContent = "📄 View Answers";
    viewBtn.style.marginLeft = '10px';

    viewBtn.onclick = async () => {
      const pdfName = document.getElementById('global-pdf-name')?.value;
      if (!pdfName) return alert("⚠️ PDF name missing.");

      try {
        const response = await fetch(`/view_answers/?pdf_name=${encodeURIComponent(pdfName)}`);
        const data = await response.json();

        if (data.error) return alert("❌ " + data.error);
        if (!data.answers || data.answers.length === 0) return alert("No answers found.");

        // Setup UI
        resultContainer.innerHTML = '';
        resultContainer.style.display = 'block';

        let currentIndex = 0;
        const questionEl = document.createElement('p');
        const userAnswerEl = document.createElement('p');
        const correctAnswerEl = document.createElement('p');
        const accuracyEl = document.createElement('p');

        const navContainer = document.createElement('div');
        navContainer.style.marginTop = '15px';

        const prevBtn = document.createElement('button');
        prevBtn.textContent = '⬅️ Previous';
        prevBtn.disabled = true;

        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next ➡️';

        navContainer.appendChild(prevBtn);
        navContainer.appendChild(nextBtn);

        function updateDisplay(index) {
          const a = data.answers[index];
          questionEl.innerHTML = `<strong>Q${index + 1}:</strong> ${a.question}`;
          userAnswerEl.innerHTML = `<strong>Your Answer:</strong> ${a.user_answer}`;
          correctAnswerEl.innerHTML = `<strong>Correct Answer:</strong> ${a.correct_answer || 'N/A'}`;
          accuracyEl.innerHTML = `<strong>Accuracy:</strong> ${a.accuracy}%`;

          prevBtn.disabled = index === 0;
          nextBtn.disabled = index === data.answers.length - 1;
        }

        prevBtn.onclick = () => {
          if (currentIndex > 0) {
            currentIndex--;
            updateDisplay(currentIndex);
          }
        };

        nextBtn.onclick = () => {
          if (currentIndex < data.answers.length - 1) {
            currentIndex++;
            updateDisplay(currentIndex);
          }
        };

        resultContainer.appendChild(questionEl);
        resultContainer.appendChild(userAnswerEl);
        resultContainer.appendChild(correctAnswerEl);
        resultContainer.appendChild(accuracyEl);
        resultContainer.appendChild(navContainer);

        updateDisplay(currentIndex);

      } catch (err) {
        console.error("Error fetching answers:", err);
        alert("⚠️ Failed to fetch answers.");
      }
    };

    buttonContainer.appendChild(saveBtn);
    buttonContainer.appendChild(viewBtn);
    resultContainer.appendChild(buttonContainer);
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

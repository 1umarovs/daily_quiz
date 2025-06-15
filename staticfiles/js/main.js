let currentQuestionId = null;

function loadQuestion(category) {
    document.getElementById('question-box').textContent = "Yuklanmoqda...";

    fetch(`http://localhost:8000/api/question/?category=${category}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('question-box').textContent = data.text;
            currentQuestionId = data.id;
        })
        .catch(() => {
            document.getElementById('question-box').textContent = "Xatolik yuz berdi!";
        });
}

function getAnswer() {
    if (!currentQuestionId) {
        alert("Avval savolni tanlang!");
        return;
    }

    fetch(`http://localhost:8000/api/answer/${currentQuestionId}/`)
        .then(res => res.json())
        .then(data => {
            const modal = document.getElementById("modal");
            const content = document.getElementById("modal-content");
            content.textContent = data.answer;
            modal.style.display = "flex";
        })
        .catch(() => alert("Javobni olishda xatolik"));

    document.getElementById("modal").onclick = () => {
        document.getElementById("modal").style.display = "none";
    };
}
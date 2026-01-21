const API_URL = "http://127.0.0.1:5000/predict";

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const transcriptArea = document.getElementById("transcript");
const resultDiv = document.getElementById("result");
const englishBtn = document.getElementById("englishBtn");
const bengaliBtn = document.getElementById("bengaliBtn");

let recognition;
let finalTranscript = "";
let currentLang = "rn-IN"; 

// Language Selection
englishBtn.addEventListener("click", () => {
    currentLang = "en-IN";
    englishBtn.classList.add("active");
    bengaliBtn.classList.remove("active");
    if (recognition) recognition.lang = currentLang;
}
);;

bengaliBtn.addEventListener("click", () => {
    currentLang = "bn-IN";
    bengaliBtn.classList.add("active");
    englishBtn.classList.remove("active");
    if (recognition) recognition.lang = currentLang;
});

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    recognition = new SpeechRecognition();
    recognition.lang = currentLang;
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
        let interimTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + " ";
            } else {
                interimTranscript += transcript;
            }
        }

        transcriptArea.value = finalTranscript + interimTranscript;
    };

    recognition.onerror = (e) => {
        console.error("Speech error:", e.error);
    };

} else {
    alert("Speech Recognition not supported. Use Chrome or Edge.");
}

// START
startBtn.addEventListener("click", () => {
    finalTranscript = "";
    transcriptArea.value = "Listening...";
    resultDiv.innerHTML = "<p>Listening...</p>";

    startBtn.disabled = true;
    stopBtn.disabled = false;

    recognition.start();
});

// STOP → CALL BACKEND
stopBtn.addEventListener("click", () => {
    recognition.stop();

    startBtn.disabled = false;
    stopBtn.disabled = true;

    // Fallback: use whatever is in textarea
    const text = transcriptArea.value.replace("Listening...", "").trim();

    if (!text) {
        resultDiv.innerHTML =
            "<p style='color:red;'>No speech detected. Please speak for 2–3 seconds.</p>";
        return;
    }

    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        resultDiv.innerHTML = `
            <p><strong>Disease:</strong> ${data.disease}</p>
            <p><strong>Medicines:</strong> ${data.medicines}</p>
        `;
    })
    .catch(err => {
        console.error(err);
        resultDiv.innerHTML =
            "<p style='color:red;'>Backend not responding</p>";
    });
});

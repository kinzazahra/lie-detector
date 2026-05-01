let startTime;
let editCount = 0; // New variable to track backspaces

const textInput = document.getElementById("text");

textInput.addEventListener("focus", () => {
    if (!startTime) {
        startTime = new Date().getTime();
    }
});

// Listen for backspaces and deletes
textInput.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" || e.key === "Delete") {
        editCount++;
    }
});

textInput.addEventListener("input", (e) => {
    if (e.target.value === "") {
        startTime = null;
        editCount = 0; // Reset edits if they clear the box completely
    }
});

function analyze() {
    let text = textInput.value;
    if (!text.trim()) return;

    let endTime = new Date().getTime();
    let typingTime = startTime ? (endTime - startTime) / 1000 : 1; 

    let btn = document.querySelector('button');
    let originalText = btn.innerText;
    btn.innerText = "Analyzing...";

    // Send editCount along with the other data
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            text: text, 
            time: typingTime,
            edits: editCount 
        })
    })
    .then(res => res.json())
    .then(data => {
        btn.innerText = originalText;

        const verdictEl = document.getElementById("result-verdict");
        verdictEl.innerText = data.verdict;
        verdictEl.style.color = data.verdict === "Likely Truth" ? "#27ae60" : "#e74c3c";

        document.getElementById("stat-wpm").innerText = `${data.wpm} WPM`;
        document.getElementById("stat-sentiment").innerText = data.sentiment;
        document.getElementById("stat-flags").innerText = data.flags;
        
        // Populate the new edits stat
        document.getElementById("stat-edits").innerText = data.edits;

        document.getElementById("results-container").classList.add("visible");
        
        // Reset timers and counters for the next run
        startTime = null; 
        editCount = 0;
    })
    .catch(err => {
        console.error("Analysis failed:", err);
        btn.innerText = originalText;
    });
}
let startTime;

document.getElementById("text").addEventListener("focus", () => {
    startTime = new Date().getTime();
});

function analyze() {
    let text = document.getElementById("text").value;
    let endTime = new Date().getTime();
    let typingTime = (endTime - startTime) / 1000;

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, time: typingTime })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.result;
    });
}
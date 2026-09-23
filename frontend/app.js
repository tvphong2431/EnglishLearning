const startButton = document.getElementById("start-button");
const youtubeInput = document.getElementById("youtube-url");

async function createSession() {
    const url = youtubeInput.value.trim();

    console.log("Input value:", url);

    if (!url) {
        console.log("URL is empty");
        return;
    }

    try {
        const requestData = {
            url: url
        };

        const response = await fetch("http://127.0.0.1:8000/sessions", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error("HTTP error: " + response.status);
        }

        const data = await response.json();

        console.log("Session:", data);

    } catch (error) {
        console.log("Error:", error.message);
    }
}

startButton.addEventListener("click", createSession);
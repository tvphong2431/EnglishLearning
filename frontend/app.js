const API_URL = "http://127.0.0.1:8000";


const startDictationButton  = document.getElementById("start-dictation-btn");


startDictationButton.addEventListener(
    "click",
    createSession
);


async function createSession() {

    const input = document.getElementById("youtube-url");
    const url = input.value;

    try {
        const response = await fetch(
            `${API_URL}/sessions`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    url: url
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Create session failed"
            );
        }

        renderSession(data);

    } catch(error) {
        console.error(error);
        alert(error.message);
    }
}



function renderSession(session) {

    const info = document.getElementById("session-info");
    info.textContent =
        `Session ID: ${session.session_id}
         | Video ID: ${session.video_id}`;


    const list =document.getElementById("sentence-list");
    list.innerHTML = "";


    for (const sentence of session.sentences) {

        const item =
            document.createElement("li");


        item.textContent =
            `Sentence ${sentence.id}
             - start: ${sentence.start}s
             - duration: ${sentence.duration}s
             - words: ${sentence.word_count}`;


        list.appendChild(item);
    }
}
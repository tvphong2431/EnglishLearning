import { playSentence } from "../player/youtubePlayer.js";


export function renderSession(session) {
    renderSessionInfo(session);
    renderSentenceList(session.sentences);
}


function renderSessionInfo(session) {
    const info = document.getElementById("session-info");
    info.textContent =
        `Session ID: ${session.session_id}
         | Video ID: ${session.video_id}`;
}


function renderSentenceList(sentences) {
    const list = document.getElementById("sentence-list");
    list.innerHTML = "";


    for (const sentence of sentences) {
        const item = document.createElement("li");

        item.textContent =
            `Sentence ${sentence.id}
             - start: ${sentence.start}s
             - duration: ${sentence.duration}s
             - words: ${sentence.word_count}`;

        item.addEventListener("click", () => {
            playSentence(sentence);
        });

        list.appendChild(item);
    }
}
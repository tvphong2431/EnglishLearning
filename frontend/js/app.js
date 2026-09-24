import { createSession } from "./api/sessionApi.js";
import {
    onYouTubeIframeAPIReady,
    loadVideo
} from "./player/youtubePlayer.js";
import { renderSession } from "./ui/sessionView.js";


const startDictationButton = document.getElementById("start-dictation-btn");
startDictationButton.disabled = true;
startDictationButton.addEventListener("click", startDictation);



async function startDictation() {
    const input = document.getElementById("youtube-url");
    const url = input.value;

    try {
        const session = await createSession(url);
        loadVideo(session.video_id);
        renderSession(session);
    } catch(error) {

        console.error(error);
        alert(error.message);

    }
}

function handlePlayerReady() {
    startDictationButton.disabled = false;
}

function loadYouTubeAPI() {
    const script = document.createElement("script");
    script.src = "https://www.youtube.com/iframe_api";
    document.body.appendChild(script);
}

window.onYouTubeIframeAPIReady = () => {
    onYouTubeIframeAPIReady(handlePlayerReady);
};

loadYouTubeAPI();
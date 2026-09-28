import { createSession } from "./api/sessionApi.js";

import {
    onYouTubeIframeAPIReady,
    loadVideo,
    playSentence
} from "./player/youtubePlayer.js";

import {
    renderSession,
    showAnswerResult
} from "./ui/sessionView.js";

import { checkAnswer, getAnswer } from "./api/answerApi.js";


let currentSessionId;


const startDictationButton = document.getElementById("start-dictation-btn");
startDictationButton.disabled = true;
startDictationButton.addEventListener("click", startDictation);


async function startDictation() {
    const input = document.getElementById("youtube-url");
    const url = input.value;

    try {
        const session = await createSession(url);

        currentSessionId = session.session_id;

        loadVideo(session.video_id);

        renderSession(
            session,
            handleSentenceSelected,
            handleCheckAnswer
        );

    } catch(error) {
        console.error(error);
        alert(error.message);
    }
}


function handleSentenceSelected(sentence) {
    playSentence(sentence);
}


async function handleCheckAnswer(sentence, answer) {
    try {
        const result = await checkAnswer(
            currentSessionId,
            sentence.id,
            answer
        );

        if (result.correct) {
            showAnswerResult(
                sentence.id,
                "Correct"
            );

            return;
        }

        const answerData = await getAnswer(
            currentSessionId,
            sentence.id
        );

        showAnswerResult(
            sentence.id,
            `Incorrect. Correct answer: ${answerData.answer}`
        );

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
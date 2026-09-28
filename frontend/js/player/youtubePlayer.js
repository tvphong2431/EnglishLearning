let player;
let sentenceTimer;

const SENTENCE_PADDING = 0.2;


export function onYouTubeIframeAPIReady(onReady) {
    player = new YT.Player("player", {
        height: "360",
        width: "640",
        events: {
            onReady: onReady
        }
    });
}


export function loadVideo(videoId) {
    player.loadVideoById(videoId);
}


export function playSentence(sentence) {

    if (sentenceTimer) {
        clearInterval(sentenceTimer);
    }


    const endTime =
        sentence.start +
        sentence.duration +
        SENTENCE_PADDING;


    player.seekTo(sentence.start);
    player.playVideo();


    sentenceTimer = setInterval(() => {

        if (player.getCurrentTime() >= endTime) {
            player.pauseVideo();
            clearInterval(sentenceTimer);
        }

    }, 100);

}
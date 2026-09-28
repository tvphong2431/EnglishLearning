// Chịu trách nhiệm cho việc render UI cho session và từng sentence

// Hàm tổng
export function renderSession(session, onSentenceSelected, onCheckAnswer) {
    renderSessionInfo(session);

    renderSentenceList(
        session.sentences,
        onSentenceSelected,
        onCheckAnswer
    );
}


function renderSessionInfo(session) {
    const info = document.getElementById("session-info");

    info.textContent = `Session ID: ${session.session_id} | Video ID: ${session.video_id}`;
}

// callback là hàm được truyền vào để một module khác gọi khi có sự kiện xảy ra
function renderSentenceList(sentences, onSentenceSelected, onCheckAnswer) {
    const list = document.getElementById("sentence-list");
    list.innerHTML = ""; // xóa danh sách cũ trước khi render session mới


    for (const sentence of sentences) {

        const item = document.createElement("li");
        const sentenceInfo = document.createElement("p");
        sentenceInfo.textContent =
            `Sentence ${sentence.id}
             - start: ${sentence.start}s
             - duration: ${sentence.duration}s
             - words: ${sentence.word_count}`;


        const answerInput = document.createElement("input");

        answerInput.type = "text";
        answerInput.placeholder = "Type what you hear";


        const checkAnswerButton = document.createElement("button");
        checkAnswerButton.textContent = "Check Answer";
        checkAnswerButton.disabled = true;


        const answerResult = document.createElement("p");
        answerResult.id = `answer-result-${sentence.id}`;


        answerInput.addEventListener("focus", () => {           
            checkAnswerButton.disabled = false;
            onSentenceSelected(sentence);
        });


        checkAnswerButton.addEventListener("click", () => {
            onCheckAnswer(
                sentence,
                answerInput.value
            );
        });


        item.appendChild(sentenceInfo);
        item.appendChild(answerInput);
        item.appendChild(checkAnswerButton);
        item.appendChild(answerResult);

        list.appendChild(item);
    }
}


export function showAnswerResult(sentenceId, message) {
    const result = document.getElementById(
        `answer-result-${sentenceId}`
    );

    if (result) {
        result.textContent = message;
    }
}
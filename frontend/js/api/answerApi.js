const API_URL = "http://127.0.0.1:8000";


export async function checkAnswer(sessionId, sentenceId, answer) {
    const response = await fetch(
        `${API_URL}/sessions/${sessionId}/check`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                sentence_id: sentenceId,
                answer: answer
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Check answer failed"
        );
    }

    return data;
}

export async function getAnswer(sessionId, sentenceId) {
    const response = await fetch(
        `${API_URL}/sessions/${sessionId}/sentences/${sentenceId}/answer`
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Get answer failed"
        );
    }

    return data;
}
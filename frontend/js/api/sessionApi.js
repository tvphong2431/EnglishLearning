const API_URL = "http://127.0.0.1:8000";


export async function createSession(url) {
    const response = await fetch(`${API_URL}/sessions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            url: url
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Create session failed"
        );
    }
    
    return data;
}
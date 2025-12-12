const chatWindow = document.getElementById("chat-window");
const form = document.querySelector(".input-area");
const input = document.getElementById("user-input");

function addMessage(role, text) {
    const row = document.createElement("div");
    row.classList.add("message-row", role);

    const label = document.createElement("div");
    label.classList.add("label", role === "user" ? "user" : "bot");
    label.textContent = role === "user" ? "ME" : "MEDIBOT";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;

    row.appendChild(label);
    row.appendChild(bubble);

    chatWindow.appendChild(row);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userMsg = input.value.trim();
    if (!userMsg) return;

    addMessage("user", userMsg);
    input.value = "";

    // Call Flask backend
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg })
    });

    const data = await res.json();
    addMessage("bot", data.answer || "Sorry, something went wrong.");
});

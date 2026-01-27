import React, { useState } from "react";

function ChatUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;

    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    setMessages([...messages, { user: input, bot: data.reply }]);
    setInput("");
  };

  return (
    <div>
      <div style={{ height: 300, overflowY: "scroll", border: "1px solid gray", padding: "10px" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: "10px" }}>
            <b>You:</b> {m.user}<br />
            <b>Bot:</b> {m.bot}
          </div>
        ))}
      </div>

      <input
        style={{ width: "80%", marginRight: "10px" }}
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatUI;

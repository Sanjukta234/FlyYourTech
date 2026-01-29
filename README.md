# Fly Your Tech – AI Chatbot with Tool Calling (LangChain + LangGraph)

---

## 1. System Architecture

**Backend**: Python + FastAPI

* LangChain for LLM + tools
* LangGraph for agent workflow
* Gemini / OpenAI / any LLM API

**Frontend**: React.js

* Simple chat UI
* REST API to backend

Flow:
User (React) → FastAPI `/chat` → LangGraph Agent → Tool Selection → Tool Response → LLM Final Answer → Frontend

---

## 2. Knowledge Base (Tool 1 – Mandatory)

Create a JSON file: `data/knowledge_base.json`

```json
{
  "company_name": "Fly Your Tech",
  "address": "2nd Floor, Tech Park, Bengaluru, India",
  "phone": "+91-9876543210",
  "email": "contact@flyyourtech.com",
  "services": [
    "AI Solutions",
    "Web Development",
    "Mobile App Development",
    "Cloud Consulting",
    "Machine Learning Consulting"
  ],
  "starting_price": "₹25,000"
}
```

---

## 3. Lead Management DB (Tool 2 – Mandatory)

Create a JSON file: `data/leads.json`

```json
[]
```

Each lead format:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "service": "AI Solutions"
}
```

---

## 4. Backend – FastAPI + LangChain + LangGraph

### 4.1 Install Dependencies

```bash
pip install fastapi uvicorn langchain langgraph pydantic python-dotenv
```

---

## 4.2 Define Tools

`tools.py`

```python
import json
from langchain.tools import tool

# -------- Tool 1: Knowledge Base Tool --------
@tool
def knowledge_base_tool(query: str) -> str:
    """Fetch company-related information from knowledge base"""
    with open("data/knowledge_base.json", "r") as f:
        kb = json.load(f)

    query_lower = query.lower()

    if "name" in query_lower:
        return f"Company Name: {kb['company_name']}"
    if "address" in query_lower:
        return f"Address: {kb['address']}"
    if "phone" in query_lower or "contact number" in query_lower:
        return f"Phone: {kb['phone']}"
    if "email" in query_lower:
        return f"Email: {kb['email']}"
    if "service" in query_lower:
        return "Services: " + ", ".join(kb['services'])
    if "price" in query_lower or "cost" in query_lower:
        return f"Starting Price: {kb['starting_price']}"

    return "Sorry, I couldn't find that information."


# -------- Tool 2: Lead Management Tool --------
@tool
def lead_management_tool(name: str, email: str, service: str) -> str:
    """Store a new lead in the lead database"""
    with open("data/leads.json", "r") as f:
        leads = json.load(f)

    new_lead = {
        "name": name,
        "email": email,
        "service": service
    }

    leads.append(new_lead)

    with open("data/leads.json", "w") as f:
        json.dump(leads, f, indent=2)

    return f"Lead saved successfully for {name} regarding {service}."


# -------- Tool 3: Pricing Tool (Mandatory 3rd Tool) --------
@tool
def pricing_tool(service: str) -> str:
    """Return estimated pricing for a given service"""
    pricing = {
        "ai solutions": "₹50,000 onwards",
        "web development": "₹30,000 onwards",
        "mobile app development": "₹40,000 onwards",
        "cloud consulting": "₹35,000 onwards"
    }

    key = service.lower()
    if key in pricing:
        return f"Estimated price for {service}: {pricing[key]}"
    else:
        return "Please contact sales for a custom quote."
```

---

## 4.3 LangGraph Agent Setup

`agent.py`

```python
from langchain.chat_models import ChatOpenAI  # or Gemini wrapper
from langgraph.graph import StateGraph
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
from tools import knowledge_base_tool, lead_management_tool, pricing_tool

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [knowledge_base_tool, lead_management_tool, pricing_tool]

agent = create_openai_tools_agent(llm, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# LangGraph Wrapper
class AgentState(dict):
    pass

workflow = StateGraph(AgentState)

workflow.add_node("agent", lambda state: agent_executor.invoke({"input": state["input"]}))
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")

app_graph = workflow.compile()
```

---

## 4.4 FastAPI Server

`main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
from agent import app_graph

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = app_graph.invoke({"input": req.message})
    return {"response": result["output"]}
```

Run backend:

```bash
uvicorn main:app --reload
```

---

## 5. Frontend – React.js

### 5.1 Simple Chat UI

`App.js`

```jsx
import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    setMessages([...messages, { user: input, bot: data.response }]);
    setInput("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Fly Your Tech Chatbot</h2>

      <div style={{ height: 300, overflowY: "scroll", border: "1px solid #ccc", padding: 10 }}>
        {messages.map((m, i) => (
          <div key={i}>
            <p><b>You:</b> {m.user}</p>
            <p><b>Bot:</b> {m.bot}</p>
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
```

---

## 6. Example Queries (For Demo)

General Knowledge (Tool 1):

* "What services does Fly Your Tech offer?"
* "What is your starting price?"
* "Give me your contact email"

Pricing (Tool 3):

* "How much does web development cost?"

Lead Creation (Tool 2):

* "I want AI Solutions. My name is Rahul and my email is [rahul@gmail.com](mailto:rahul@gmail.com)"

---

## 7. Evaluation Checklist (Matches Assignment)

* Python backend ✔
* LangChain used ✔
* LangGraph workflow ✔
* 3 mandatory tools implemented ✔
* **Scheduling tool added (optional bonus)** ✔
* Automatic tool selection ✔
* React frontend ✔
* Company KB implemented ✔
* Lead management simulated ✔

---

## 8. Scheduling Tool (Tool 4 – Optional Enhancement)

This tool allows users to book a demo or consultation appointment.

### 8.1 Data File

Create a new file:

```
backend/data/appointments.json
```

```json
[]
```

---

## 8.2 Tool Implementation

Add to `backend/app/tools.py`:

```python
@tool
def scheduling_tool(name: str, email: str, date: str, time: str) -> str:
    """Schedule a demo or consultation appointment"""

    appointment = {
        "name": name,
        "email": email,
        "date": date,
        "time": time
    }

    try:
        with open("data/appointments.json", "r") as f:
            appointments = json.load(f)
    except FileNotFoundError:
        appointments = []

    appointments.append(appointment)

    with open("data/appointments.json", "w") as f:
        json.dump(appointments, f, indent=2)

    return f"Appointment scheduled for {name} on {date} at {time}."
```

---

## 8.3 Register Scheduling Tool in Agent

Update `backend/app/agent.py`:

```python
from tools import knowledge_base_tool, lead_management_tool, pricing_tool, scheduling_tool

tools = [
    knowledge_base_tool,
    lead_management_tool,
    pricing_tool,
    scheduling_tool
]
```

---

## 8.4 Example Scheduling Queries

* "Book a demo for me on 20th Feb at 3 PM. My name is Ankit and email is [ankit@gmail.com](mailto:ankit@gmail.com)"
* "Schedule a consultation tomorrow at 11 AM for Rahul, [rahul@gmail.com](mailto:rahul@gmail.com)"

The agent will automatically invoke `scheduling_tool` based on intent.

---

## 9. Optional Enhancements

* Add vector DB (FAISS) for KB
* Add tool for appointment scheduling ✔ (Implemented)
* Add logging of conversations
* Add UI styling

---

## 10. Project Folder Structure

* Python backend ✔
* LangChain used ✔
* LangGraph workflow ✔
* 3 tools implemented ✔
* Automatic tool selection ✔
* React frontend ✔
* Company KB implemented ✔
* Lead management simulated ✔

---

## 8. Optional Enhancements

* Add vector DB (FAISS) for KB
* Add tool for appointment scheduling
* Add logging of conversations
* Add UI styling

---

## 9. Project Folder Structure

Recommended clean structure for submission and demo:

```text
fly-your-tech-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI entry point
│   │   ├── agent.py             # LangGraph + Agent setup
│   │   ├── tools.py             # All 3 tools
│   │   ├── schemas.py           # Pydantic request/response models
│   │   └── config.py            # API keys, settings
│   │
│   ├── data/
│   │   ├── knowledge_base.json  # Company KB (Tool 1)
│   │   └── leads.json           # Lead DB (Tool 2)
│   │
│   ├── requirements.txt
│   ├── .env                    # API keys
│   └── README.md               # Backend instructions
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js              # Chat UI
│   │   ├── index.js
│   │   ├── api.js              # API helper
│   │   └── styles.css
│   ├── package.json
│   └── README.md               # Frontend instructions
│
├── docs/
│   ├── architecture.md         # System design explanation
│   └── demo_queries.md         # Sample queries for evaluation
│
├── .gitignore
├── README.md                  # Main project README
└── run.sh                     # Optional startup script
```

---

### Key Files Explained

* `backend/app/main.py` → FastAPI server
* `backend/app/agent.py` → LangGraph workflow
* `backend/app/tools.py` → Knowledge, Lead, Pricing tools
* `backend/data/` → All persistent data
* `frontend/src/App.js` → Chat interface
* `README.md` → Submission documentation

---

* Add vector DB (FAISS) for KB
* Add tool for appointment scheduling
* Add logging of conversations
* Add UI styling

---


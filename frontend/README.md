# Fly Your Tech – AI Chatbot with Tool Calling

This project is a **basic AI-powered business chatbot** built for the fictional company **“Fly Your Tech”**.
It demonstrates **tool calling**, **LangChain**, and **LangGraph-based orchestration** with a simple **React frontend** and **Python backend**.

---

##  Features

* Chatbot that answers company-related queries
* Automatic routing to different tools based on user intent
* Three tools implemented:

  1. Knowledge Base Tool (company info)
  2. Lead Management Tool (dummy lead database)
  3. Scheduling Tool (dummy meeting scheduler)
* Backend built with Flask + LangGraph
* Frontend built with React

---

## 🛠️ Tech Stack

### Backend

* Python 3.10+
* Flask
* LangChain
* LangGraph

### Frontend

* React.js
* Fetch API for backend communication

---

## 📁 Project Structure

```
fly-your-tech/
│
├── backend/
│   ├── app.py
│   ├── graph.py
│   ├── tools/
│   │   ├── knowledge_base.py
│   │   ├── leads.py
│   │   └── scheduler.py
│   └── data/
│       ├── company.json
│       └── leads.json
│
└── frontend/
    ├── package.json
    └── src/
        ├── App.js
        └── ChatUI.js
```

---

##  Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install flask flask-cors langchain langgraph
```

### 3. Run Backend Server

```bash
python3 app.py
```

Backend will start at:

```
http://localhost:5000
```

---

## 🌐 Frontend Setup

### 1. Go to Frontend Folder

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start React App

```bash
npm start
```

Frontend will open at:

```
http://localhost:3000
```

---

##  How Tool Calling Works

This project uses **LangGraph** to define a simple state-based agent workflow.

* The user query is passed into a **router node**.
* The router analyzes the query and decides which tool to invoke:

| Intent Type                   | Tool Used          |
| ----------------------------- | ------------------ |
| Company info, services, price | KnowledgeBaseTool  |
| Lead queries                  | LeadManagementTool |
| Meeting / scheduling          | SchedulerTool      |

The router node is implemented inside `graph.py` using a **StateGraph**.

---

##  Tools Implemented

### 1. Knowledge Base Tool

Returns:

* Company name
* Address
* Phone number
* Email
* Services offered
* Starting price

### 2. Lead Management Tool

* Reads from `leads.json`
* Can show all leads
* Can return details of a specific lead

### 3. Scheduling Tool

* Simulates meeting scheduling
* Returns a dummy confirmation message

---

##  Example Queries

Try these in the chat UI:

* `What services do you offer?`
* `What is your starting price?`
* `Show all leads`
* `Details of Rahul`
* `Schedule a meeting`

---

##  About LangGraph Usage

* A custom `AgentState` is defined with input and output fields.
* A `StateGraph` is created with a single router node.
* The router node performs intent routing and invokes the appropriate tool.

This demonstrates:

* State-based agent workflow
* Tool calling inside a LangGraph node
* Modular and extensible agent design

---

##  For Demo / Loom Explanation

Key points to explain:

* Use of LangGraph for orchestration
* Tool-based routing architecture
* Separation of tools and routing logic
* Frontend–backend integration

---

##  Notes

* The routing logic is rule-based for stability and to avoid API limitations.
* The architecture is designed to support LLM-based routing in future upgrades.

---

##  Author

Developed as an academic project to demonstrate:

* LangChain
* LangGraph
* Tool Calling
* Full-stack chatbot architecture

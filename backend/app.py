from flask import Flask, request, jsonify
from graph import run_agent
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    response = run_agent(user_message)
    return jsonify({"reply": response})


@app.route("/", methods=["GET"])
def home():
    return "Fly Your Tech Chatbot Backend is Running"


if __name__ == "__main__":
    app.run(debug=True)
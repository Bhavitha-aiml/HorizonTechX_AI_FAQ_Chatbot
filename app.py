from flask import Flask, render_template_string, request
from chatbot import FAQChatbot

app = Flask(__name__)
chatbot = FAQChatbot()

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>FAQ Chatbot</title>
  <style>
    :root { --bg: #0f172a; --panel: #ffffff; --accent: #2563eb; --accent-2: #38bdf8; --text: #0f172a; --muted: #64748b; --user: #dbeafe; --bot: #ecfdf5; }
    * { box-sizing: border-box; }
    body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; min-height: 100vh; background: radial-gradient(circle at top left, #1d4ed8, #0f172a 70%); color: var(--text); display: flex; align-items: center; justify-content: center; padding: 24px; }
    .container { width: 100%; max-width: 800px; background: rgba(255,255,255,0.96); backdrop-filter: blur(10px); border-radius: 24px; padding: 28px; box-shadow: 0 20px 45px rgba(0,0,0,0.25); }
    .header { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 18px; }
    .badge { background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: white; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
    h2 { margin: 0 0 6px; color: #1e3a8a; font-size: 28px; }
    .subtitle { margin: 0; color: var(--muted); }
    form { display: flex; gap: 10px; margin: 18px 0 20px; }
    input[type=text] { flex: 1; padding: 13px 14px; border: 1px solid #cbd5e1; border-radius: 12px; font-size: 15px; outline: none; }
    input[type=text]:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
    button { padding: 13px 16px; border: none; border-radius: 12px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: white; cursor: pointer; font-weight: 600; }
    button:hover { transform: translateY(-1px); }
    .chat { border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; background: linear-gradient(180deg, #f8fbff, #fefefe); }
    .message { margin-bottom: 12px; }
    .label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
    .user-label { color: var(--accent); }
    .bot-label { color: #15803d; }
    .bubble { padding: 12px 14px; border-radius: 12px; line-height: 1.5; }
    .user-bubble { background: var(--user); color: #1e3a8a; }
    .bot-bubble { background: var(--bot); color: #166534; }
    .hint { color: var(--muted); font-size: 14px; margin: 8px 0 0; }
    @media (max-width: 600px) { form { flex-direction: column; } button { width: 100%; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <div class="badge">AI FAQ Assistant</div>
        <h2>Smart FAQ Chatbot</h2>
        <p class="subtitle">Ask questions about support, AI, data science, and more.</p>
      </div>
    </div>
    <form method="post">
      <input type="text" name="question" placeholder="Ask a question" value="{{ question }}" required>
      <button type="submit">Send</button>
    </form>
    <div class="chat">
      {% if question %}
        <div class="message">
          <div class="label user-label">You</div>
          <div class="bubble user-bubble">{{ question }}</div>
        </div>
        <div class="message">
          <div class="label bot-label">Bot</div>
          <div class="bubble bot-bubble">{{ answer }}</div>
        </div>
      {% else %}
        <p class="hint">Try: How do I reset my password? or What is AI?</p>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        answer = chatbot.generate_response(question)
    return render_template_string(HTML, question=question, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)

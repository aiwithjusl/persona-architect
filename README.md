<p align="center">
  <img src="images/persona-architect-banner.png" alt="Persona Architect Banner" width="100%" />
</p>

# Persona Architect

🧠 Simulate intelligent AI personas with modular, prompt-based architecture using Python + NLP.

## 🔍 Features

Persona Architect allows you to:
- Define AI personalities in a JSON config
- Simulate realistic responses using OpenAI (or stub logic)
- Track and save full conversations with memory
- Use for coaching, writing, training, or prototyping AI agents

## 📂 Project Structure

- `main.py` – CLI runner  
- `persona_config.json` – Persona definitions  
- `prompt_builder.py` – Prompt construction logic  
- `memory.py` – Tracks user + AI dialogue history  
- `response_handler.py` – Handles AI or mock responses  
- `session_saver.py` – Saves session logs to timestamped file  
- `templates/` – Prompt templates used per persona  

## 🛠 Requirements

To run with OpenAI API (optional):

```bash
pip install openai

🚀 How to Run

▶️ Offline Mode (Default)

No setup required — runs in stubbed mode with preset AI responses:

python main.py

Type your message and see your persona respond.
Type exit or quit to end the session and auto-save your chat log.


---

🌐 Live OpenAI Mode (Optional)

1. Create a config.py file in the project root:

OPENAI_API_KEY = "your-openai-api-key-here"

2. In response_handler.py, set:

USE_OPENAI = True

3. Run the app again:

python main.py

 ⚠️ Important: Do not share or upload your API key publicly. Keep it local and secure.




---

📄 License

MIT – Free to use and extend.

---

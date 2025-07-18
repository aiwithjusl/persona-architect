"""
main.py

Main CLI interface for Persona Architect.
- Loads a persona from JSON config
- Builds a dynamic AI prompt
- Sends prompt to AI response handler
- Tracks conversation history
- Saves the session log on exit
- Supports mid-chat persona switching via "/switch <name>"
- Supports manual save with "/save"
- Displays current conversation history with "/history"
- Clears memory mid-chat with "/reset"
- Lists all available personas with "/list"
- Displays help menu with "/help"
"""

import json
from prompt_builder import build_prompt
from memory import Memory
from session_saver import save_session
from response_handler import get_response
from config_loader import load_persona

# === Load all personas from persona_config.json for listing ===
def list_personas():
    with open("persona_config.json", "r") as f:
        config = json.load(f)
    return list(config.keys())

# === Main Chat Loop ===
if __name__ == "__main__":
    persona = load_persona("default")
    memory = Memory()

    while True:
        user_input = input("You: ").strip()

        # 🚪 Exit chat and save session
        if user_input.lower() in ["exit", "quit"]:
            save_session(persona["name"], memory)
            break

        # 🔄 Mid-chat persona switching
        if user_input.lower().startswith("/switch "):
            new_persona_name = user_input.split(" ", 1)[1].strip()
            new_persona = load_persona(new_persona_name)

            save_session(persona["name"], memory)  # Save previous session
            memory = Memory()  # Start fresh memory for new persona
            persona = new_persona

            print(f"\n🔄 Persona switched to: {persona['name']}\n")
            continue

        # 💾 Manual save
        if user_input.lower() == "/save":
            save_session(persona["name"], memory)
            print("✅ Session saved.\n")
            continue

        # 📜 Show chat history
        if user_input.lower() == "/history":
            print("\n📜 Conversation History:")
            for entry in memory.history:
                print(f"{entry['speaker']}: {entry['message']}")
            print()
            continue

        # 🔁 Reset conversation memory
        if user_input.lower() == "/reset":
            memory = Memory()
            print("🧼 Conversation memory cleared.\n")
            continue

        # 📋 List all available personas
        if user_input.lower() == "/list":
            personas = list_personas()
            print("\n📋 Available Personas:")
            for p in personas:
                print(f" - {p}")
            print()
            continue

        # 🆘 Help command
        if user_input.lower() == "/help":
            print("""
🛠 Available Commands:
/help          – Show this help menu
/exit or /quit – Exit the chat and save session
/save          – Manually save current session
/history       – View current conversation history
/reset         – Clear conversation memory
/switch <name> – Switch to another persona
/list          – List all available personas
""")
            continue

        # 🧠 Generate AI response
        prompt = build_prompt(persona, user_input)
        response = get_response(prompt)

        # 🗂 Save conversation in memory
        memory.add("You", user_input)
        memory.add(persona["name"], response)

        # 🖨 Show AI response
        print(f"\n{persona['name']}: {response}\n")

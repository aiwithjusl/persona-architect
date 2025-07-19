import json
from prompt_builder import build_prompt
from memory import Memory
from session_saver import save_session
from response_handler import get_response
from config_loader import load_persona
from log_importer import import_log  # ✅ NEW import

# === Optional Autosave ===
AUTOSAVE = False

# === Load all personas from persona_config.json for listing ===
def list_personas():
    with open("persona_config.json", "r") as f:
        config = json.load(f)
    return {k: v["description"] for k, v in config.items()}

def load_all_personas_raw():
    with open("persona_config.json", "r") as f:
        return json.load(f)

# === Manage persona switching and memory ===
class PersonaManager:
    def __init__(self, initial_persona_name="default"):
        self.personas = {}
        self.memories = {}
        self.current_key = initial_persona_name.lower()
        self.current_persona = self.load(self.current_key)

    def load(self, persona_name):
        persona_name = persona_name.lower()
        persona = load_persona(persona_name)
        if persona_name not in self.memories:
            self.memories[persona_name] = Memory()
        self.personas[persona_name] = persona
        self.current_key = persona_name
        return persona

    def switch(self, persona_name):
        save_session(self.current_persona["name"], self.memory)
        self.current_persona = self.load(persona_name)
        print(f"\n🔄 Persona switched to: {self.current_persona['name']}\n")

    @property
    def memory(self):
        return self.memories[self.current_key]

# === Run interactive chat ===
def main():
    manager = PersonaManager()

    while True:
        user_input = input(f"[{manager.current_persona['name']}] You: ").strip()

        # 🚪 Exit
        if user_input.lower() in ["exit", "quit"]:
            save_session(manager.current_persona["name"], manager.memory)
            break

        # 🔄 Switch persona
        if user_input.lower().startswith("/switch "):
            new_name = user_input.split(" ", 1)[1].strip()
            manager.switch(new_name)
            continue

        # 💾 Save session
        if user_input.lower() == "/save":
            save_session(manager.current_persona["name"], manager.memory)
            print("✅ Session saved.\n")
            continue

        # 📜 View history
        if user_input.lower() == "/history":
            print(f"\n📜 Conversation History ({manager.current_persona['name']}):")
            for entry in manager.memory.history:
                print(f"{entry['speaker']}: {entry['message']}")
            print()
            continue

        # 🧼 Reset memory
        if user_input.lower() == "/reset":
            manager.memories[manager.current_key] = Memory()
            print(f"🧼 Memory reset for: {manager.current_persona['name']}\n")
            continue

        # 📋 List personas
        if user_input.lower() == "/list":
            print("\n📋 Available Personas:")
            for key, desc in list_personas().items():
                print(f" - {key}: {desc}")
            print()
            continue

        # 🔍 View persona traits
        if user_input.lower().startswith("/traits"):
            parts = user_input.strip().split(" ", 1)
            raw = load_all_personas_raw()

            if len(parts) == 2:
                name = parts[1].strip().lower()
                if name in raw:
                    print(f"\n🧬 Traits for '{name}':")
                    for key, val in raw[name].items():
                        print(f"{key.capitalize()}: {val}")
                    print()
                else:
                    print(f"❌ Persona '{name}' not found.\n")
            else:
                print(f"\n🧬 Traits for current persona ({manager.current_persona['name']}):")
                for key, val in manager.current_persona.items():
                    print(f"{key.capitalize()}: {val}")
                print()
            continue

        # 📥 Import log (placeholder)
        if user_input.lower().startswith("/importlog "):
            path = user_input.split(" ", 1)[1].strip()
            import_log(manager.current_persona["name"], manager.memory, path)
            continue

        # 🔁 Reload persona config
        if user_input.lower() == "/reload":
            manager.personas = {}
            manager.current_persona = manager.load(manager.current_key)
            print("🔁 Persona configuration reloaded.\n")
            continue

        # 🆘 Help
        if user_input.lower() == "/help":
            print("""
🛠 Available Commands:
/help           – Show this help menu
/exit or /quit  – Exit and save session
/save           – Save current session
/history        – View conversation history
/reset          – Reset memory for current persona
/switch <name>  – Switch to another persona
/list           – Show available personas
/traits [name]  – View current or specific persona's full traits
/importlog <file_path> – (Future) Import conversation log to memory
/reload         – Reload persona_config.json live
""")
            continue

        # 🧠 Respond
        prompt = build_prompt(manager.current_persona, user_input)
        response = get_response(prompt)
        manager.memory.add("You", user_input)
        manager.memory.add(manager.current_persona["name"], response)

        if AUTOSAVE:
            save_session(manager.current_persona["name"], manager.memory)
            print("💾 Autosaved.\n")

        print(f"\n{manager.current_persona['name']}: {response}\n")

if __name__ == "__main__":
    main()

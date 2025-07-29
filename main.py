import json
import traceback
from prompt_builder import build_prompt
from memory import Memory
from session_saver import save_session
from response_handler import get_response
from config_loader import load_persona
from log_importer import parse_log_file

AUTOSAVE = False
AUTOSAVE_SUMMARY = False  # ✅ New toggle flag


def list_personas():
    try:
        with open("persona_config.json", "r") as f:
            config = json.load(f)
        return {k: v["description"] for k, v in config.items()}
    except Exception as e:
        print(f"❌ Failed to list personas: {e}")
        traceback.print_exc()
        return {}


def load_all_personas_raw():
    try:
        with open("persona_config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load raw persona config: {e}")
        traceback.print_exc()
        return {}


class PersonaManager:
    def __init__(self, initial_persona_name="default"):
        self.personas = {}
        self.memories = {}
        self.current_key = initial_persona_name.lower()
        self.current_persona = self.load(self.current_key)

    def load(self, persona_name):
        try:
            persona_name = persona_name.lower()
            persona = load_persona(persona_name)
            if persona_name not in self.memories:
                self.memories[persona_name] = Memory()
            self.personas[persona_name] = persona
            self.current_key = persona_name
            return persona
        except Exception as e:
            print(f"❌ Failed to load persona '{persona_name}': {e}")
            traceback.print_exc()
            return {"name": "Unknown", "description": "Failed to load persona", "template": "default.txt"}

    def switch(self, persona_name):
        try:
            save_session(self.current_persona["name"], self.memory)
            self.current_persona = self.load(persona_name)
            print(f"\n🔄 Persona switched to: {self.current_persona['name']}\n")
        except Exception as e:
            print(f"❌ Failed to switch persona: {e}")
            traceback.print_exc()

    def edit_trait(self, trait, value):
        if trait in self.current_persona:
            self.current_persona[trait] = value
            print(f"✏️ Trait '{trait}' updated to: {value}\n")
        else:
            print(f"❌ Trait '{trait}' not found in current persona.\n")

    def revert_traits(self):
        try:
            updated = load_persona(self.current_key)
            self.current_persona = updated
            self.personas[self.current_key] = updated
            print(f"🔁 Reverted traits for '{self.current_key}' to saved state.\n")
        except Exception as e:
            print(f"❌ Failed to revert traits: {e}")
            traceback.print_exc()

    @property
    def memory(self):
        return self.memories[self.current_key]


def diff_traits(saved, current):
    added = {k: v for k, v in current.items() if k not in saved}
    removed = {k: v for k, v in saved.items() if k not in current}
    modified = {
        k: (saved[k], current[k])
        for k in saved if k in current and saved[k] != current[k]
    }
    return added, removed, modified


def main():
    manager = PersonaManager()

    while True:
        try:
            user_input = input(f"[{manager.current_persona['name']}] You: ").strip()
        except KeyboardInterrupt:
            print("\n👋 Exiting via keyboard interrupt. Saving session...")
            save_session(manager.current_persona["name"], manager.memory)
            break

        if user_input.lower() in ["exit", "quit", "/exit", "/quit"]:
            print("👋 Exiting. Saving session...")
            save_session(manager.current_persona["name"], manager.memory)
            break

        try:
            # ==== Settings ====
            if user_input.lower() == "/autosave_summary":
                global AUTOSAVE_SUMMARY
                AUTOSAVE_SUMMARY = not AUTOSAVE_SUMMARY
                print(f"📝 Summary autosave {'enabled' if AUTOSAVE_SUMMARY else 'disabled'}.\n")

            # ==== Persona Management ====
            elif user_input.lower().startswith("/switch "):
                manager.switch(user_input.split(" ", 1)[1].strip())

            elif user_input.lower() == "/list":
                print("\n📋 Available Personas:")
                for key, desc in list_personas().items():
                    print(f" - {key}: {desc}")
                print()

            elif user_input.lower().startswith("/traits edit "):
                try:
                    _, _, body = user_input.partition("edit ")
                    trait, value = map(str.strip, body.split("=", 1))
                    manager.edit_trait(trait.lower(), value)
                except Exception as e:
                    print(f"❌ Failed to edit trait: {e}")
                    traceback.print_exc()

            elif user_input.lower() == "/traits save":
                try:
                    data = load_all_personas_raw()
                    data[manager.current_key] = manager.current_persona
                    with open("persona_config.json", "w") as f:
                        json.dump(data, f, indent=2)
                    print(f"💾 Traits saved for '{manager.current_persona['name']}'.\n")
                except Exception as e:
                    print(f"❌ Failed to save traits: {e}")
                    traceback.print_exc()

            elif user_input.lower() == "/traits revert":
                manager.revert_traits()

            elif user_input.lower() == "/traits diff":
                try:
                    saved = load_persona(manager.current_key)
                    current = manager.current_persona
                    added, removed, modified = diff_traits(saved, current)

                    print(f"\n🔍 Trait differences for '{manager.current_key}':\n")
                    if added:
                        print("➕ Added Traits:")
                        for k, v in added.items():
                            print(f"  - {k}: {v}")
                    if removed:
                        print("\n❌ Removed Traits:")
                        for k, v in removed.items():
                            print(f"  - {k}: {v}")
                    if modified:
                        print("\n🔧 Modified Traits:")
                        for k, (old, new) in modified.items():
                            print(f"  - {k}: {old} → {new}")
                    if not (added or removed or modified):
                        print("✅ No differences found. Traits are identical.\n")
                    print()
                except Exception as e:
                    print(f"❌ Failed to diff traits: {e}")
                    traceback.print_exc()

            elif user_input.lower().startswith("/traits"):
                try:
                    parts = user_input.strip().split(" ", 1)
                    raw = load_all_personas_raw()
                    name = parts[1].strip().lower() if len(parts) == 2 else manager.current_key
                    if name in raw:
                        print(f"\n🧬 Traits for '{name}':")
                        for k, v in raw[name].items():
                            print(f"{k.capitalize()}: {v}")
                        print()
                    else:
                        print(f"❌ Persona '{name}' not found.\n")
                except Exception as e:
                    print(f"❌ Failed to load traits: {e}")
                    traceback.print_exc()

            # ==== Memory ====
            elif user_input.lower() == "/save":
                save_session(manager.current_persona["name"], manager.memory)
                print("✅ Session saved.\n")

            elif user_input.lower() == "/reset":
                manager.memories[manager.current_key] = Memory()
                print(f"🧼 Memory reset for: {manager.current_persona['name']}\n")

            elif user_input.lower() == "/history":
                print(f"\n📜 Conversation History ({manager.current_persona['name']}):")
                for entry in manager.memory.history:
                    if isinstance(entry, dict) and "speaker" in entry and "message" in entry:
                        print(f"{entry['speaker']}: {entry['message']}")
                    else:
                        print(f"⚠️ Skipping malformed entry: {entry}")
                print()

            elif user_input.lower().startswith("/history filter "):
                keyword = user_input.split(" ", 2)[2].strip().lower()
                matches = 0
                print(f"\n📜 Filtered History for '{keyword}':")
                for entry in manager.memory.history:
                    if isinstance(entry, dict) and keyword in (entry["speaker"] + entry["message"]).lower():
                        print(f"{entry['speaker']}: {entry['message']}")
                        matches += 1
                print(f"\n✅ {matches} entries matched.\n" if matches else f"❌ No entries found.\n")

            elif user_input.lower() == "/history count":
                valid = [e for e in manager.memory.history if isinstance(e, dict) and "speaker" in e and "message" in e]
                print(f"🧮 Total valid conversation entries: {len(valid)}\n")

            elif user_input.lower() == "/summary":
                print("📡 Generating summary of conversation...")
                context = manager.memory.get_context()
                if not context.strip():
                    print("⚠️ No messages to summarize.\n")
                    continue
                try:
                    summary = get_response(
                        f"System: You are a helpful assistant summarizing a conversation.\n"
                        "Task: Summarize the following conversation clearly, focusing on major points and tone.\n"
                        f"Conversation:\n{context}"
                    )
                    print("\n📌 Conversation Summary:\n" + summary + "\n")
                    if AUTOSAVE_SUMMARY:
                        file_name = f"{manager.current_persona['name']}_summary.txt"
                        with open(file_name, "a", encoding="utf-8") as f:
                            f.write(f"\n==== Summary ({manager.current_persona['name']}): ====\n{summary}\n")
                        print(f"💾 Summary saved to '{file_name}'\n")
                except Exception as e:
                    print(f"❌ Failed to generate summary: {e}")
                    traceback.print_exc()

            elif user_input.lower() == "/context":
                print("\n🧠 Conversation Context Overview:")
                try:
                    context = manager.memory.get_context_summary()
                    print(context if context else "⚠️ No context available yet.")
                except Exception as e:
                    print(f"❌ Failed to get context summary: {e}")
                    traceback.print_exc()
                print()

            # ==== Config ====
            elif user_input.lower() == "/reload":
                try:
                    manager.current_persona = manager.load(manager.current_key)
                    print(f"🔄 Reloaded configuration for '{manager.current_key}'.\n")
                except Exception as e:
                    print(f"❌ Failed to reload config: {e}")
                    traceback.print_exc()

            elif user_input.lower().startswith("/importlog "):
                try:
                    path = user_input.split(" ", 1)[1].strip()
                    confirm = input(f"📄 Importing log from '{path}'. Proceed? (y/n): ").strip().lower()
                    if confirm != "y":
                        print("❌ Import canceled.\n")
                        continue
                    entries = parse_log_file(path)
                    count = sum(1 for e in entries if "speaker" in e and "message" in e)
                    for e in entries:
                        manager.memory.add(e["speaker"], e["message"])
                    print(f"✅ Imported {count} log entries into memory.\n")
                except Exception as e:
                    print(f"❌ Failed to import log: {e}")
                    traceback.print_exc()

            elif user_input.lower() == "/help":
                print("""
📖 Help Menu – Available Commands

💡 Basics:
  /help                    – Show this help menu
  /exit or /quit           – Exit and save session
  /save                    – Save current session
  /reload                  – Reload current persona's config
  /autosave_summary        – Toggle automatic saving of summaries

🧠 Conversation Memory:
  /history                 – View full conversation history
  /history filter <term>   – Filter history by keyword
  /history count           – Count valid conversation entries
  /reset                   – Reset memory for current persona
  /summary                 – Summarize conversation using AI
  /context                 – Show recent conversation context

🧬 Persona Management:
  /list                    – List available personas
  /switch <name>           – Switch to another persona
  /traits                  – View traits of current persona
  /traits <name>           – View traits of specified persona
  /traits edit <k> = <v>   – Edit a trait in current persona
  /traits save             – Save current trait changes
  /traits revert           – Revert to saved traits
  /traits diff             – Show trait differences vs saved state

📁 Log Management:
  /importlog <file_path>   – Import a conversation log file
""")

            # ==== Message Processing ====
            else:
                prompt = build_prompt(manager.current_persona, user_input)
                response = get_response(prompt)
                manager.memory.add("You", user_input)
                manager.memory.add(manager.current_persona["name"], response)

                if AUTOSAVE:
                    save_session(manager.current_persona["name"], manager.memory)
                    print("💾 Autosaved.\n")

                print(f"\n{manager.current_persona['name']}: {response}\n")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()

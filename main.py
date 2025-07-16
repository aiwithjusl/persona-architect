"""
main.py

Main CLI interface for Persona Architect.
- Loads a persona from JSON config
- Builds a dynamic AI prompt
- Sends prompt to AI response handler
- Tracks conversation history
- Saves the session log on exit
"""

import json
from prompt_builder import build_prompt
from memory import Memory
from session_saver import save_session
from response_handler import get_response  # Now moved to dedicated file

# === Persona Loader ===
def load_persona(persona_name="default"):
    """
    Loads persona data from 'persona_config.json'.
    If specified persona is not found, fallback to 'default'.
    """
    with open("persona_config.json", "r") as f:
        config = json.load(f)
    if persona_name in config:
        return config[persona_name]
    else:
        print(f"[!] Persona '{persona_name}' not found. Loading default...")
        return config["default"]

# === Main Chat Loop ===

if __name__ == "__main__":
    # Load default persona
    persona = load_persona("default")
    memory = Memory()  # Track the full dialogue history

    # Start interactive chat loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            save_session(persona["name"], memory)  # Save log on exit
            break

        prompt = build_prompt(persona, user_input)  # Construct full AI prompt
        response = get_response(prompt)             # Get AI-generated response

        # Add both user and AI message to memory
        memory.add("You", user_input)
        memory.add(persona["name"], response)

        # Print AI response
        print(f"\n{persona['name']}: {response}\n")
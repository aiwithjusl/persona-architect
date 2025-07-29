# prompt_builder.py

def build_prompt(persona, user_input):
    """
    Loads the template file defined in the persona and replaces {{input}} with user input.
    Falls back to default.txt if the specified template is missing.
    """
    template_file = persona.get("template", "default.txt")

    try:
        with open(f"templates/{template_file}", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"[!] Template '{template_file}' not found. Falling back to default.")
        try:
            with open("templates/default.txt", "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            print("[!] Fallback template 'default.txt' not found. Using empty template.")
            template = ""

    return template.replace("{{input}}", user_input)

def build_prompt(persona, user_input):
    template_file = persona.get("template", "default.txt")
    try:
        with open(f"templates/{template_file}", "r") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"[!] Template '{template_file}' not found. Falling back to default.")
        with open("templates/default.txt", "r") as f:
            template = f.read()

    return template.replace("{{input}}", user_input)

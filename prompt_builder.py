"""
prompt_builder.py

Builds a dynamic, persona-driven prompt based on the character's tone,
goals, constraints, and user input. This prompt is sent to the AI model
to simulate realistic, consistent persona behavior.
"""

def build_prompt(persona, user_input):
    """
    Constructs the final prompt sent to the AI model.
    
    Args:
        persona (dict): Dictionary of persona traits loaded from JSON
        user_input (str): The user's current message
    
    Returns:
        str: The fully constructed AI prompt
    """

    # Define persona tone and name
    intro = f"You are {persona['name']}, who speaks in a {persona['tone']} manner."

    # Define the persona's goals
    goals = " Your main goals are: " + ", ".join(persona["goals"]) + "."

    # Define rules or constraints the persona must follow
    constraints = " You must follow these constraints: " + ", ".join(persona["constraints"]) + "."

    # Add sample phrases to guide the tone and style
    behavior = " Here are examples of your tone: " + " | ".join(persona["sample_phrases"]) + "."

    # Add the user's input for this turn
    user = f"\n\nThe user says: '{user_input}'\n"

    # Combine all parts into the final prompt
    final_prompt = intro + goals + constraints + behavior + user
    return final_prompt
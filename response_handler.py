# response_handler.py

"""
Handles response generation for Persona Architect.

Supports:
- Stubbed offline responses for testing
- OpenAI API responses for production use

Toggle `USE_OPENAI` to enable/disable API usage.
"""

USE_OPENAI = False  # 🔁 Safe to keep off for development/testing

def get_response(prompt):
    """
    Returns a response using either the OpenAI API or a stubbed fallback.

    Args:
        prompt (str): The full prompt to send to the model.

    Returns:
        str: The generated response.
    """
    try:
        return get_openai_response(prompt) if USE_OPENAI else get_stubbed_response(prompt)
    except Exception as e:
        print(f"[!] Error in get_response(): {e}")
        return "⚠️ An error occurred while generating the response."

def get_stubbed_response(prompt):
    """
    Fallback stubbed response logic for offline testing or demos.

    Args:
        prompt (str): The full prompt string.

    Returns:
        str: Hardcoded response based on prompt content.
    """
    try:
        prompt_lower = prompt.lower()
        if "science" in prompt_lower:
            return "🔬 Based on scientific reasoning, we would need to test this with controlled variables."
        elif "story" in prompt_lower or "once upon a time" in prompt_lower:
            return "📖 Once upon a time, a curious mind asked a bold question, and a journey began..."
        elif "minimal" in prompt_lower or "short" in prompt_lower:
            return "✔️ Yes."
        elif "friend" in prompt_lower or "happy" in prompt_lower:
            return "😊 I'm here for you! What can I do to brighten your day?"
        else:
            return "🌿 Let’s take a moment to breathe. What would help you feel more at ease right now?"
    except Exception as e:
        print(f"[!] Error in get_stubbed_response(): {e}")
        return "⚠️ An error occurred in the offline response system."

def get_openai_response(prompt):
    """
    Sends the prompt to OpenAI's Chat API and returns the AI's response.

    ⚠️ Requires:
        - Internet connection
        - A valid OpenAI API key (from config.py)

    Args:
        prompt (str): The prompt to send to the model.

    Returns:
        str: The response from OpenAI.
    """
    try:
        import openai
        from config import OPENAI_API_KEY  # 🔐 Secure API key management

        openai.api_key = OPENAI_API_KEY

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )

        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[!] OpenAI API error: {e}")
        return "⚠️ An error occurred while contacting the OpenAI API."

"""
response_handler.py

Handles response generation for Persona Architect.
Supports both:
- Offline stubbed response mode (for testing or demo use)
- OpenAI API integration (for live LLM responses)

Toggle `USE_OPENAI` to switch between modes.
"""

# Toggle to True if using OpenAI's live API
USE_OPENAI = False  # 🔁 Safe to keep off for development

def get_response(prompt):
    """
    Returns a response from either OpenAI or a stubbed fallback.
    
    Args:
        prompt (str): The full prompt built from persona traits + user input
    
    Returns:
        str: AI-generated or stubbed response
    """
    try:
        if USE_OPENAI:
            return get_openai_response(prompt)
        else:
            return get_stubbed_response(prompt)
    except Exception as e:
        print(f"[!] Error in get_response(): {e}")
        return "⚠️ An error occurred while generating the response."

def get_stubbed_response(prompt):
    """
    Stubbed (hardcoded) fallback response.
    Useful for offline testing or demonstration.
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
    Sends the constructed prompt to the OpenAI Chat API and returns the AI's response.
    
    ⚠️ Note:
        - Requires an internet connection
        - API key is securely loaded from config.py
        - In production, replace with environment-based loading or secure key vault
    """
    try:
        import openai
        from config import OPENAI_API_KEY  # 🔐 Centralized API key management

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
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"[!] OpenAI API error: {e}")
        return "⚠️ An error occurred while contacting the OpenAI API."

"""
memory.py

Handles conversation history by storing user and persona messages.
Used to simulate memory during multi-turn dialogues and to support
session saving at the end of the interaction.
"""

class Memory:
    def __init__(self):
        # Initialize an empty list to store the dialogue history
        self.history = []

    def add(self, speaker, message):
        """
        Add a message to memory from the specified speaker.
        Example: 'You: Hello there.'
        """
        self.history.append(f"{speaker}: {message}")

    def get_context(self):
        """
        Return the full conversation as a single string,
        formatted line by line in historical order.
        """
        return "\n".join(self.history)

    def clear(self):
        """
        Clear all stored conversation history.
        Useful for resetting between sessions or personas.
        """
        self.history = []

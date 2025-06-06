"""
Text-to-Speech Converter
Author: Gaurav Pandey
"""

import pyttsx3

# Initialize the text-to-speech engine
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing the text-to-speech engine: {e}")
    raise  # Re-raise the exception for further handling if needed

# Function to set voice and speed, and speak the given text
def speak(text):
    """
    Speaks the provided text using the text-to-speech engine.
    
    Parameters:
    text (str): The text to be spoken.
    
    Raises:
    ValueError: If the input text is empty or not a string.
    """
    # Validate the input text
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input must be a non-empty string.")

    try:
        # Set properties before adding anything to speak
        # Change the speech rate (words per minute)
        rate = engine.getProperty('rate')  # Get current speech rate
        engine.setProperty('rate', rate - 10)  # Decrease the rate by 10

        # Change the voice (0 for male, 1 for female)
        voices = engine.getProperty('voices')  # Get available voices
        if voices:
            engine.setProperty('voice', voices[0].id)  # Set to the first available voice
        else:
            print("No voices available. Using default voice.")

        # Speak the provided text
        engine.say(text)  # Queue the text to be spoken
        engine.runAndWait()  # Wait until the speaking is finished

    except Exception as e:
        print(f"An error occurred while trying to speak: {e}")
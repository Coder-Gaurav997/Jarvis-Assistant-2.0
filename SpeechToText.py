"""
Speech Recognition Module
Author: Gaurav Pandey
"""

import speech_recognition as sr

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def speech_to_text():
    """
    Convert speech from the microphone to text using Google Speech Recognition.
    
    Parameters:
    language (str): The language code for the speech recognition (default is 'en-US').
    
    Returns:
    str or None: The recognized text if successful, None if there was an error.
    """
    with sr.Microphone() as source:  # Use the default microphone as the audio source
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise to improve recognition accuracy
        audio = recognizer.listen(source)  # Listen for audio 
        
        try:
            # Use Google Speech Recognition to convert audio to text
            text = recognizer.recognize_google(audio)  
            return text  # Return the recognized text
        except sr.UnknownValueError:
            # Handle the case where speech is unintelligible
            print("Could Not Understand Audio")
            return None
        except sr.RequestError:
            # Handle errors related to the Google Speech Recognition service
            print(f"Internet Not Connected!")
            return None
        except Exception as e:
            # Handle any other exceptions that may occur
            print(f"An error occurred: {e}")
            return None
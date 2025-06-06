"""
Jarvis 2.0 Voice/Text Assistant
Author: Gaurav Pandey
"""

import os
import Brain
import SpeechToText as stt
import TextToSpeech as tts
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

def main():
    """
    Main function to run the Jarvis voice assistant.
    It initializes the assistant, listens for user input, and provides responses.
    """
    os.system('cls')  # Clear the terminal screen
    print(Fore.GREEN + Style.BRIGHT + "Initialising Jarvis 2.0...")  # Print initialization message
    print(Fore.GREEN + Style.BRIGHT + "--------------------------")
    tts.speak("Initialising Jarvis!")  # Use text-to-speech to announce initialization

    while True:
        way = input(Fore.CYAN + Style.BRIGHT + "How Do You Want To Use Jarvis 2.0? Voice(V) or Text(T):- ")  # Prompt user for input to use Jarvis
        if way.lower() == 't' or way.lower() == 'v':
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Please Enter A Valid Choice!\n")

    while True:
        try:
            if way.lower() == 't':
                text = input(Style.RESET_ALL + "\nGaurav: ")  # Get user input as text

            elif way.lower() == 'v':
                print(Style.RESET_ALL + "\nListening...")  # Indicate that the assistant is listening
                text = stt.speech_to_text()  # Capture speech input and convert it to text
                
                if text is None:
                    # If no text was recognized, continue listening
                    continue
            
                print(f"Gaurav: {text}")  # Print the recognized text (user input)

            Response = Brain.main(text)  # Get the response from the model based on user input
            print(f"Jarvis: {Response}")  # Print the response from the assistant
            tts.speak(Response)  # Use text-to-speech to speak the response
        except KeyboardInterrupt:
            continue

# Entry point of the program
if __name__ == "__main__":
    main()  # Run the main function
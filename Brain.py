"""
AI Query Classification and Response System
Author: Gaurav Pandey
"""

from groq import Groq
from dotenv import dotenv_values
import SpeechToText as stt
import TextToSpeech as tts
import ChatBot
import RealTime

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve the Groq API key from environment variables
GroqAPIKey = env_vars.get("BrainAPI") 

# Initialize the Groq client with the provided API key
client = Groq(api_key=GroqAPIKey)

# System prompt to guide the AI in classifying queries
System_Prompt = """
1. You are an advanced AI system that categorizes queries into two types: general queries and real-time queries.
2. A query is classified as a general query if it can be answered by a language model (LLM).
3. A query is categorized as a real-time query if it requires current, up-to-date information.
# Examples of query categorization:
a) "Hello Jarvis, How are you?" - general Hello Jarvis, How are you?
b) "What's the stock price of Tata?" - realtime What's the stock price of Tata?
4. Ensure that all queries are formatted correctly, including proper punctuation and capitalization.
5. Remember to include general and real-time status at the beginning of the query(in lowercase).
6. Don't add or remove anything or even word else in the Query.
7. Don't add fullstop or period after status like (general. or realtime.), it is wrong way."""

def AnswerModifier(Answer):
    """
    Modify the answer by removing any empty lines.
    
    Parameters:
    Answer (str): The original answer string.
    
    Returns:
    str: The modified answer with empty lines removed.
    """
    return '\n'.join(line for line in Answer.split('\n') if line.strip())  # Join non-empty lines

def Model(Query):
    """
    Generate a response from the model based on the user's query.
    
    Parameters:
    Query (str): The user's query.
    
    Returns:
    str: The model's response after classification.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Specify the model to use
        messages=[{"role": "system", "content": System_Prompt}, {"role": "user", "content": Query}],
        max_tokens=1024,  # Limit the response length
        temperature=0.7,  # Control the randomness of the output
        top_p=1,  # Use nucleus sampling
        stream=True,  # Enable streaming of responses
        stop=None  # No specific stop sequence
    )
    
    # Concatenate the chunks of the response
    Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
    return AnswerModifier(Answer)  # Return the modified answer

def main(text):
    """
    Main function to handle the query classification and response generation.
    
    Parameters:
    text (str): The user's input text.
    
    Returns:
    str: The response from the appropriate system based on query classification.
    """
    Query = Model(text)  # Get the model's response
    
    # Check if the query is classified as general or real-time
    if Query.startswith("general"):
        _, actual_query = Query.split(" ", 1)  # Extract the actual query
        Response = ChatBot.main(actual_query)  # Get response from the ChatBot
        return Response
    elif Query.startswith("realtime"):
        _, actual_query = Query.split(" ", 1)  # Extract the actual query
        Response = RealTime.main(actual_query)  # Get response from the RealTime module
        return Response
    else:
        return "Query classification not recognized."  # Handle unrecognized queries
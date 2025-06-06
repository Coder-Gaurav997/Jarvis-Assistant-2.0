"""
ChatBot Application
Author: Gaurav Pandey
"""

from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve user and assistant names and the Groq API key from environment variables
UserName = env_vars.get("User  Name")
AssistantName = env_vars.get("AssistantName")
GroqAPIKey = env_vars.get("ChatBotAPI")

# Initialize the Groq client with the provided API key
client = Groq(api_key=GroqAPIKey)

def RealTimeInformation():
    """
    Get the current date and time formatted as a string.
    
    Returns:
    str: A string containing the current day, date, month, and year.
    """
    current_date_time = datetime.datetime.now()  # Get the current date and time
    return f"Day: {current_date_time.strftime('%A')}, Date: {current_date_time.strftime('%d')}, Month: {current_date_time.strftime('%B')}, Year: {current_date_time.strftime('%Y')}"

def AnswerModifier(Answer):
    """
    Modify the answer by removing any empty lines.
    
    Parameters:
    Answer (str): The original answer string.
    
    Returns:
    str: The modified answer with empty lines removed.
    """
    return '\n'.join(line for line in Answer.split('\n') if line.strip())  # Join non-empty lines

# System message to set the context for the chatbot
System = f"""***I am {UserName} and you are a very advanced AI assistant named {AssistantName}***
***Don't tell the time and date until asked***
***Keep your answers as short as possible and point to point***
***Your responses should be professional, attractive, and use simple words***"""

def log_conversation(user_query, bot_response):
    """
    Log the conversation between the user and the bot to a JSON file.
    
    Parameters:
    user_query (str): The user's query.
    bot_response (str): The bot's response.
    """
    conversation = {
        "user": user_query,
        "bot": bot_response,
        "timestamp": datetime.datetime.now().isoformat()  # Record the timestamp of the conversation
    }
    
    # Check if the conversation log file exists
    if os.path.exists("Conversation.json"):
        with open("Conversation.json", "r") as file:
            data = load(file)  # Load existing conversation data
            data.append(conversation)  # Append the new conversation
    else:
        data = [conversation]  # Create a new list for the first conversation
    
    # Write the updated conversation data back to the JSON file
    with open("Conversation.json", "w") as file:
        dump(data, file, indent=4)  # Save with pretty formatting

def ChatBot(Query, real_time_info):
    """
    Generate a response from the chatbot based on the user's query and real-time information.
    
    Parameters:
    Query (str): The user's query.
    real_time_info (str): The current date and time information.
    
    Returns:
    str: The chatbot's response.
    """
    completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Specify the model to use
        messages=[
            {"role": "system", "content": System},
            {"role": "system", "content": real_time_info},
            {"role": "user", "content": Query}
        ],
        max_tokens=1024,  # Limit the response length
        temperature=0.7,  # Control the randomness of the output
        top_p=1,  # Use nucleus sampling
        stream=True,  # Enable streaming of responses
        stop=None  # No specific stop sequence
    )

    # Concatenate the chunks of the response
    Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
    return AnswerModifier(Answer)  # Return the modified answer

def main(Query):
    """
    Main function to handle the chatbot interaction.
    
    Parameters:
    Query (str): The user's query.
    
    Returns:
    str: The chatbot's response.
    """
    real_time_info = RealTimeInformation()  # Get real-time information
    Answer = ChatBot(Query, real_time_info)  # Get the chatbot's response
    log_conversation(Query, Answer)  # Log the conversation
    return Answer  # Return the final answer
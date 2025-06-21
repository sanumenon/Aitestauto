from dotenv import load_dotenv
from google import genai
from google.genai import types
import os   

# This script initializes a Google Generative AI client for interacting with a Large Language Model (LLM).
load_dotenv() # Load environment variables from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Get your Gemini API key

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please set it.")

client = genai.Client(api_key=GOOGLE_API_KEY)


# Function to get a response from the LLM
# This function takes a prompt and returns the LLM's response.
# It uses the configured LLM client to generate the response.
# The response is generated with a specified temperature to control randomness.
# The temperature parameter can be adjusted to make the responses more or less random.
# A lower temperature (e.g., 0.2) makes the output more deterministic,
# while a higher temperature (e.g., 0.8) makes it more creative and varied.

def get_llm_response(prompt: str, temperature=0.7):
    """
    Get a response from the LLM for a given prompt.
    
    Args:
        prompt (str): The input prompt for the LLM.
        max_tokens (int): The maximum number of tokens in the response.
        
    Returns:
        str: The response from the LLM.
    """
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature)
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error: Could not generate response." 
print(f"LLM client initialized successfully.")
print(f"You can now use the llm_client to get responses from the LLM.")
#print(get_llm_response("Explain the concept of Page Object Model in test automation."))
"""
Test script for Grok API connection
Run this to verify your API key and connection
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment or prompt user
API_KEY = os.getenv("GROK_API_KEY")
if not API_KEY:
    API_KEY = input("Enter your xAI Grok API key: ")

# Initialize the client (xAI uses the OpenAI-compatible endpoint)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.x.ai/v1",
)

def test_api_connection():
    """Test the Grok API connection"""
    print("Testing Grok API connection...\n")
    
    try:
        # Make a test chat completion request
        response = client.chat.completions.create(
            model="grok-3",  # Options: grok-3, grok-4, grok-3-mini
            messages=[
                {"role": "user", "content": "Introduce yourself in one sentence."}
            ],
            max_tokens=50,
        )
        
        # Print the response
        print("✓ API key is valid! Response:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        print(f"\nModel used: {response.model}")
        print(f"Tokens used: {response.usage.total_tokens}")
        return True
        
    except Exception as e:
        print(f"✗ Error testing API key: {e}\n")
        
        error_msg = str(e)
        if "401" in error_msg:
            print("This likely means your API key is invalid or expired.")
            print("Get your API key at: https://x.ai/api")
        elif "429" in error_msg:
            print("Rate limit exceeded. Try again later.")
        elif "404" in error_msg and "model" in error_msg.lower():
            print("Model not found—check available models at https://x.ai/api.")
        
        return False


def test_esg_response():
    """Test with an ESG-related query"""
    print("\n\nTesting with ESG-related query...\n")
    
    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ESG analyst."
                },
                {
                    "role": "user",
                    "content": "List the three main pillars of ESG reporting."
                }
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        print("✓ ESG query successful! Response:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Grok API Connection Test")
    print("=" * 60)
    
    # Test basic connection
    if test_api_connection():
        # If successful, test ESG-specific query
        test_esg_response()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

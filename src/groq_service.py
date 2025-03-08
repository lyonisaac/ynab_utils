"""Groq API service for emoji suggestions."""
import requests
from typing import Optional

class GroqService:
    """Service for interacting with Groq API."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_emoji_suggestion(self, payee_name: str) -> Optional[str]:
        """Get emoji suggestion for a payee using Groq API."""
        url = f"{self.base_url}/chat/completions"
        
        prompt = (
            f'Please suggest a single emoji that best represents the following '
            f'business/payee name: "{payee_name}"\n\n'
            f'Return ONLY the emoji character and nothing else. Choose an emoji '
            f'that intuitively represents the type of business or service.'
        )
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5,
            "max_tokens": 10,
            "top_p": 1
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            emoji = result['choices'][0]['message']['content'].strip()
            return emoji
        except Exception as e:
            print(f"Error getting emoji from Groq API: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            return None
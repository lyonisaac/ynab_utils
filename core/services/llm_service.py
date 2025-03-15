"""LLM service for interacting with various LLM providers."""
from abc import ABC, abstractmethod
import requests
from typing import Optional, Dict, Any, List


class LLMService(ABC):
    """Abstract base class for LLM services."""
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate text response from the LLM."""
        pass


class GroqService(LLMService):
    """Service for interacting with Groq API."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using Groq API."""
        url = f"{self.base_url}/chat/completions"
        
        temperature = kwargs.get("temperature", 0.5)
        max_tokens = kwargs.get("max_tokens", 50)
        top_p = kwargs.get("top_p", 1.0)
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error generating text from Groq API: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            return None
            
    def get_emoji_suggestion(self, text: str) -> Optional[str]:
        """Get emoji suggestion for text using Groq API."""
        # Check if this is a retry attempt (contains previously suggested emojis)
        retry_instructions = ""
        if "Previously suggested:" in text:
            # Split the input to separate the payee name from the retry context
            parts = text.split("This is retry #")
            base_text = parts[0].strip()
            
            # Extract previously suggested emojis
            if len(parts) > 1:
                previously_suggested = parts[1].split("Previously suggested:")[1].strip()
                retry_instructions = (
                    f"\nThis is a retry attempt. Please suggest a DIFFERENT emoji than the "
                    f"following previously suggested ones: {previously_suggested}."
                )
        else:
            base_text = text
            
        prompt = (
            f'Please suggest a single emoji that best represents the following '
            f'business/payee name: "{base_text}"{retry_instructions}\n\n'
            f'Return ONLY the emoji character and nothing else. Choose an emoji '
            f'that intuitively represents the type of business or service.'
        )
        
        return self.generate_text(
            prompt=prompt,
            temperature=0.7,  # Slightly higher temperature for more variety in retries
            max_tokens=10
        )


# Factory function to get the appropriate LLM service
def get_llm_service(provider: str, **kwargs) -> Optional[LLMService]:
    """Get an LLM service instance based on provider name."""
    if provider.lower() == "groq":
        api_key = kwargs.get("api_key")
        model = kwargs.get("model", "llama3-70b-8192")
        if not api_key:
            raise ValueError("API key is required for Groq service")
        return GroqService(api_key=api_key, model=model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
import os
import json
import anthropic
from typing import Dict, Any

class ClaudeCustomPrompt:
    """
    ComfyUI node that generates prompts using Claude API
    """
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.client = None
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "system_prompt": ("STRING", {
                    "default": "You are an AI art prompt generator. Reply only with a prompt for image generation, no explanations.", 
                    "multiline": True
                }),
                "user_input": ("STRING", {
                    "default": "Generate a prompt for: space cat", 
                    "multiline": True
                }),
            },
            "optional": {
                "api_key": ("STRING", {
                    "default": "", 
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "prompt generation"
    
    def generate_prompt(self, system_prompt: str, user_input: str, api_key: str = "") -> tuple[str]:
        """
        Generate a prompt using Claude API.
        
        Args:
            system_prompt (str): System instructions for Claude
            user_input (str): User's input prompt to be expanded
            api_key (str, optional): Claude API key. Defaults to environment variable
            
        Returns:
            tuple[str]: Generated prompt as a single-element tuple
            
        Raises:
            ValueError: If no API key is provided or inputs are empty
            RuntimeError: If API call fails
        """
        # Input validation
        if not system_prompt.strip():
            raise ValueError("System prompt cannot be empty")
        if not user_input.strip():
            raise ValueError("User input cannot be empty")
            
        # Use provided API key or fallback to environment variable
        key_to_use = api_key if api_key else self.api_key
        if not key_to_use:
            raise ValueError("No API key provided. Please set ANTHROPIC_API_KEY environment variable or provide it as input.")
            
        # Initialize client if needed
        if not self.client or api_key:
            self.client = anthropic.Anthropic(api_key=key_to_use)
        
        try:
            # Make API call to Claude
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )
            
            # Extract the generated prompt
            if not message.content:
                raise RuntimeError("No content received from API")
                
            generated_prompt = message.content[0].text.strip()
            return (generated_prompt,)
            
        except anthropic.APIError as e:
            raise RuntimeError(f"API Error: {str(e)}")
        except anthropic.RateLimitError as e:
            raise RuntimeError(f"Rate limit exceeded: {str(e)}")
        except anthropic.APIConnectionError as e:
            raise RuntimeError(f"Connection error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

# Node registration
NODE_CLASS_MAPPINGS = {
    "ClaudeCustomPrompt": ClaudeCustomPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ClaudeCustomPrompt": "Claude Prompt Generator"
}

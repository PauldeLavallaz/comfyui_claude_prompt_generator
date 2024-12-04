import os
import anthropic
from typing import Dict, Any

class ClaudeCustomPrompt:
    """
    ComfyUI node that generates prompts using the Anthropic Claude API.
    """

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
    RETURN_NAMES = ("generated_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Prompt Generation"

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.client = None

    def generate_prompt(self, system_prompt: str, user_input: str, api_key: str = "") -> tuple:
        # Use provided API key or fallback to environment variable
        key_to_use = api_key if api_key else self.api_key
        if not key_to_use:
            raise ValueError("No API key provided. Please set ANTHROPIC_API_KEY environment variable or provide it as input.")

        # Initialize client if needed
        if not self.client or api_key:
            self.client = anthropic.Client(api_key=key_to_use)

        try:
            # Construct the prompt
            prompt = f"{anthropic.HUMAN_PROMPT}{system_prompt}\n{user_input}{anthropic.AI_PROMPT}"

            # Make API call to Claude
            response = self.client.completion(
                prompt=prompt,
                model="claude-v1",
                max_tokens_to_sample=500,
                temperature=0,
                stop_sequences=[anthropic.HUMAN_PROMPT]
            )

            # Extract the generated prompt
            generated_prompt = response['completion'].strip()
            return (generated_prompt,)

        except Exception as e:
            raise RuntimeError(f"Error generating prompt: {str(e)}")

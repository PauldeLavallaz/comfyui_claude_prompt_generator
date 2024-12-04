from .claude_custom_prompt import ClaudeCustomPrompt

NODE_CLASS_MAPPINGS = {
    "ClaudeCustomPrompt": ClaudeCustomPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ClaudeCustomPrompt": "Claude Prompt Generator"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

class SplitTextLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Ingrese su texto aquí."}),
                "words_per_line": ("INT", {"default": 5, "min": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "split_text"
    CATEGORY = "Text"

    def split_text(self, text, words_per_line):
        words = text.split()
        lines = [" ".join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
        return ("\n".join(lines),)

NODE_CLASS_MAPPINGS = {"SplitTextLines": SplitTextLines}
NODE_DISPLAY_NAME_MAPPINGS = {"SplitTextLines": "Dividir texto en líneas"}

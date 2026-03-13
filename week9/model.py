from llama_cpp import Llama


class LocalModel:
    def __init__(self, model_path: str):
        """
        model_path: absolute or relative path to your .gguf model
        """

        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,          # match model training context if possible
            n_threads=8,         # adjust based on CPU cores
            verbose=False
        )

    def generate(self, messages, max_tokens: int = 300):
        """
        messages: list of dicts like:
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
        """

        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=0.2,      # low temperature for agent discipline
            max_tokens=max_tokens,
        )

        return response["choices"][0]["message"]["content"].strip()
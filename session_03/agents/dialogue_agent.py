class DialogueAgent:
    def __init__(self, name: str, system_message: str) -> None:
        self.name = name
        self.system_message = system_message
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        # Use Ollama here instead of OpenAI
        prompt = "\n".join(self.message_history + [self.prefix])
        response = self.ollama_call(prompt)  # Implement this method
        return response

    def receive(self, name: str, message: str) -> None:
        self.message_history.append(f"{name}: {message}")

    def ollama_call(self, prompt: str) -> str:
        # Implement Ollama API call here
        # This is a placeholder, you need to implement the actual Ollama API call
        return "Ollama response placeholder"
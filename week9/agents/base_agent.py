from collections import deque

class BaseAgent:
    def __init__(self, name, system_prompt, model):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.memory = deque(maxlen=10)

    def receive(self, message):
        self.memory.append({"role": "user", "content": message})

    def think(self):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory)

        response = self.model.generate(messages)

        self.memory.append({"role": "assistant", "content": response})

        print(f"\n[{self.name} MEMORY SIZE]: {len(self.memory)}")

        return response
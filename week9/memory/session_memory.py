class SessionMemory:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        # keep only last N messages
        if len(self.messages) > self.window_size:
            self.messages.pop(0)

    def get_memory(self):
        return self.messages

    def clear(self):
        self.messages = []
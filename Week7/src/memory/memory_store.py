import json
from collections import deque
from pathlib import Path
import numpy as np

LOG_FILE = Path("CHAT-LOGS.json")


class MemoryStore:
    def __init__(self, max_history=5):
        self.history = deque(maxlen=max_history)

    def add(self, role, message):
        self.history.append({"role": role, "message": message})
        self._log(role, message)

    def get_recent(self):
        return list(self.history)

    def _log(self, role, message):
        entry = {"role": role, "message": message}
        if LOG_FILE.exists():
            data = json.loads(LOG_FILE.read_text())
        else:
            data = []
        data.append(entry)
        LOG_FILE.write_text(json.dumps(data, indent=2))

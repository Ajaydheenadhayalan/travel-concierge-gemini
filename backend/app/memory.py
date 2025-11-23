class InMemorySessionService:
    def __init__(self): self.sessions = {}
    def create_or_get(self, user_id): return self.sessions.setdefault(user_id,{})
    def save(self, user_id, data): self.sessions[user_id] = data

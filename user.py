import uuid

class User:
    def __init__(self, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.birthdate = str(uuid.uuid4())
        self.follow_requests = set()
        self.followers = set()
        self.following = set()
        self.blocked_users = set()

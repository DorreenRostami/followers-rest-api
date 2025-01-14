import uuid

class User:
    def __init__(self, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.birthdate = str(uuid.uuid4())
        self.follow_requests = set()
        self.followers = set()
        self.following = set()
        self.blocked_users = set()

    def send_follow_request(self, other_user):
        if self.user_id in other_user.blocked_users:
            return 0
        if self.user_id in other_user.followers:
            return -1
        other_user.follow_requests.add(self.user_id)
        return 1
    
    def accept_follow_request(self, other_user):
        if other_user.user_id not in self.follow_requests:
            return False
        self.follow_requests.remove(other_user.user_id)
        self.followers.add(other_user.user_id)
        other_user.following.add(self.user_id)
        return True
        

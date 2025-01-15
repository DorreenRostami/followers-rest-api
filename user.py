import uuid

class User:
    def __init__(self, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.birthdate = str(uuid.uuid4())
        self.follow_requests = set()
        self.followers = set()
        self.following = set()
        self.blocked_users = set()

    def get_follow_requests(self):
        return self.follow_requests
    
    def get_followers(self):
        return self.followers
    
    def get_following(self):
        return self.following
    
    def get_blocked_users(self):
        return self.blocked_users

    def send_follow_request(self, other_user):
        if self.user_id == other_user.user_id: 
            return 0
        if self.user_id in other_user.blocked_users:
            return -1
        if self.user_id in other_user.followers:
            return -2
        if other_user.user_id in self.blocked_users:
            return -3
        other_user.follow_requests.add(self.user_id)
        return 1
    
    def handle_follow_request(self, other_user, accept=True):
        if self.user_id == other_user.user_id or other_user.user_id not in self.follow_requests:
            return False
        self.follow_requests.remove(other_user.user_id)
        if accept:
            self.followers.add(other_user.user_id)
            other_user.following.add(self.user_id)
        return True
    
    def block_user(self, other_user):
        if self.user_id == other_user.user_id:
            return False
        self.blocked_users.add(other_user.user_id)
        self.follow_requests.discard(other_user.user_id)
        self.followers.discard(other_user.user_id)
        self.following.discard(other_user.user_id)
        return True
    

        

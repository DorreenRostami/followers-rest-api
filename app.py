from flask import Flask, jsonify, request
from user import User
from threading import Lock

import user

app = Flask(__name__)
lock = Lock()
users = {}

@app.route('/create_user', methods=['POST'])
def create_user_endpoint():
    if request.is_json:
        req = request.get_json()
        if not req:
            user = User()
        else:
            user_id = req.get('user_id', None)  # If user_id is in the body, use it
            user = User(user_id)
        users[user.user_id] = user
        return jsonify({'user_id': user.user_id, 'birthdate': user.birthdate}), 201
    else:
        return jsonify({'error': 'Invalid content type, application/json expected'}), 400
    

@app.route('/users', methods=['GET'])
def get_users_endpoint():
    return jsonify({'user_ids': list(users.keys())}), 200

@app.route('/send_follow_request', methods=['POST'])
def send_follow_request_endpoint():
    req = request.json
    if not req or 'sender' not in req or 'receiver' not in req:
        return jsonify({'message': 'Missing sender or receiver'}), 400
    
    sender = users.get(req['sender'])
    receiver = users.get(req['receiver'])

    if not sender or not receiver:
        return jsonify({'message': 'User not found'}), 404

    with lock:
        res = sender.send_follow_request(receiver)
        if res == 0:
            return jsonify({'message': f'Forbidden: Users can\'t follow themselves'}), 403
        elif res == -1:
            return jsonify({'message': f'Forbidden: {sender.user_id} is blocked by {receiver.user_id}'}), 403
        elif res == -2:
            return jsonify({'message': f'{sender.user_id} already follows {receiver.user_id}'}), 400
        elif res == -3:
            return jsonify({'message': f'Forbidden: {sender.user_id} has blocked {receiver.user_id} and cannot follow them'}), 403
        return jsonify({'message': f'Follow request sent from {sender.user_id} to {receiver.user_id}'}), 200 #res=1
        
    
@app.route('/accept_follow_request', methods=['POST'])
def accept_follow_request_endpoint():
    req = request.json
    if not req or 'this_user' not in req or 'potential_follower' not in req:
        return jsonify({'message': 'Missing this_user or potential_follower'}), 400
    
    this_user = users.get(req['this_user'])
    potential_follower = users.get(req['potential_follower'])

    if not this_user or not potential_follower:
        return jsonify({'message': 'User not found'}), 404

    with lock:
        if this_user.handle_follow_request(potential_follower):
            return jsonify({'message': f'{potential_follower.user_id} is now following {this_user.user_id}'}), 200
        return jsonify({'message': f'{potential_follower.user_id} has not sent a request to follow {this_user.user_id}'}), 404

@app.route('/deny_follow_request', methods=['POST'])
def deny_follow_request_endpoint():
    req = request.json
    if not req or 'this_user' not in req or 'potential_follower' not in req:
        return jsonify({'message': 'Missing this_user or potential_follower'}), 400
    
    this_user = users.get(req['this_user'])
    potential_follower = users.get(req['potential_follower'])

    if not this_user or not potential_follower:
        return jsonify({'message': 'User not found'}), 404

    with lock:
        if this_user.handle_follow_request(potential_follower, False):
            return jsonify({'message': f'{potential_follower.user_id}\'s follow request removed from {this_user.user_id}\'s requests'}), 200
        return jsonify({'message': f'{potential_follower.user_id} has not sent a request to follow {this_user.user_id}'}), 404
    
@app.route('/block_user', methods=['POST'])
def block_user_endpoint():
    req = request.json
    if not req or 'blocker' not in req or 'blocked' not in req:
        return jsonify({'message': 'Missing blocker or blocked'}), 400
    
    blocker_id = req.get('blocker')
    blocked_id = req.get('blocked')

    if blocker_id not in users or blocked_id not in users:
        return jsonify({'message': 'User not found'}), 404

    blocker = users[blocker_id]
    blocked = users[blocked_id]

    with lock:
        if blocker.block_user(blocked):
            return jsonify({'message': f'{blocker.user_id} has blocked {blocked.user_id}'}), 200
        else :
            return jsonify({'message': f'Forbidden: Users can\'t block themselves'}), 403
    
if __name__ == '__main__':
    app.run()
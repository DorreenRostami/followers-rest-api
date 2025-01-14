from flask import Flask, jsonify, request
from user import User
from threading import Lock

import user

app = Flask(__name__)
lock = Lock()
users = {}

@app.route('/create_user', methods=['GET','POST'])
def create_user_endpoint():
    user = User()
    users[user.user_id] = user
    return jsonify({'user_id': user.user_id, 'birthdate': user.birthdate}), 201

@app.route('/users', methods=['GET'])
def get_users_endpoint():
    return jsonify({'user_ids': list(users.keys())}), 200

@app.route('/send_follow_request', methods=['POST'])
def send_follow_request_endpoint():
    req = request.json
    sender = users.get(req['sender'])
    receiver = users.get(req['receiver'])

    if not sender or not receiver:
        return jsonify({'message': 'Not Found: User not found'}), 404

    with lock:
        res = sender.send_follow_request(receiver)
        if res == 1:
            return jsonify({'message': f'OK: Follow request sent from {sender.user_id} to {receiver.user_id}'}), 200
        if res == 0:
            return jsonify({'message': f'Forbidden: {sender.user_id} is blocked by {receiver.user_id}'}), 403
        return jsonify({'message': f'Forbidden: {sender.user_id} already follows {receiver.user_id}'}), 403
    
@app.route('/accept_follow_request', methods=['POST'])
def accept_follow_request_endpoint():
    req = request.json
    this_user = users.get(req['this_user'])
    potential_follower = users.get(req['potential_follower'])

    if not this_user or not potential_follower:
        return jsonify({'message': 'Not Found: User not found'}), 404

    with lock:
        if this_user.accept_follow_request(potential_follower):
            return jsonify({'message': f'OK: {potential_follower.user_id} is now following {this_user.user_id}'}), 200
        return jsonify({'message': f'Not Found: {potential_follower.user_id} has not sent a request to follow {this_user.user_id}'}), 404
    
if __name__ == '__main__':
    app.run()
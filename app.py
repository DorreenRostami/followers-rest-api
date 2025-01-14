from flask import Flask, jsonify
from user import User
from threading import Lock

app = Flask(__name__)
lock = Lock()
users = {}

@app.route('/create_user', methods=['POST'])
def create_user_endpoint():
    user = User()
    users[user.user_id] = user
    return jsonify({'user_id': user.user_id, 'birthdate': user.birthdate}), 201


if __name__ == '__main__':
    app.run()
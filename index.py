#!/usr/bin/env python3

# link: http://localhost:8080
# could be useful for ws: https://flask-socketio.readthedocs.io/en/latest/
# sqlite docs: https://docs.python.org/3/library/sqlite3.html

# json file handling
import json
# web server stuffs
from flask import Flask, request, Response, redirect, send_file
# websockets (for real-time communication)
from flask_socketio import SocketIO, emit

# import local helper classes
from helper.voting import Voting
from helper.voterData import VoterData

# load config
with open("config.json") as config_file:
    config = json.load(config_file)

# start things up
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']
socketio = SocketIO(app)

globalVote = Voting(config['options'])
voter_list = []

# if QR code is on the side, users can scan that to bring up
# the voting page on another device
# incorporate OAuth / Google Sign-In later

# Default question/answer choices. Override in admin panel.
data = {
    'question': "Default Question",
    'options': [
        "One",
        "Two",
        "Three",
        "Four",
        "Five"
    ],
    'vbucks': config['vbucks']
}

def renderTable(inp):
    el = ""
    for i in range(0, len(inp['fptp'])):
        fptp_num = list(inp['fptp'])[i]
        borda_num = list(inp['borda'])[i]
        score_num = list(inp['score'])[i]
        quad_num = list(inp['quad'])[i]

        fptp = data['options'][int(fptp_num) - 1]
        borda = data['options'][int(borda_num) - 1]
        score = data['options'][int(score_num) - 1]
        quad = data['options'][int(quad_num) - 1]
        
        el += f"<tr><td>{i + 1}</td><td>{fptp}</td><td>{borda}</td><td>{score}</td><td>{quad}</td></tr>"
    return el

# Web server -------------------------------

# voting page
@app.route('/')
def vote():
    return send_file(
            "static/index.html",
            attachment_filename="index.html",
            mimetype="text/html"
    )

# admin page
@app.route('/admin')
def admin_page():
    return send_file(
            "static/admin.html",
            attachment_filename="admin.html",
            mimetype="text/html"
    )

if config['debug']:
    # debug menu
    @app.route('/console')
    def console_page():
        return send_file(
                "static/console.html",
                attachment_filename="console.html",
                mimetype="text/html"
        )

# serves stylesheet
@app.route('/index.css')
def serve_css():
    return send_file(
            "static/index.css",
            attachment_filename="index.css",
            mimetype="text/css"
    )

# serves voter js
@app.route('/index.js')
def serve_js():
    return send_file(
            "static/index.js",
            attachment_filename="index.js",
            mimetype="text/javascript"
    )

# serves admin js
@app.route('/admin.js')
def serve_admin_js():
    return send_file(
            "static/admin.js",
            attachment_filename="admin.js",
            mimetype="text/javascript"
    )

# WebSockets ----------------------------------

# New user identified. Pass important data to prepare client (such as question and options)
@socketio.on('newUser')
def handle_new_user(message):
    print("New user connected.")
    emit('conf', data)
    emit('updateResults', renderTable(globalVote.get_votes()), broadcast=True)

# When votes are submitted on frontend, they are processed here.
@socketio.on('voteSubmit')
def handle_submission(message):
    # (validation here)
    """
    {
        "data": "User voted.",
        "fptp": 0,
        "borda": [],
        "score": [],
        "quad": []
    }
    """

    total = 0
    for value in message['quad']:
        total += value * value

    if total > config['vbucks']:
        # Unlock the client and have them try again.
        print("Invalid vote detected! Too many votes allocated.")
        emit('status', {'data': "unlock", 'invalid': True})
        return

    if message['fptp'] == -1:
        print("Invalid vote detected! No FPTP vote.")
        emit('status', {'data': "unlock", 'invalid': True})
        return

    globalVote.quadratic(message['quad'])
    print("Vote submitted successfully.")

    voter = VoterData(config['options'])
    voter.score_fptp(message['fptp'])
    voter.score_borda(message['borda'])
    voter.score_score(message['score'])
    voter.score_quad(message['quad'])
    voter_list.append(voter.get_votes())

    globalVote.fptp_vote(message['fptp'])
    globalVote.borda_vote(message['borda'])
    globalVote.score_vote(message['score'])
    globalVote.num_voters += 1

    # Send results to all locked clients
    emit('updateResults', renderTable(globalVote.get_votes()), broadcast=True)

"""
Everything here should be restricted to admin only. If user isn't admin, drop the connection.
"""
@socketio.on('admin')
def admin(message):
    try:
        # This is NEVER how you should do auth, but this is a /hack/athon, after all.
        if message['password'] == config['password']:
            # Screen locking
            try:
                if message['lock'] == True:
                    print("[Admin] Locking users...")
                    emit('status', {'data': "lock"}, broadcast=True)
                else:
                    print("[Admin] Unlocking users...")
                    emit('status', {'data': "unlock"}, broadcast=True)
            except:
                # If lock state isn't set, ignore.
                pass

            # Question updating
            try:
                if message['question']:
                    data['question'] = message['question']
                    print(f"[Admin] New question set: {data['question']}")
                    emit('question', {'data': data['question']}, broadcast=True)
            except:
                pass

            # Options updating
            try:
                if message['options']:
                    data['options'] = message['options']
                    print(f"Options updated. Refresh clients to update.")
                    # stretch goal: notification on options update
            except:
                pass
        else:
            print("[Admin] Unauthorized access (bad passphrase).")
    except:
        print("[Admin] Unauthorized access (no passphrase).")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=config['port'], debug=config['debug'])
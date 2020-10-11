# VoteyMcVote.space

A single-instance, game-styled surveying tool for multiple polling systems written in Python and JavaScript.

Created at [KnightHacks 2020](https://knighthacks.org/) by:

- [Cameron B.](https://github.com/CameronBerezuk)
- [Conrad S.](https://github.com/conradsmi)
- [Prathik](https://github.com/prathik2001)
- [Jeffrey D.V.](https://github.com/jeffreydivi)

Demo at [VoteyMcVote.space](https://VoteyMcVote.space/)

## Features

- Conduct surveys in multiple polling systems simultaneously in real time
- Customize poll question and responses in an admin panel
- Lock and unlock active users' screens on-demand

## Polling Systems Supported

- [First-Past-The-Post](https://en.wikipedia.org/wiki/First-past-the-post_voting)
- [Borda Count](https://en.wikipedia.org/wiki/Borda_count)
- [Score Voting](https://en.wikipedia.org/wiki/Score_voting)
- [Quadratic Voting](https://en.wikipedia.org/wiki/Quadratic_voting)

## Technologies Used

- [Flask](https://palletsprojects.com/p/flask/)
- [Socket.IO](https://socket.io/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
- [SortableJS](https://sortablejs.github.io/sortablejs/)

## Setup

```bash
# Install requirements
pip3 install -r requirements.txt
# Start the server
python3 index.py
```

## Known Bugs

A lot of them. I doubt this is secure either.

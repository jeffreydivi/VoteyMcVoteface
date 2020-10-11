# VoteyMcVote.space

A single-instance, game-styled surveying tool for multiple polling systems written in Python and JavaScript.

Created at [KnightHacks 2020](https://knighthacks.org/) by:

- [Cameron B.](https://github.com/CameronBerezuk)
- [Conrad S.](https://github.com/conradsmi)
- [Prathik R.](https://github.com/prathik2001)
- [Jeffrey D.V.](https://github.com/jeffreydivi)

## Description

VoteyMcVote.space provides an entertaining demonstration of the relative merits of different voting systems, and allows users to learn more about these systems and explore how they work in practice. In an era where political polarization is approaching record highs and numerous people feel that they do not have a say in the political system, it is important to spread knowledge about alternative voting methods that may allow people with all sorts of different opinions to have an influence on the final outcome. In addition to this, we believe change starts from the bottom up, and VoteyMcVote.space allows individuals and organizations to see the effects of different voting systems on any personal issue, solving any problem from leadership elections to choosing the best pizza toppings. VoteyMcVote.space showcases innovative, inclusive new approaches to decision making and seeks to bring forward a future where standard polling will be revolutionized.

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

## The Story

We are all Burnett Honors CS students participating in our first hackathon. After some brainstorming, we decided to make a simple educational tool that showcases different polling methods (from first-past-the-post to quadratic voting) and displays the results in real time. Despite most of us being C natives, we had a bit of experience in Python, so we agreed it would be a fair common-ground language to build a more sophisticated application.

And then we built a thing, decided it would be funny to name it VoteyMcVote.space (the domain works nicely here), and released it to the world.

VoteyMcVote.space provides an entertaining demonstration of the relative merits of different voting systems, and allows users to learn more about these systems and explore how they work in practice. In an era where political polarization is approaching record highs and numerous people feel that they do not have a say in the political system, it is important to spread knowledge about alternative voting methods that may allow people with all sorts of different opinions to have an influence on the final outcome. In addition to this, we believe change starts from the bottom up, and VoteyMcVote.space allows individuals and organizations to see the effects of different voting systems on any personal issue, solving any problem from leadership elections to choosing the best pizza toppings. VoteyMcVote.space showcases innovative, inclusive new approaches to decision making and seeks to bring forward a future where standard polling will be revolutionized.

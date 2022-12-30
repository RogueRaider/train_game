from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aqwerqwer!##$@#@$'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/train-game')
def train_game():
	return render_template('train_game.html')


if __name__ == '__main__':
    socketio.run(app, port=8000, host='0.0.0.0')




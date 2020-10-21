#!/usr/bin/env python3
import flask
import datetime

app = flask.Flask(__name__)
@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime('%Y-%m-%d %H:%M')
    templateData = {
        'title' : 'Flask Server',
        'time': timeString
    }
    return flask.render_template('index.html', **templateData)

@app.route('/input/clear')
def clear():
    print('Cleared!')
    return index()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8081, debug = True)
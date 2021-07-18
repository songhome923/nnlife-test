from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, XDDDD!'

if __name__ == 'main':
    app.run() #啟動伺服器
from flask import Flask

app=Flask(__name__)

@app.route('/')
def hello_world():
    return 'App running'

app.run(debug=True)
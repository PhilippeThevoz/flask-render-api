from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Render (PHT....)!")

@app.route('/api/data')
def data():
    return jsonify(data=[1, 2, 3, 4, 5, 6, 7])

@app.route('/api/hello/<name>')
def greet(name):
    return jsonify(greeting=f"Hello, {name}!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


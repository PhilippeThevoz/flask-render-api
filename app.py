from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Render (PHT....)!")

@app.route('/api/fileread/<filename>')
def fileread(filename):
    base_url = "https://raw.githubusercontent.com/PhilippeThevoz/Tests/main/.well-known/"
    file_url = f"{base_url}{filename}"
    print(f"📡 Fetching URL: {file_url}")

    try:
        response = requests.get(file_url)
        print(f"🌐 GitHub response status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            print(f"\n📄 Content of {filename}:\n{content}\n")  # Print to server console
            return jsonify(message=f"File '{filename}' read successfully.")
        else:
            print(f"⚠️ File not found or inaccessible: {file_url}")
            return jsonify(error=f"Could not read file: {filename}"), 404

    except requests.exceptions.RequestException as e:
        print(f"❌ Error reading file: {e}")
        return jsonify(error="Error fetching file from GitHub"), 500
        
@app.route('/api/hello/<name>')
def greet(name):
    return jsonify(greeting=f"Hello, {name}!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

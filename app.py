from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Render (PHT....)!")

@app.route('/api/fileread/<path:filename>')
def fileread(filename):
    # Full GitHub raw content base
    base_url = "https://raw.githubusercontent.com/PhilippeThevoz/Tests/main/"
    file_url = f"{base_url}{filename}"
    
    print(f"📡 Fetching URL: {file_url}")

    try:
        response = requests.get(file_url)
        print(f"🌐 GitHub response status: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            print(f"\n📄 Content of {filename}:\n{content}\n")  # Print to server logs
            return jsonify(
                message=f"File '{filename}' read successfully.",
                content_preview=content[:200]  # Optional preview in response
            )
        else:
            print(f"⚠️ File not found or inaccessible: {file_url}")
            return jsonify(error=f"Could not read file: {filename}"), 404

    except requests.exceptions.RequestException as e:
        print(f"❌ Error reading file: {e}")
        return jsonify(error="Error fetching file from GitHub"), 500

@app.route('/api/hello/<name>')
def greet(name):
    return jsonify(greeting=f"Hello, {name}!")
    
    
from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# You should use an environment variable or secure store instead
GITHUB_TOKEN = "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"
REPO_OWNER = "PhilippeThevoz"
REPO_NAME = "Tests"
BRANCH = "main"

@app.route('/api/filewrite/<path:filename>', methods=['POST'])
def filewrite(filename):
    content = request.json.get("content", "")
    if not content:
        return jsonify(error="No content provided."), 400

    # GitHub API endpoint to create/update a file
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}"

    # First, get the current file SHA if it exists (required to update)
    response = requests.get(api_url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    })

    sha = response.json().get("sha") if response.status_code == 200 else None

    data = {
        "message": f"Updated via API: {filename}",
        "content": base64.b64encode(content.encode()).decode(),  # base64-encoded file content
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha  # required if updating

    write_response = requests.put(api_url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }, json=data)

    if write_response.status_code in (200, 201):
        return jsonify(message="✅ File written to GitHub", filename=filename)
    else:
        return jsonify(error="❌ Failed to write file", details=write_response.json()), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, jsonify
import requests
import json
from Function_verification1 import verification1

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Render (PHT....)!")

@app.route('/verify1/<prefix>')
@app.route('/verify1/<prefix>', methods=['POST'])
def verify1_route(prefix):
    try:
        data = request.get_json()
        file_content = data.get("file_content")

        if not file_content:
            return jsonify(error="Missing 'file_content' in request"), 400

        # Save file content temporarily in memory for validation
        records = json.loads(file_content)
        
        # Write to a temporary in-memory file for compatibility with verification1
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmpfile:
            json.dump(records, tmpfile)
            tmpfile.flush()
            tmpfile_path = tmpfile.name

        result = verification1(tmpfile_path)

        return jsonify(message=result)

    except Exception as e:
        return jsonify(error="Failed to process file content", details=str(e)), 500


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
GITHUB_TOKEN = os.environ.get("GITHUB_PHT")
REPO_OWNER = "PhilippeThevoz"
REPO_NAME = "Tests"
BRANCH = "main"

@app.route('/api/filewrite/<path:filename>', methods=['POST'])
def filewrite(filename):
    import base64

    try:
        token = os.environ.get("GITHUB_PHT")
        repo_owner = "PhilippeThevoz"
        repo_name = "Tests"
        branch = "main"

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

        content = request.json.get("content")
        if not content:
            return jsonify(error="Missing content"), 400

        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{filename}"

        # Check if file exists
        get_resp = requests.get(api_url, headers=headers)
        sha = get_resp.json().get("sha") if get_resp.status_code == 200 else None

        payload = {
            "message": f"Update {filename} via API",
            "content": encoded_content,
            "branch": branch
        }
        if sha:
            payload["sha"] = sha

        put_resp = requests.put(api_url, headers=headers, json=payload)
        print("📡 GitHub PUT response:", put_resp.status_code, put_resp.text)

        if put_resp.status_code in [200, 201]:
            return jsonify(message="✅ File written to GitHub", filename=filename)
        else:
            return jsonify(error="GitHub API error", details=put_resp.json()), 500

    except Exception as e:
        print("❌ Exception during filewrite:", e)
        return jsonify(error="Internal server error", details=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

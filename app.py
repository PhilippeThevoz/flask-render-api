import requests
import json

base_url = "https://flask-render-api-p8d4.onrender.com/api"

mode = input("Choose mode (read/write): ").strip().lower()

if mode == "read":
    relative_path = input("Enter the relative file path to read from GitHub (e.g. DPP/.../filename.json): ")
    url = f"{base_url}/fileread/{relative_path}"
    print("📡 Requesting URL:", url)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Response from API:")
            print(response.json())
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print("⚠️ Network error:", e)

elif mode == "write":
    relative_path = input("Enter the relative file path to WRITE to GitHub (e.g. PHT-Tests/my-file.txt): ")
    local_filename = input("Enter the local filename to upload (e.g. myfile.txt): ")

    try:
        with open(local_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"❌ File '{local_filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        exit(1)

    url = f"{base_url}/filewrite/{relative_path}"
    payload = {"content": file_content}
    print(f"📡 Uploading '{local_filename}' to GitHub as '{relative_path}'...")
    print("Sending to:", url)

    try:
        response = requests.post(url, json=payload)
        if response.status_code in (200, 201):
            print("✅ Write operation successful:")
            print(response.json())
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print("⚠️ Network error:", e)


else:
    print("❌ Invalid mode. Please choose 'read' or 'write'.")

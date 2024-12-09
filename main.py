import requests
from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import base64

app = Flask(__name__)

client = Client("https://vamsi92-removebg.hf.space")

# GitHub Configuration
GITHUB_TOKEN = "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"
GITHUB_REPO = "vamsi92/RemoveBGAPI"
GITHUB_BRANCH = "main"

def upload_to_github(file_name, file_content):
    """Uploads a file to GitHub and returns the public URL."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{file_name}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "message": f"Add {file_name}",
        "content": base64.b64encode(file_content).decode("utf-8"),  # Encode file as base64
        "branch": GITHUB_BRANCH,
    }

    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        file_info = response.json()
        return file_info["content"]["html_url"]  # GitHub URL for the file
    else:
        raise Exception(f"GitHub upload failed: {response.text}")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.args
    input_image = data.get('input_image')
    if not input_image:
        return jsonify({'error': 'Missing input image'}), 400

    try:
        # Call the Gradio client to process the image
        result = client.predict(input_image=handle_file(input_image), api_name="/predict")

        # Save the result to a file
        file_name = "result.png"
        with open(file_name, "wb") as f:  # Open in binary write mode
            f.write(result)  # Ensure `result` is bytes

        # Upload the file to GitHub
        with open(file_name, "rb") as f:  # Read the file in binary mode
            file_content = f.read()
            file_url = upload_to_github(file_name, file_content)

        return jsonify({'result_url': file_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

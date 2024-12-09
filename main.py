from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import requests
import os
import base64

app = Flask(__name__)

# Initialize Gradio client
client = Client("https://vamsi92-removebg.hf.space")

# GitHub Configuration
GITHUB_TOKEN = "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"  # Replace with your token
GITHUB_REPO = "vamsi92/RemoveBGAPI"  # Replace with your repo (e.g., vamsi92/image-results)
GITHUB_BRANCH = "main"  # Replace with your branch

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.args
    input_image = data.get('input_image')
    if not input_image:
        return jsonify({'error': 'Missing input image'}), 400

    try:
        # Generate result using Gradio API
        result = client.predict(input_image=handle_file(input_image), api_name="/predict")

        # Save result file path
        output_path = result  # This should point to the result file in /tmp
        filename = os.path.basename(output_path)

        # Read file content
        with open(output_path, 'rb') as f:
            content = f.read()

        # Upload the result to GitHub
        response = upload_to_github(filename, content)
        if response.status_code == 201:
            return jsonify({'message': 'File uploaded to GitHub successfully'}), 200
        else:
            return jsonify({'error': 'Failed to upload file to GitHub', 'details': response.json()}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def upload_to_github(filename, content):
    """
    Upload a file to GitHub after encoding in Base64.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    # Encode content in Base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    data = {
        "message": f"Upload {filename}",
        "content": encoded_content,  # Base64 encoded content
        "branch": GITHUB_BRANCH,
    }

    response = requests.put(url, json=data, headers=headers)
    return response

if __name__ == '__main__':
    app.run(debug=True)

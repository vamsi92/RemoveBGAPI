from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import os

app = Flask(__name__)

client = Client("https://vamsi92-removebg.hf.space")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.args
    input_image = data.get('input_image')
    if not input_image:
        return jsonify({'error': 'Missing input image'}), 400

    try:
        # Make the prediction using the Gradio API client
        result = client.predict(input_image=handle_file(input_image), api_name="/predict")

        # Log the result (file path)
        result_file_path = result.get("result")
        if result_file_path:
            print(f"Result file path: {result_file_path}")

            # Optionally, read the file content if you need to do something with it (e.g., return it)
            # For example, read the file and log its size or send it back to the client
            if os.path.exists(result_file_path):
                with open(result_file_path, 'rb') as f:
                    file_data = f.read()
                    print(f"File size: {len(file_data)} bytes")  # Log the file size
                    # You can also return the file or process it further here

            # Send back the file path or some other relevant response
            return jsonify({'result': result_file_path}), 200
        else:
            return jsonify({'error': 'No result file path returned from the prediction'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

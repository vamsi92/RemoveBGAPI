from doctest import debug

from flask import Flask,request,jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)

client = Client("https://vamsi92-removebg.hf.space")

@app.route('/predict',methods=['Post','Get'])
def predict():
    data = request.args
    input_image = data.get('input_image')
    if not input_image:
        return jsonify({'error':'Missing input image'}),400

    try:
        result = client.predict(input_image=handle_file(input_image),api_name="/predict")
        return jsonify({'result':result}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)
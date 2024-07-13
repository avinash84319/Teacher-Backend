from flask import Flask, request, jsonify
from model import answer_question
from json_parsor import generate_template
import logging
import requests

#setup logging
logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)

@app.route('/api/')
def hello():
    return "Welcome to Backend for teacherstudent"

@app.route('/api/question', methods=['POST'])
def question():
    try:
        data = request.get_json()
        text = data['text']
        config = data['config']
        template = generate_template(text, config)
        response = answer_question(template)
        return jsonify(response)
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"})


if __name__ == '__main__':  
   app.run()
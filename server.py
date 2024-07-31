from flask import Flask, request, jsonify
from database import *
from pdfparser import pdf_to_text
from generate_questions import generate_questions
import logging
import requests
from flask_cors import CORS, cross_origin
import base64


#setup logging
# logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route('/api/')
def hello():
    return "Welcome to Backend for teacherstudent"


@app.route('/api/sectionDetails', methods=['POST'])
def secStore():
    # try:
        result=True
        data = request.get_json()

        userid=str(data['user_id'])
        pdfid=str(data['pdf_id'])


        pdf=data["pdf_content"]                                    #extracting the pdf
        pdf = base64.b64decode(pdf)
        with open(f'./user_files/{userid+"-"+pdfid}.pdf', 'wb') as f:     #saving the pdf in the server(local) change to s3 bucket
            f.write(pdf)
                 
        path = f'./user_files/{userid+"-"+pdfid}.pdf'

        text=pdf_to_text(path)                                      #converting the pdf to text
        data['text']=text
        print(text)

        data=generate_questions(data)                               #generating questions from the text and storing in the data

        #store the pdf path or link in the database
        result=store_pdf(pdfid,path)


        # storing user pdf details in the database
        # result=result and store_user_pdf(userid,pdfid)

        # for i,section_data in enumerate(data['sections']):

        #     # storing the section details in the database
        #     result=result and store_section_info(pdfid+"/"+str(i),section_data)

        if result!=True:

            raise Exception(result)

        return jsonify({"message": "Section details stored","data":data})
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify({"error": "An error occurred"})


if __name__ == '__main__':  
   app.run(debug=True)
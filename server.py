from flask import Flask, request, jsonify
from database import *
from pdfparser import pdf_to_text
from generate_questions import generate_questions
import logging
import requests
from flask_cors import CORS, cross_origin
import base64
from auth import google_auth,profile
from gcpUpload import *
from model import check_model


#setup logging
# logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route('/')
def hellop():
    return "Welcome to Backend for teacherstudent"

@app.route('/api/')
def hello():
    return "Welcome to Backend for teacherstudent"

@app.route('/auth/google', methods=['POST'])
def google_a():
    data = request.json
    return google_auth(data)

@app.route('/api/profile', methods=['GET'])
def profile_a():
    auth_header = request.headers.get('Authorization')
    return profile(auth_header)

@app.route('/api/fetchFiles')
def fetchFiles():
    
    try:
        user_id = request.args.get('user_id')

        print(" getting files for user ",user_id)

        return jsonify({"user_id": user_id, "files": fetch_files(user_id)})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"})

@app.route('/api/fetchFileDetails')
def fetchFileDetails():
    try:
        pdf_id = request.args.get('pdf_id')

        pdf_url=get_pdf_path(pdf_id)

        print(" getting file details for pdf ",pdf_id)

        return jsonify({"pdf_id": pdf_id,"pdf_url":pdf_url,"sections": fetch_section_details(pdf_id)})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"})

@app.route('/api/deleteFile')
def deleteFile():
    try:
        pdf_id = request.args.get('pdf_id')

        print(" deleting file for pdf ",pdf_id)

        return jsonify({"pdf_id": pdf_id, "status": delete_pdf(pdf_id)})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"})



@app.route('/api/sectionDetails', methods=['POST'])
def secStore():
    # try:
        result=True
        data = request.get_json()

        userid=str(data['user_id'])
        pdfid=str(data['pdf_id'])


        pdf=data["pdf_content"]                                    #extracting the pdf
        pdf = base64.b64decode(pdf)
        with open(f'./user_files/{userid+"-"+pdfid}.pdf', 'wb') as f: 
            f.write(pdf)
                 
        path = f'./user_files/{userid+"-"+pdfid}.pdf'

        file_url=upload_blob(path,userid+"-"+pdfid+".pdf")                  #uploading the pdf to the gcp cloud storage and returning the url

        text=pdf_to_text(path)                                      #converting the pdf to text
        data['text']=text
        print(text)

        data=generate_questions(data)                               #generating questions from the text and storing in the data

        #store the pdf path or link in the database
        result=store_pdf(pdfid,file_url)


        #storing user pdf details in the database
        result=result and store_user_pdf(userid,pdfid,data['pdf_name'])

        for i,section_data in enumerate(data['sections']):

            # storing the section details in the database
            result=result and store_section_info(pdfid,pdfid+"/"+str(i),section_data)

        if result!=True:

            raise Exception(result)

        return jsonify({"message": "Section details stored","data":data})
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify({"error": "An error occurred"})


if __name__ == '__main__':
    
    # check if the tables are created
    result=create_db()
    if result!=True:
        logging.error(result)
        print(result)

    # check if model is ready
    result=check_model()
    if result!=True:
        logging.error(result)
    print(result)

    #check if the gcp bucket is ready
    result=check_bucket()
    if result!=True:
        logging.error(result)
        print(result)
    

    app.run(debug=True)
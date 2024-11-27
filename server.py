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

@app.route("/api/pdfupload",methods=['POST'])
def pdfupload():

    """
    This function is used to upload the pdf to the cloud storage and store the pdf path in the database
    :param: user_id,pdf_id,pdf_content,pdf_name
    """

    try:
        result=True
        data = request.get_json()

        pdf_name = str(data["pdf_name"])
        userid=str(data['user_id'])
        pdfid=str(data['pdf_id'])
        pdf=data["pdf_content"]                                     #extracting the pdf

        if userid=="" or pdfid=="" or pdf=="" or pdf_name=="":
            raise Exception("Please provide all the details")

        pdf = base64.b64decode(pdf)
        with open(f'./user_files/{userid+"-"+pdfid}.pdf', 'wb') as f: 
            f.write(pdf)
                 
        path = f'./user_files/{userid+"-"+pdfid}.pdf'

        file_url=upload_blob(path,userid+"-"+pdfid+".pdf")                  #uploading the pdf to the gcp cloud storage and returning the url

        #store the pdf path or link in the database
        result=store_pdf_path(userid,pdfid,file_url)

        print("SERVER:"+str(result))

        #storing user pdf details in the database
        result=result and store_user_pdf(userid,pdfid,pdf_name)

        print("SERVER:"+str(result))

        if result!=True:
            raise Exception(result)

        return jsonify({"message": "Pdf uploaded","file_url":file_url}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"}),500


@app.route('/api/sectionUpload', methods=['POST'])
def sectionUpload():
    try:
        result=True
        data = request.get_json()

        print("SERVER :-"+ str(data))

        userid=str(data['user_id'])

        sections_data = data['sections']

        for section in sections_data:
            section_id = section['section_id']

            # storing the section details in the database
            result=store_section_info(userid,section_id,section)

            if result!=True:
                raise Exception(result)

        if result!=True:
            raise Exception(result)

        return jsonify({"message": "Section details stored","data":data})
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})


@app.route('/api/createClass', methods=['POST'])
def createClass():
    try:
        data = request.get_json()
        result=True

        class_name=data['class_name']
        user_id=data['user_id']
        description=data['description']

        # storing the class details in the database
        id=creat_class(user_id,class_name,description)

        if id==False:
            raise Exception("An error occurred while creating the class")

        return jsonify({"message": "Class created","id":id})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

@app.route('/api/addstudent', methods=['GET'])
def addstudent():
    try:
        result=True
        class_id=request.args.get('class_id')
        student_name=request.args.get('student_name')

        # storing the student details in the database
        id=create_student(student_name,class_id)

        if id==False:
            raise Exception("An error occurred while adding the student")

        return jsonify({"message": "Student added","id":id})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

@app.route('/api/updateStudentAnalytics',methods=['POST'])
def update_analysis():

    try:
        data = request.get_json()
        
        studentid = data['student_id']
        analytics = data['student_json']

        id = update_analytics(studentid,analytics)

        if id==False:
            print(id)
            raise Exception("an error has occured adding analytics ")

        return jsonify({"message":"analytics added"})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

@app.route('/api/getStudentAnalytics',methods=['GET'])
def get_analysis():
    try:
        studentid = request.args.get('student_id')

        analytics = get_analytics(studentid)

        if analytics==False:
            raise Exception("an error has occured getting analytics ")

        return jsonify({"analytics":analytics})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

@app.route('/api/genereateQuestions',methods=['POST'])
def generateQuestions():
    try:
        data = request.get_json()
        userid = data['user_id']
        studentid = data['student_id']
        section_id = data['section_id']
        pdf_id = data['pdf_id']


        # get pdf path in gcp
        pdf_path = get_pdf_path(pdf_id)

        # get the text from the pdf
        text = get_pdf_text_from_gcp(pdf_path)

        # get the section details
        data = fetch_section_json(userid,section_id)

        # get the student analytics
        analytics = get_analytics(studentid)

        # generate the questions
        data = generate_questions(data,text,analytics)

        return jsonify({"data":data})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

        



if __name__ == '__main__':
    
    # check if the tables are created
    result=create_db()
    if result!=True:
        logging.error(result)
        print("SERVER:"+result)

    # check if model is ready
    result=check_model()
    if result!=True:
        logging.error(result)
        print("SERVER:"+result)

    #check if the gcp bucket is ready
    result=check_bucket()
    if result!=True:
        logging.error(result)
        print("SERVER:"+result)
    

    app.run(debug=True)
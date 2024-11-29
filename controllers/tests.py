from database import *
import logging
from flask import request,jsonify
from helper.generate_questions import generate_questions
from helper.gcpUpload import get_pdf_text_from_gcp

def createTest():
    try:
        data = request.get_json()
        result=True
        test_name=data['test_name']
        user_id=data['user_id']
        description=data['description']
        student_id=data['student_id']
        pdf_id=data['pdf_id']

        # storing the test details in the database
        id=add_test(user_id,student_id,pdf_id,test_name,description)

        if id==False:
            raise Exception("An error occurred while creating the test")

        return jsonify({"message": "Test created","id":id}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500

def generateQuestions():
    try:
        data = request.get_json()
        userid = data['user_id']
        studentid = data['student_id']
        section_id = data['section_id']
        pdf_id = data['pdf_id']
        test_id = data['test_id']

        print("SERVER :-"+ str(data))

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

        # store the questions in the testsection table
        add_test_section(test_id,section_id,data)

        return jsonify({"data":data}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500

def getTestSections():

    try:
        test_id = request.args.get('test_id')

        # first get the sections for the test from testsection table

        sections = get_test_sections(test_id)

        return jsonify({"sections":sections}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500
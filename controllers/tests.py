from database import *
import logging
from flask import request,jsonify
from helper.generate_questions import generate_questions
from helper.gcpUpload import get_pdf_text_from_gcp
import json

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
        
        print(f"SERVER :- test id at create test :- {id}")

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
        instruction = data['instruction']
        topics = data['topics']

        print(f"server :- testid:-{test_id}")

        # get pdf path in gcp
        pdf_path = get_pdf_path(pdf_id)

        # get the text from the pdf
        text = get_pdf_text_from_gcp(pdf_path)

        # get the section details
        data = fetch_section_json(userid,section_id)

        # get the student analytics
        analytics = get_analytics(studentid)

        # get previous test questions
        previous_questions = get_previous_test_questions(test_id)

        print("SERVER previous questions:-"+ str(data))

        # generate the questions
        data,questions = generate_questions(data,text,analytics,previous_questions,instruction,topics)

        # store the questions in the testsection table
        done = add_test_section(test_id,section_id,data)

        # store the questions in the question table
        for question in questions:
            add_question(question,section_id,test_id)

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

def getTestQuestions():
    
        try:

            result = []

            test_id = request.args.get('test_id')

            # get all the sections for the test from testsection table
            sections = get_test_sections(test_id)

            if sections==False:
                raise Exception("An error occurred while fetching the sections in the getTestQuestions function")

            for section in sections:
                

                # get the questions for the section from the question table
                questions = get_test_questions(test_id,section[2])

                if questions==False:
                    raise Exception("An error occurred while fetching the questions in the getTestQuestions function")

                # get section name using id
                section_name = fetch_section_details(section[2])[2]

                if section_name==False:
                    raise Exception("An error occurred while fetching the section name in the getTestQuestions function")

                question_ids = [question[0] for question in questions]

                result.append({"section":section[2],"name":section_name,"questions":question_ids})

            return jsonify({"sections":result}),200

        except Exception as e:
            logging.error(e)
            return jsonify({"error": "An error occurred " + str(e)}),500

def getTestSingleQuestion():
    try:
        question_id = request.args.get('question_id')

        question = get_single_question(question_id)

        question = json.loads(question)

        # remove the correct answer from the question
        question["correct_answer_index"]=""

        return jsonify({"question":question}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500

def submitQuestion():

    try:
        data = request.get_json()

        question_id = data['question_id']
        answer = data['answer']

        # store the answer in the database in question table by adding the student_answer field in json

        question = get_single_question(question_id)

        question = json.loads(question)

        question["student_answer"]=answer

        question = json.dumps(question)

        id = update_question(question_id,question)

        if id==False:
            raise Exception("An error occurred while submitting the question")

        return jsonify({"message": "Question submitted"}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500
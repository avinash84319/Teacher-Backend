from database import *
import logging
from flask import request,jsonify

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

def classes_teacher():

    try:
        user_id = request.args.get('user_id')

        classes = get_classes_teacher(user_id)

        return jsonify({"classes":classes})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)}),500

def students_class():

    try:
        class_id = request.args.get('class_id')

        students = get_students_class(class_id)

        return jsonify({"students":students})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

def classes_with_tests():

    try:
        classes = get_classes_with_tests()

        return jsonify({"classes":classes})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})
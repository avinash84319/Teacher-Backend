from database import *
import logging
from flask import request,jsonify

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

def students_all():
    try:
        students = get_all_students()

        if students==False:
            raise Exception("an error has occured getting students ")

        return jsonify({"students":students})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})

def getStudentwithtests():

    try:
        students = get_students_with_tests()

        if students==False:
            raise Exception("an error has occured getting students ")

        return jsonify({"students":students})

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred " + str(e)})
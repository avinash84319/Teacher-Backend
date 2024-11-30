from database import *
import logging
from flask import request,jsonify

def createAssignment():

    try:
        # Get the request data
        data= request.get_json()

        # Check if the request data is empty
        if not data:
            return jsonify({'error': 'No data provided'})

        # Get the assignment data from the request
        title = data['title']
        description = data['description']
        type = data['type']
        due_date = data['due_date']

        user_id = str(data['teacherId'])
        class_ids = data['classIds']
        student_ids = data['studentIds']

        # Create the assignment
        assignment_id = create_assignment(title,description,type,due_date,user_id,class_ids,student_ids)

        return jsonify({"message": "Assignment created successfully"}), 200

    except Exception as e:

        logging.error(e)
        return jsonify({"error": "An error occurred"}), 500
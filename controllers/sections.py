from database import *
import logging
from flask import request,jsonify

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
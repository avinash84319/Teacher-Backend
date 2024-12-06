from database import *
from helper.gcpUpload import upload_blob,get_pdf_text_from_gcp
import logging
from flask import request,jsonify
import base64
from helper.model import give_headings

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

        print("SERVER:"+pdf_name+" "+userid+" "+pdfid)
        if userid=="" or pdfid=="" or pdf=="" or pdf_name=="":
            raise Exception("Please provide all the details")

        pdf = base64.b64decode(pdf)
        with open(f'./user_files/{userid+"-"+pdfid}.pdf', 'wb') as f: 
            f.write(pdf)
                 
        path = f'./user_files/{userid+"-"+pdfid}.pdf'

        file_url=upload_blob(path,userid+"-"+pdfid+".pdf")                  #uploading the pdf to the gcp cloud storage and returning the url

        #store the pdf path or link in the database
        result=store_pdf_path(userid,pdfid,file_url)

        # get the headings from the pdfs
        text = get_pdf_text_from_gcp(file_url)

        # get headings json
        headings = give_headings(text)

        print("SERVER:"+str(result))

        #storing user pdf details in the database
        result=result and store_user_pdf(userid,pdfid,pdf_name)

        print("SERVER:"+str(result))

        if result!=True:
            raise Exception(result)

        return jsonify({"message": "Pdf uploaded","file_url":file_url,"headings":headings}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"}),500

def uploadMaterial():

    """
    This function is used to upload the material to the cloud storage and store the material path in the database
    :param: user_id,material_id,material_content,material_name
    """

    try:
        result=True
        data = request.get_json()

        user_id = str(data['teacherId'])
        class_ids = data['classIds']
        student_ids = data['studentIds']

        files = data['files']  #json array of files with filename,base64

        if user_id=="" or class_ids=="" or student_ids=="" or files=="":
            raise Exception("Please provide all the details")

        for file in files:
            material_name = file['fileName']
            material_content = file['base64']

            material_content = base64.b64decode(material_content)
            with open(f'./user_files/{user_id+"-"+material_name}', 'wb') as f: 
                f.write(material_content)
                    
            path = f'./user_files/{user_id+"-"+material_name}'

            file_url=upload_blob(path,user_id+"-"+material_name)                  #uploading the pdf to the gcp cloud storage and returning the url

            #store the pdf path or link in the database
            result=store_material_path(user_id,class_ids,student_ids,file_url)

            print("SERVER:"+str(result))

        if result!=True:
            raise Exception(result)

        return jsonify({"message": "Material uploaded","file_url":file_url}),200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": "An error occurred"}),500

def materials_class():
    
        """
        This function is used to get the materials for a class
        :param:

        """

        try:
            result=True
            data = request.get_json()

            user_id = str(data['teacherId'])
            class_id = str(data['classId'])

            if user_id=="" or class_id=="":
                raise Exception("Please provide all the details")

            materials = get_materials_for_class(user_id,class_id)

            return jsonify({"materials": materials}),200

        except Exception as e:
            logging.error(e)
            return jsonify({"error": "An error occurred"}),500
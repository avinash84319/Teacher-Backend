from database import *
from helper.gcpUpload import upload_blob
import logging
from flask import request,jsonify
import base64

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
import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values
import json

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

#damm please upload

mydb.autocommit = True

pool = mydb.cursor()

def create_db():

    database = os.getenv("DB_NAME")

    try:
        pool.execute("CREATE DATABASE IF NOT EXISTS "+database)
        pool.execute("USE "+database)
        pool.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR(255), name VARCHAR(255), email VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS passwords (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, password VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS sections (userid VARCHAR(255),sectionid VARCHAR(255) PRIMARY KEY, name VARCHAR(255), mcq TEXT, mc TEXT, ftb TEXT, tf TEXT, mtf TEXT, sub TEXT, pag TEXT,questions TEXT,easy INT,medium INT,hard INT,easyMarks INT,mediumMarks INT,hardMarks INT)")
        pool.execute("CREATE TABLE IF NOT EXISTS userpdfs (userid varchar(255), pdfid VARCHAR(255), pdfname VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS pdfpaths (userid varchar(255),pdfid VARCHAR(255), path TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS classes (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), class_name VARCHAR(255), description TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(255), class_id INT)")
        pool.execute("CREATE TABLE IF NOT EXISTS studentAnalytics (id INT AUTO_INCREMENT PRIMARY KEY, studentid INT, analytics TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS sectionjson (userid INT,sectionid TEXT,sectionjson TEXT)")

        return True

    except Exception as e:
        print(e)
        return e


def store_pdf_path(userid,pdf_id, pdf_path):
    try:
        result = pool.execute("INSERT INTO pdfpaths (userid,pdfid,path) VALUES (%s, %s, %s)", (userid,pdf_id,pdf_path))
        print(f"DATABASE: {result}")

    except Exception as e:
        return e

    return True

def store_user_pdf(user_id,pdf_id,pdf_name):
    try:

        # check if the pdf is already stored
        result = pool.execute("SELECT * FROM userpdfs WHERE userid = %s AND pdfid = %s", (user_id, pdf_id))
        print(f"DATABASE: {result}")
        if pool.fetchone():
            return True
        else:
            pool.execute("INSERT INTO userpdfs (userid, pdfid,pdfname) VALUES (%s, %s, %s)", (user_id, pdf_id, pdf_name))

    except Exception as e:
        return e

    return True

def store_section_info(userid,id,data):

    # check if the section is already stored and delete it
    pool.execute("SELECT * FROM sections WHERE userid = %s AND sectionid = %s", (userid, id))
    if pool.fetchone():
        pool.execute("DELETE FROM sections WHERE userid = %s AND sectionid = %s", (userid, id))

    name = data['name']
    mcq = data['mcq']
    mc = data['multipleChoice']
    ftb = data['fillInTheBlanks']
    tf = data['trueFalse']
    mtf = data['matchTheFollowing']
    sub = data['subjective']
    pag = data['paragraph']
    questions= data['questions']
    easy=data['easy']
    medium=data['medium']
    hard=data['hard']
    easyMarks=data['easyMarks']
    mediumMarks=data['mediumMarks']
    hardMarks=data['hardMarks']

    # convert all arrays into strings using json.stringify
    mcq = json.dumps(mcq)
    mc = json.dumps(mc)
    ftb = json.dumps(ftb)
    tf = json.dumps(tf)
    mtf = json.dumps(mtf)
    sub = json.dumps(sub)
    pag = json.dumps(pag)
    questions = json.dumps(questions)

    try:
        pool.execute("INSERT INTO sections (userid,sectionid,name, mcq, mc, ftb, tf, mtf, sub, pag,questions,easy,medium,hard,easyMarks,mediumMarks,hardMarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)", (userid,id,name, mcq, mc, ftb, tf, mtf, sub, pag,questions,easy,medium,hard,easyMarks,mediumMarks,hardMarks))
    except Exception as e:
        return e

    # directly store json for now

    try:

        data = json.dumps(data)

        pool.execute("INSERT INTO sectionjson (userid,sectionid,sectionjson) VALUES(%s,%s,%s)",(userid,id,data))
    except Exception as e:
        return e
    
    return True

def get_user(id):
    try:
        pool.execute("SELECT * FROM users WHERE id = %s", (id,))
        
        return pool.fetchone()

    except Exception as e:
        print(e)
        return False


def add_user(id,name, email):
    try:
        pool.execute("INSERT INTO users (id,name, email) VALUES (%s,%s,%s)", (id,name, email))

    except Exception as e:
        return e

    return True


def fetch_files(user_id):
    try:
        pool.execute("SELECT pdfid,pdfname FROM userpdfs WHERE userid = %s", (user_id,))

        files = pool.fetchall()

        # for every file , getting no of sections,and no of easy,medium and hard questions

        details = []
        for i in range(len(files)):
            pool.execute("SELECT * FROM sections WHERE userid = %s", (files[i][0],))
            sections = pool.fetchall()

            easy=0
            medium=0
            hard=0

            for section in sections:
                
                sectiondetails=[]
                # changing from strict to json

                data=json.loads(section[10])

                for question in data:
                    if question['difficulty']=='easy':
                        easy+=1
                    elif question['difficulty']=='medium':
                        medium+=1
                    elif question['difficulty']=='hard':
                        hard+=1

                sectiondetails.append({"section_name":section[1],"sectionid":section[0]})

            details.append({"pdfid":files[i][0],"pdfname":files[i][1],"easy":easy,"medium":medium,"hard":hard,"sections":sectiondetails})
                
        
        return details

    except Exception as e:
        print(e)
        return False


def fetch_section_details(userid,sectionid):
    try:
        print(sectionid)

        pool.execute("SELECT * FROM sections WHERE userid = %s and sectionid = %s", (userid,sectionid))
        
        details=pool.fetchall()

        print(details)

        for i in range(len(details)):
            details[i]=list(details[i])
            details[i][3]=json.loads(details[i][3])
            details[i][4]=json.loads(details[i][4])
            details[i][5]=json.loads(details[i][5])
            details[i][6]=json.loads(details[i][6])
            details[i][7]=json.loads(details[i][7])
            details[i][8]=json.loads(details[i][8])
            details[i][9]=json.loads(details[i][9])
            details[i][10]=json.loads(details[i][10])

        return details

    except Exception as e:
        print(e)
        return False

def fetch_section_json(user_id,section_id):

    try:

        print(user_id,section_id)

        pool.execute("SELECT sectionjson FROM sectionjson WHERE userid = %s and sectionid = %s", (user_id,section_id))
    
        details = pool.fetchall()

        details = {"sections":[json.loads(details[0][0])]}

        return details

    except Exception as e:
        print(e)
        return False



def delete_pdf(pdf_id):

    try:
        pool.execute("DELETE FROM userpdfs WHERE pdfid = %s", (pdf_id,))
        pool.execute("DELETE FROM sections WHERE pdfid = %s", (pdf_id,))
        pool.execute("DELETE FROM pdfs WHERE pdfid = %s", (pdf_id,))

    except Exception as e:
        return e

    return True


def get_pdf_path(pdf_id):
    try:
        pool.execute("SELECT path FROM pdfpaths WHERE pdfid = %s", (pdf_id,))

        return pool.fetchone()[0]

    except Exception as e:
        print(e)
        return False

def creat_class(user_id,class_name,description):

    try:
        result = pool.execute("INSERT INTO classes (user_id,class_name,description) VALUES (%s,%s,%s)", (user_id,class_name,description))

        # get the id of the class
        id = result.lastrowid

        return id

    except Exception as e:
        return False

def create_student(student_name,class_id):
    try:
        result = pool.execute("INSERT INTO students (student_name,class_id) VALUES (%s,%s)", (student_name,class_id))

        # get the id of the student
        id = result.lastrowid

        return id

    except Exception as e:
        return False

def update_analytics(studentid,analytics):
    try:
        analytics = json.dumps(analytics)

        result = pool.execute("INSERT INTO studentAnalytics (studentid,analytics) VALUES (%s,%s)",(studentid,analytics))

        # get the id of the student
        id = result.lastrowid

        return id

    except Exception as e:
        return e

def get_analytics(studentid):
    try:
        pool.execute("SELECT analytics FROM studentAnalytics WHERE studentid = %s",(studentid,))

        analytics = pool.fetchone()[0]

        return json.loads(analytics)

    except Exception as e:
        return False

def get_pdf_path(pdf_id):
    try:
        pool.execute("SELECT path FROM pdfpaths WHERE pdfid = %s", (pdf_id,))

        return pool.fetchone()[0]

    except Exception as e:
        print(e)
        return False








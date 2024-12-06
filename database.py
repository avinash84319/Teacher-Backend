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

pool = mydb.cursor(buffered=True)

def create_db():

    database = os.getenv("DB_NAME")

    try:
        pool.execute("CREATE DATABASE IF NOT EXISTS "+database)
        pool.execute("USE "+database)
        pool.execute("CREATE TABLE IF NOT EXISTS users (id INT, name VARCHAR(255), email VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS passwords (id INT AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), password VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS sections (userid VARCHAR(255),sectionid VARCHAR(255) PRIMARY KEY, name VARCHAR(255), mcq TEXT, mc TEXT, ftb TEXT, tf TEXT, mtf TEXT, sub TEXT, pag TEXT,questions TEXT,easy varchar(255),medium varchar(255),hard varchar(255),easyMarks varchar(255),mediumMarks varchar(255),hardMarks varchar(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS userpdfs (userid varchar(255), pdfid VARCHAR(255), pdfname VARCHAR(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS pdfpaths (userid varchar(255),pdfid VARCHAR(255), path TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS classes (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), class_name VARCHAR(255), description TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(255), class_id varchar(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS studentAnalytics (id INT AUTO_INCREMENT PRIMARY KEY, studentid varchar(255), analytics TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS sectionjson (userid varchar(255),sectionid TEXT,sectionjson TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS tests (id INT AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), student_id varchar(255), pdf_id TEXT, test_name VARCHAR(255), description TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS testsections (id INT AUTO_INCREMENT PRIMARY KEY, test_id varchar(255), section_id TEXT, sectiondata TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS questions (id INT AUTO_INCREMENT PRIMARY KEY, test_id varchar(255),section_id TEXT,question_json TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS materials (id INT AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), student_id TEXT, file_url TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS classMaterials (id INT AUTO_INCREMENT PRIMARY KEY,user_id TEXT, class_id varchar(255), file_url TEXT)")
        pool.execute("CREATE TABLE IF NOT EXISTS studentassignements (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, type VARCHAR(255), due_date DATE, student_id varchar(255))")
        pool.execute("CREATE TABLE IF NOT EXISTS classassignments (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, type VARCHAR(255), due_date DATE,user_id TEXT, class_id varchar(255), student_id varchar(255))")

        # other ui tables
        return True

    except Exception as e:
        print(e)
        return e


def store_pdf_path(userid,pdf_id, pdf_path):
    try:
        result = pool.execute("INSERT into pdfpaths (userid,pdfid,path) VALUES (%s, %s, %s)", (userid,pdf_id,pdf_path))
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
            pool.execute("INSERT into userpdfs (userid, pdfid,pdfname) VALUES (%s, %s, %s)", (user_id, pdf_id, pdf_name))

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
        pool.execute("INSERT into sections (userid,sectionid,name, mcq, mc, ftb, tf, mtf, sub, pag,questions,easy,medium,hard,easyMarks,mediumMarks,hardMarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)", (userid,id,name, mcq, mc, ftb, tf, mtf, sub, pag,questions,easy,medium,hard,easyMarks,mediumMarks,hardMarks))
    except Exception as e:
        return e

    # directly store json for now

    try:

        data = json.dumps(data)

        pool.execute("INSERT into sectionjson (userid,sectionid,sectionjson) VALUES(%s,%s,%s)",(userid,id,data))
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
        pool.execute("INSERT into users (id,name, email) VALUES (%s,%s,%s)", (id,name, email))

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

def fetch_section_details(sectionid):

    try:

        pool.execute("SELECT * FROM sections WHERE sectionid = %s", (sectionid,))

        details = pool.fetchall()

        return details[0]

    except Exception as e:
        print(e)
        return False

def fetch_section_json(user_id,section_id):

    try:

        print(user_id,section_id)

        pool.execute("SELECT sectionjson FROM sectionjson WHERE userid = %s and sectionid = %s", (user_id,section_id))

        print("after pool execute")

        details = pool.fetchall()

        print("in fetch section json" + str(details))

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
        results = pool.fetchall()  # Fetch all rows for the given pdf_id

        if results:
            # Handle duplicates or return the first one
            return results[0][0]  # or you can process all results
        else:
            return None  # No result found

    except Exception as e:
        print(e)
        return False

def creat_class(user_id,class_name,description):

    try:
        result = pool.execute("INSERT into classes (user_id,class_name,description) VALUES (%s,%s,%s)", (user_id,class_name,description))

        # get the id of the class
        id = result.lastrowid

        return id

    except Exception as e:
        return False

def create_student(student_name,class_id):
    try:
        result = pool.execute("INSERT into students (student_name,class_id) VALUES (%s,%s)", (student_name,class_id))

        # get the id of the student
        id = result.lastrowid

        return id

    except Exception as e:
        return False

def update_analytics(studentid,analytics):
    try:
        analytics = json.dumps(analytics)

        result = pool.execute("INSERT into studentAnalytics (studentid,analytics) VALUES (%s,%s)",(studentid,analytics))

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

def get_classes_teacher(user_id):
    try:
        pool.execute("SELECT * FROM classes WHERE user_id = %s", (user_id,))

        return pool.fetchall()

    except Exception as e:
        return False


def get_students_class(class_id):
    try:
        pool.execute("SELECT * FROM students WHERE class_id = %s", (class_id,))

        return pool.fetchall()

    except Exception as e:
        return False

def add_test(user_id,student_id,pdf_id,test_name,description):
    try:
        
        pool.execute("INSERT into tests (user_id,student_id,pdf_id,test_name,description) VALUES (%s,%s,%s,%s,%s)", (user_id,student_id,pdf_id,test_name,description))

        # get the id of the test with student_id and pdf_id

        pool.execute("SELECT id FROM tests WHERE user_id = %s AND student_id = %s AND pdf_id = %s", (user_id,student_id,pdf_id))

        result = pool.fetchone()

        id = result[-1]

        return id

    except Exception as e:
        print(e)
        return False

def add_test_section(test_id,section_id,section_data):
    try:

        print("DATABASE: adding test section: " + str(test_id) + " " + str(section_id) + " " )
        section_data = json.dumps(section_data)

        result = pool.execute("INSERT into testsections (test_id,section_id,sectiondata) VALUES (%s,%s,%s)", (test_id,section_id,section_data))

        return True

    except Exception as e:
        print("DATABASE at add_test_section: " + str(e))
        return False

def get_test_sections(test_id):
    try:

        pool.execute("SELECT * FROM testsections WHERE test_id = %s", (test_id,))

        return pool.fetchall()

    except Exception as e:
        print("DATABASE at get_test_sections: " + str(e))
        return False

def get_all_students():
    try:
        pool.execute("SELECT * FROM students")

        return pool.fetchall()

    except Exception as e:
        print("DATABASE at get_all_students: " + str(e))
        return False

def add_question(question,section_id,test_id):

    try:
        question = json.dumps(question)

        result = pool.execute("INSERT into questions (test_id,section_id,question_json) VALUES (%s,%s,%s)", (test_id,section_id,question))

        return True

    except Exception as e:
        print("DATABASE at add_question: " + str(e))
        return False

def get_test_questions(test_id,section_id):
    try:
        pool.execute("SELECT * FROM questions WHERE test_id = %s and section_id = %s", (test_id,section_id))

        return pool.fetchall()

    except Exception as e:
        return False

def get_single_question(question_id):

    try:
        pool.execute("SELECT * FROM questions WHERE id = %s", (question_id,))

        return pool.fetchall()[0][3]

    except Exception as e:
        return False

def update_question(question_id,question):
    
        try:
            question = json.dumps(question)
    
            pool.execute("UPDATE questions SET question_json = %s WHERE id = %s", (question,question_id))
    
            return True
    
        except Exception as e:
            return False

def store_material_path(user_id,class_ids,student_ids,file_url):
    try:

        for class_id in class_ids:

            # put in classMaterials

            pool.execute("INSERT into classMaterials (user_id,class_id,file_url) VALUES (%s,%s,%s)", (user_id,class_id,file_url))
            
            # get all students in the class

            pool.execute("SELECT * FROM students WHERE class_id = %s", (class_id,))

            students = pool.fetchall()

            for student in students:

                pool.execute("INSERT into materials (user_id,student_id,file_url) VALUES (%s,%s,%s)", (user_id,student[0],file_url))

        for student_id in student_ids:

            pool.execute("INSERT into materials (user_id,student_id,file_url) VALUES (%s,%s,%s)", (user_id,student_id,file_url))

        return True

    except Exception as e:
        print("Error at store_material_path: " + str(e))
        return False

def create_assignment(title,description,type,due_date,user_id,class_ids,student_ids):
    try:

        print(class_ids,student_ids)
        
        for class_id in class_ids:

            # get all students in the class

            pool.execute("SELECT * FROM students WHERE class_id = %s", (class_id,))

            students = pool.fetchall()

            for student in students:

                pool.execute("INSERT into studentassignements (title,description,type,due_date,student_id) VALUES (%s,%s,%s,%s,%s)", (title,description,type,due_date,student[0]))

        for student_id in student_ids:

            pool.execute("INSERT into classassignments (title,description,type,due_date,user_id,class_id,student_id) VALUES (%s,%s,%s,%s,%s,%s,%s)", (title,description,type,due_date,user_id,class_id,student_id))

        return True

    except Exception as e:
        print("Error at create_assignment: " + str(e))
        return False

def get_students_with_tests():

    try:
        pool.execute("SELECT * FROM students")

        students = pool.fetchall()

        res = []

        for student in students:

            pool.execute("SELECT * FROM tests WHERE student_id = %s", (student[0],))

            tests = pool.fetchall()

            res.append({"student":student,"tests":tests})

        return res

    except Exception as e:
        print("Error at get_students_with_tests: " + str(e))
        return False

def get_classes_with_tests():

    try:
        pool.execute("SELECT * FROM classes")

        classes = pool.fetchall()

        res = []

        for class_ in classes:

            # geeting all tests for the class

            # first get all students in the class
            pool.execute("SELECT * FROM students WHERE class_id = %s", (class_[0],))

            students = pool.fetchall()

            student_tests  = []

            for student in students:

                # get all tests for the student
                pool.execute("SELECT * FROM tests WHERE student_id = %s", (student[0],))

                tests = pool.fetchall()

                student_tests.append({"student":student[0],"tests":tests})

            tests = [stt["tests"] for stt in student_tests]

            # removing duplicates
            resl_tests = []
            for test in tests:
                for t in test:
                    if t not in resl_tests:
                        resl_tests.append(t)

            # summing up all the tests for the class
            res.append({"class":class_,"tests":resl_tests})

        return res

    except Exception as e:
        print("Error at get_classes_with_tests: " + str(e))
        return False

def get_previous_test_questions(test_id):
    try:
        pool.execute("SELECT * FROM questions WHERE test_id = %s", (test_id,))

        return pool.fetchall()

    except Exception as e:
        return False

def get_materials_for_class(user_id,class_id):
    try:
        pool.execute("SELECT * FROM classMaterials WHERE user_id = %s AND class_id = %s", (user_id,class_id))

        return pool.fetchall()

    except Exception as e:
        return False
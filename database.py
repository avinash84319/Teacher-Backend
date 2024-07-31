import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values
import json

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

mydb.autocommit = True

pool = mydb.cursor()

pool.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
pool.execute("CREATE TABLE IF NOT EXISTS passwords (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, password VARCHAR(255))")
pool.execute("CREATE TABLE IF NOT EXISTS sections (sectionid VARCHAR(255) PRIMARY KEY, name VARCHAR(255), mcq TEXT, mc TEXT, ftb TEXT, tf TEXT, mtf TEXT, sub TEXT, pag TEXT,questions Text)")
pool.execute("CREATE TABLE IF NOT EXISTS userpdfs (userid varchar(255), pdfid VARCHAR(255))")
pool.execute("CREATE TABLE IF NOT EXISTS pdfs (pdfid VARCHAR(255), path TEXT)")


def store_pdf(pdf_id, pdf_path):
    try:
        pool.execute("INSERT INTO pdfs (pdfid, path) VALUES (%s, %s)", (pdf_id, pdf_path))

    except Exception as e:
        return e

    return True

def store_user_pdf(user_id, pdf_id):
    try:
        pool.execute("INSERT INTO userpdfs (userid, pdfid) VALUES (%s, %s)", (user_id, pdf_id))

    except Exception as e:
        return e

    return True

def store_section_info(id,data):

    name = data['name']
    mcq = data['mcq']
    mc = data['multipleChoice']
    ftb = data['fillInTheBlanks']
    tf = data['trueFalse']
    mtf = data['matchTheFollowing']
    sub = data['subjective']
    pag = data['paragraph']
    questions= data['questions']

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
        pool.execute("INSERT INTO sections (sectionid,name, mcq, mc, ftb, tf, mtf, sub, pag,questions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id,name, mcq, mc, ftb, tf, mtf, sub, pag, questions))
    except Exception as e:
        return e
    
    return True







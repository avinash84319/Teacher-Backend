# Import necessary modules and packages
from flask import Flask, request, jsonify
import logging  # For logging errors
import requests  # For HTTP requests
from flask_cors import CORS, cross_origin  # For enabling CORS
import base64  # For encoding/decoding data
from helper.model import check_model  # For checking model readiness
from controllers import greet, materials, auth, sections, classes, students, tests  # Controller functions for routing

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# -------------------------------
# Define Routes and Handlers
# -------------------------------

# Root and Hello World routes
app.add_url_rule('/', 'hellop', greet.hellop, methods=['GET'])  # Simple hello endpoint
app.add_url_rule('/api', 'hello', greet.hello, methods=['GET'])  # Another hello endpoint for API

# Authentication routes
app.add_url_rule('/auth/google', 'google_a', auth.google_a, methods=['POST'])  # Google auth via POST
app.add_url_rule('/api/profile', 'profile_a', auth.profile_a, methods=['GET'])  # Get user profile

# Materials related routes
app.add_url_rule('/api/pdfupload', 'pdfupload', materials.pdfupload, methods=['POST'])  # Upload PDF

# Section management routes
app.add_url_rule('/api/sectionUpload', 'sectionUpload', sections.sectionUpload, methods=['POST'])  # Upload section data

# Class management routes
app.add_url_rule('/api/createClass', 'createClass', classes.createClass, methods=['POST'])  # Create new class
app.add_url_rule('/api/addstudent', 'addstudent', classes.addstudent, methods=['GET'])  # Add student to class

# Student analytics routes
app.add_url_rule('/api/updateStudentAnalytics', 'update_analysis', students.update_analysis, methods=['POST'])  # Update student analytics
app.add_url_rule('/api/getStudentAnalytics', 'get_analysis', students.get_analysis, methods=['GET'])  # Get student analytics

# Test management routes
app.add_url_rule('/api/createTest', 'createTest', tests.createTest, methods=['POST'])  # Create new test
app.add_url_rule('/api/generateQuestions', 'generateQuestions', tests.generateQuestions, methods=['POST'])  # Generate test questions
app.add_url_rule('/api/getTestSectionsData', 'getTestSections', tests.getTestSections, methods=['GET'])  # Get test sections data

# Class and Student retrieval routes
app.add_url_rule('/api/getTeachersClasses', 'classes_teacher', classes.classes_teacher, methods=['GET'])  # Get classes for teacher
app.add_url_rule('/api/getClassStudents', 'students_class', classes.students_class, methods=['GET'])  # Get students in a class

# -------------------------------
# Server Initialization and Checks
# -------------------------------

if __name__ == '__main__':
    
    # 1. Check if the database tables are created
    result = create_db()  # This will check if the database and tables are created
    if result != True:
        logging.error(result)  # Log the error if tables are not created
        print("SERVER: " + result)

    # 2. Check if the machine learning model is ready
    result = check_model()  # This checks if the model is loaded and ready
    if result != True:
        logging.error(result)  # Log the error if the model is not ready
        print("SERVER: " + result)

    # 3. Check if the Google Cloud Platform (GCP) bucket is ready
    result = check_bucket()  # This checks if the GCP bucket is configured correctly
    if result != True:
        logging.error(result)  # Log the error if the bucket is not ready
        print("SERVER: " + result)

    # Start the Flask app in debug mode
    app.run(debug=True)

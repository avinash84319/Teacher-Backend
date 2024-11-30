import logging
from flask import request,jsonify
from helper.auth_funcs import google_auth, profile

def google_a():
    data = request.json
    return google_auth(data)

def profile_a():
    auth_header = request.headers.get('Authorization')
    return profile(auth_header)

from flask import jsonify
import firebase_admin
from firebase_admin import credentials, auth
from database import *

# Initialize Firebase Admin SDK
cred = credentials.Certificate('gkey.json')
firebase_admin.initialize_app(cred)


def google_auth(data):

    print("data",data)
    id_token = data['result']["_tokenResponse"]["idToken"]

    if not id_token:
        return jsonify({"error": "ID token is missing"}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
        print("decoded_token",decoded_token)
        name=decoded_token['name']
        email=decoded_token['email']
        picture=decoded_token['picture']
        user_id=decoded_token['uid']

        # Check if user exists in the database
        user = get_user(user_id)

        if not user:
            # Add user to the database
            add_user(user_id,name,email)


        # You can perform additional user verification or database operations here

        return jsonify({"user_id":user_id,"name": name, "email": email, "picture": picture,"token":id_token}), 200
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        return jsonify({"error": e}), 401


def profile(auth_header):
    
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 400

    token = auth_header.split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        name = decoded_token.get('name')
        email = decoded_token.get('email')
        picture = decoded_token.get('picture')

        return jsonify({"name": name, "email": email, "photoURL": picture}), 200
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return jsonify({"error": "Unauthorized"}), 401

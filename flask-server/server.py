from flask import Flask, request, jsonify
from flask_cors import CORS
from api import get_gemini_response
#from ..DB import db_functions
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import DB.db_functions
from datetime import date
import uuid


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes


@app.route('/calendar', methods=['POST'])
def create_expected_data():
    
    # data = request.get_json()
    # start_time = data.get('start_time')
    # end_time = data.get('end_time')
    # title = data.get('title')


@app.route('/api/chrome_extension/insertvalue', methods=['POST'])
def handle_chrome_extension_data():
    data = request.get_json()
    # here the data will be a python dict and the keys we have are 
    # date, start_time, end_time, title and description
    # Process Chrome extension data
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    title = data.get('title')
    des = data.get('description')
    category = get_gemini_response(title, des)
    url = data.get('url')
    uid = data.get('uid')
    DB.db_functions.insert_visited(uid,url,start_time,end_time,date,category)
    print("Received data from Chrome extension:", data)
    return jsonify({"message": "Data from Chrome extension received successfully"}), 200

@app.route('/api/frontend/insert_user', methods=['POST'])
def handle_frontend_data():
    data = request.get_json()
    # Process frontend data for this case it is entering the user info to make the account
    Fname = data.get('FirstName')
    Lname = data.get('LastName')
    Email = data.get('Email')  # dont need 
    gid = data.get('GoogleID') #make it a unique identifier
    DOB = data.get('DOB') # I dont think we need this 
    uid = str(uuid.uuid4()) # we dont need 
    DB.db_functions.insert_user(uid,Fname, Lname, Email, gid, DOB) # I changed this bcz we need to store the uid with the user info as well
    print("Received data from frontend:", data)
    return jsonify({"message": "Data from frontend received successfully"}), 200

# this method will be used to send info from the backend to the frontend
@app.route('/api/total_time_each_category', methods=['GET'])
def send_data():
    # so far we decided to send the info 
    # total info per day
    today = date.today()
    DB.db_functions.get_total_time_per_category_per_day(today,uid)
    return jsonify()

    

if __name__ == "__main__":
    app.run(debug=True)

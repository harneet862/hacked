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
    data = request.get_json()
    for i in data:
        start_time = i.get('start_time')
        end_time = i.get('end_time')
        title = i.get('title')
        date = i.now()
        DB.db_functions.insert_expected(start_time, end_time, title, date)
    print("Received data from calendar")
    return jsonify({"message": "Data from calendar received successfully"}), 200
    
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
    DB.db_functions.insert_visited(url,start_time,end_time,date,category)
    print("Received data from Chrome extension:", data)
    return jsonify({"message": "Data from Chrome extension received successfully"}), 200

@app.route('/api/frontend/insert_user', methods=['POST'])
def handle_frontend_data():
    data = request.get_json()
    # Process frontend data for this case it is entering the user info to make the account
    Fname = data.get('FirstName')
    Lname = data.get('LastName') 
    gid = data.get('GoogleID') #make it a unique identifier
    DOB = data.get('DOB') # I dont think we need this 
    DB.db_functions.insert_user(Fname, Lname, gid, DOB) # I changed this bcz we need to store the uid with the user info as well
    print("Received data from frontend:", data)
    return jsonify({"message": "Data from frontend received successfully"}), 200

# this method will be used to send info from the backend to the frontend
@app.route('/api/expectedvsactual', methods=['GET'])
def send_data():
    event_date = date.today()
    ans = DB.db_functions.get_user_expected(event_date)
    # this should provide me with a set which has the values which are events which would be start_time, end_time, title, date
    for i in ans:
        if 
    # so far we decided to send the info 
    # total info per day
    
    DB.db_functions.get_total_time_per_category_per_day(today)
    return jsonify()

    

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from api import get_gemini_response_category
from api import get_gemini_response_bool
# from datetime import datetime, timedelta
#from dateutil.parser import parse
#from ..DB import db_functions
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import DB.db_functions
from datetime import date
import datetime 
import sqlite3
conn = sqlite3.connect('../DB/extension_db.db', check_same_thread=False)
cursor = conn.cursor()
user_Fname = "Karan"
user_lname = "Brar"

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/')
def new():
    return "Hello World"

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

# this one is working    
@app.route('/api/chrome_extension/insertvalue', methods=['POST'])
def handle_chrome_extension_data():
    print("ok",request.data)
    
    data = request.get_json()
    # here the data will be a python dict and the keys we have are 
    # date, start_time, end_time, title and description
    # Process Chrome extension data
    if data is None:
        return jsonify({"error": "'Log stored' key not found in the data"}), 400
    date = data.get('date')
    start_time = data.get('startTime')
    time_obj = datetime.datetime.strptime(str(start_time), "%H:%M:%S")
    formattedStartTime = time_obj.strftime("%H:%M")
    end_time = data.get('endTime')
    time_obj = datetime.datetime.strptime(str(end_time), "%H:%M:%S")
    formattedendTime = time_obj.strftime("%H:%M")
    title = data.get('title')
    des = data.get('description')
    category = get_gemini_response_category(title, des)
    url = data.get('url')
    DB.db_functions.insert_actual(cursor, url, title, formattedStartTime,formattedendTime,date,category)
    conn.commit()
    print("Received data from Chrome extension:", data)
    return jsonify({"message": "Data from Chrome extension received successfully"}), 200

@app.route('/api/frontend/insert_user', methods=['POST'])
def handle_frontend_data():
    data = request.get_json()
    # Process frontend data for this case it is entering the user info to make the account
    Fname = data.get('FirstName')
    Lname = data.get('LastName') 
    gid = data.get('GoogleID') #make it a unique identifier
    DB.db_functions.insert_user(cursor, Fname, Lname, gid) # I changed this bcz we need to store the uid with the user info as well
    print("Received data from frontend:", data)
    return jsonify({"message": "Data from frontend received successfully"}), 200

# this method will be used to send info from the backend to the frontend for rendering the calendar data 
@app.route('/api/expectedvsactual', methods=['GET'])
def send_data():
    event_date = date.today()
    expected = DB.db_functions.get_user_expected(str(event_date))  # Expected format: (title, start_time, end_time, date, category)
    actual = DB.db_functions.get_actual_expected(str(event_date))  # Actual format: (url, title, start_time, end_time, date, category)
    
    data = {"arr": []}
    
    for i in expected:
        proportion = 0
        i = list(i)
        
        start_time = i[1]
        end_time = i[2]
        
        # Convert to datetime objects to calculate time difference
        start_time_object = datetime.strptime(start_time, "%H:%M")
        end_time_object = datetime.strptime(end_time, "%H:%M")
        
        # Time given as total expected duration
        time_given = end_time_object - start_time_object
        total_seconds_given = time_given.total_seconds()

        for j in actual:
            j = list(j)
            actual_start = j[2]
            actual_end = j[3]
            
            # Convert actual times to datetime objects as well
            actual_start_object = datetime.strptime(actual_start, "%H:%M")
            actual_end_object = datetime.strptime(actual_end, "%H:%M")
            
            # Check for overlapping times between expected and actual times
            if (actual_start_object >= start_time_object and actual_end_object <= end_time_object) or \
               (actual_end_object <= end_time_object and actual_end_object >= start_time_object) or \
               (actual_start_object >= start_time_object and actual_start_object <= end_time_object):
                
                # Calculate actual time spent for overlapping segments
                if get_gemini_response_category(j[0], j[1], i[0]):    
                    overlap_start = max(start_time_object, actual_start_object)
                    overlap_end = min(end_time_object, actual_end_object)
                    
                    actual_time = overlap_end - overlap_start
                    total_seconds_actual = actual_time.total_seconds()
                    
                    # Calculate proportion of time spent
                    proportion += total_seconds_actual / total_seconds_given

        # Store the proportion for this event
        data["arr"].append({
            "start_time": start_time,
            "end_time": end_time,
            "proportion": proportion,
            "title": i[0]
        })
    
    return data
                

@app.route('/api/getusername', methods=['GET'])
def send_name():
    return (user_Fname, user_lname)


if __name__ == "__main__":
    app.run(debug=True)

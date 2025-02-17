from flask import Flask, request, jsonify
from flask_cors import CORS
from api import get_gemini_response_category
from api import get_gemini_response_bool
from datetime import datetime, timedelta
#from dateutil.parser import parse
#from ..DB import db_functions
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import DB.db_functions
from datetime import date
import datetime 
import subprocess
from events_caller import googleoath
import sqlite3
import random 

db_path =  "./extension_db.db"
connection = sqlite3.connect(db_path, check_same_thread = False)
cursor = connection.cursor()

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes


@app.route('/calendar', methods=['POST'])
def create_expected_data():
    data = request.get_json()
    # print("hello friends", data)
    for i in data:
        start_time = i.get("start_time")
        end_time = i.get('end_time')
        title = i.get('title')
        category="Social Media"
        date = datetime.datetime.now().date()
        DB.db_functions.insert_expected(cursor,title, start_time, end_time, date, category)
        connection.commit()
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
    connection.commit()
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

@app.route('/api/trigger-events-caller', methods=['GET'])
def trigger_events():
    """
    This endpoint triggers the Google OAuth login flow by running events_caller.py.
    Instead of redirecting, it returns a JSON response with an exit status.
    """
    try:
        googleoath()
        # subprocess.run(["python", "events_caller.py"], check=True)
        return jsonify({"status": 0, "message": "Google login successful"}), 200
    #except subprocess.CalledProcessError:
       # return jsonify({"status": 1, "message": "Google login failed"}), 500
    except Exception as e:
       return jsonify({"status": 1, "message": f"Google login failed: {str(e)}"}), 500

# this method will be used to send info from the backend to the frontend
@app.route('/api/expectedvsactual', methods=['GET'])
def send_data():
    event_date = date.today()
    # Hardcoded expected and actual event data
    expected = [
    {
        "EVENT_TITLE": "CS Lecture - Machine Learning",
        "StartTime": "09:00",
        "EndTime": "10:30",
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "EVENT_TITLE": "DSA Practice - LeetCode",
        "StartTime": "11:00",
        "EndTime": "12:30",
        "Date": "2025-02-17",
        "Category": "Productivity"
    },
    {
        "EVENT_TITLE": "Research Paper Reading",
        "StartTime": "13:00",
        "EndTime": "14:00",
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "EVENT_TITLE": "React Development - UniMeals",
        "StartTime": "14:30",
        "EndTime": "16:00",
        "Date": "2025-02-17",
        "Category": "Productivity"
    },
    {
        "EVENT_TITLE": "Gym Break - YouTube Workout Guide",
        "StartTime": "16:30",
        "EndTime": "17:00",
        "Date": "2025-02-17",
        "Category": "Fitness"
    },
    {
        "EVENT_TITLE": "Netflix - Relaxation Time",
        "StartTime": "18:00",
        "EndTime": "19:30",
        "Date": "2025-02-17",
        "Category": "Entertainment"
    },
    {
        "EVENT_TITLE": "Networking Course Study",
        "StartTime": "20:00",
        "EndTime": "21:30",
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "EVENT_TITLE": "Twitter/Reddit - Tech News",
        "StartTime": "22:00",
        "EndTime": "22:30",
        "Date": "2025-02-17",
        "Category": "News"
    }
    ]
    actual = [
    {
        "URL": "https://universityportal.com/ml-lecture",
        "TITLE": "CS Lecture - Machine Learning",
        "StartTime": "09:10",  # Started 10 mins late
        "EndTime": "10:40",    # Extended by 10 mins
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "URL": "https://leetcode.com/problemset",
        "TITLE": "DSA Practice - LeetCode",
        "StartTime": "11:15",  # Started late
        "EndTime": "12:15",    # Ended early
        "Date": "2025-02-17",
        "Category": "Productivity"
    },
    {
        "URL": "https://youtube.com/research-paper-summary",
        "TITLE": "Research Paper Video Summary",
        "StartTime": "13:00",
        "EndTime": "13:50",    # Shorter duration
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "URL": "https://github.com/unimeals",
        "TITLE": "React Development - UniMeals",
        "StartTime": "14:45",  # Started later
        "EndTime": "16:15",    # Extended
        "Date": "2025-02-17",
        "Category": "Productivity"
    },
    {
        "URL": "https://youtube.com/workout-routine",
        "TITLE": "Gym Break - Watching Workout Videos",
        "StartTime": "16:30",
        "EndTime": "17:15",    # Spent extra time watching
        "Date": "2025-02-17",
        "Category": "Fitness"
    },
    {
        "URL": "https://netflix.com",
        "TITLE": "Netflix - Binge Watching",
        "StartTime": "18:00",
        "EndTime": "20:00",    # Extended from 1.5 hours to 2 hours
        "Date": "2025-02-17",
        "Category": "Entertainment"
    },
    {
        "URL": "https://coursera.org/networks",
        "TITLE": "Networking Course Study",
        "StartTime": "20:15",  # Started later
        "EndTime": "21:20",    # Shortened
        "Date": "2025-02-17",
        "Category": "Education"
    },
    {
        "URL": "https://reddit.com/r/technology",
        "TITLE": "Browsing Reddit Tech News",
        "StartTime": "22:00",
        "EndTime": "22:45",    # Spent extra time
        "Date": "2025-02-17",
        "Category": "News"
    },
    {
        "URL": "https://youtube.com/shorts",
        "TITLE": "Watching Random YouTube Shorts",
        "StartTime": "22:45",
        "EndTime": "23:15",    # Unplanned activity
        "Date": "2025-02-17",
        "Category": "Entertainment"
    }
    ]
    
    data = {"arr": []}
    
    for i in expected:
        proportion = 0
        # Access time directly by key, not by converting dict to list
        start_time = i["StartTime"]
        end_time = i["EndTime"]
        
        # Convert to datetime objects to calculate time difference
        start_time_object = datetime.datetime.strptime(start_time, "%H:%M")
        end_time_object = datetime.datetime.strptime(end_time, "%H:%M")
        
        # Time given as total expected duration
        time_given = end_time_object - start_time_object
        total_seconds_given = time_given.total_seconds()

        for j in actual:
            actual_start = j["StartTime"]
            actual_end = j["EndTime"]
            
            # Convert actual times to datetime objects as well
            actual_start_object = datetime.datetime.strptime(actual_start, "%H:%M")
            actual_end_object = datetime.datetime.strptime(actual_end, "%H:%M")
            
            # Check for overlapping times between expected and actual times
            if (actual_start_object >= start_time_object and actual_end_object <= end_time_object) or \
               (actual_end_object <= end_time_object and actual_end_object >= start_time_object) or \
               (actual_start_object >= start_time_object and actual_start_object <= end_time_object):
                
                # Calculate actual time spent for overlapping segments
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
            "title": i["EVENT_TITLE"]
        })
    print(data)
    
    return data
                
@app.route('/api/frontendata', methods=['GET'])
def send_data_front_end():
    event_date = date.today()
    expected = DB.db_functions.get_user_expected(cursor, str(event_date)) 
    data = {"arr": []}
    for i in expected:
        i = list(i)
        start_time = i[1]
        end_time = i[2]
        title = i[0]
        data["arr"].append({
            "start_time": start_time,
            "end_time": end_time,
            "proportion": random.random(),
            "title": title
        })
    print(data)
    return data
        
    # so far we decided to send the info 
    # total info per day
    
    # DB.db_functions.get_total_time_per_category_per_day(today)
    # return jsonify()

    

if __name__ == "__main__":
    app.run(debug=True)

import sqlite3
from db_functions import insert_expected, insert_actual

def populate_database():
    # Connect to the database
    connection = sqlite3.connect('extension_db.db')
    cursor = connection.cursor()

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

    # Populate Expected table
    for event in expected:
        insert_expected(cursor, event['EVENT_TITLE'], event['StartTime'], event['EndTime'], event['Date'], event['Category'])

    # Populate Actual table
    for event in actual:
        insert_actual(cursor, event['URL'], event['TITLE'], event['StartTime'], event['EndTime'], event['Date'], event['Category'])

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print("Tables populated successfully!")

if __name__ == '__main__':
    populate_database()

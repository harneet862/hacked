import sqlite3

def insert_user(cursor, first_name, last_name, email, google_id, dob=None):
    query = """
    INSERT INTO Users (FirstName, LastName, Email, GoogleID, DOB)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (first_name, last_name, email, google_id, dob))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")

def insert_visited(cursor, uid, url, start_time, end_time, date, category):
    query = """
    INSERT INTO Visited (UID, URL, StartTime, EndTime, Date, Category)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (uid, url, start_time, end_time, date, category))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting visited entry: {e}")

def get_total_time_per_category_per_day(cursor, date, uid):
    query = """
    SELECT 
        Category,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE Date = ? AND UID = ?
    GROUP BY Category;
    """
    cursor.execute(query, (date, uid,))
    return cursor.fetchall()

def get_total_time_per_category_per_week(cursor, date, uid):
    query = """
    SELECT 
        Category,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', ?) AND UID = ?
    GROUP BY Category;
    """
    cursor.execute(query, (date, uid,))
    return cursor.fetchall()

def get_total_time_per_website_per_day(cursor, date, uid):
    query = """
    SELECT 
        URL,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE Date = ? AND UID = ?
    GROUP BY URL;
    """
    cursor.execute(query, (date, uid,))
    return cursor.fetchall()

def get_total_time_per_website_per_week(cursor, date, uid):
    query = """
    SELECT 
        URL,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', ?) AND UID = ?
    GROUP BY URL;
    """
    cursor.execute(query, (date, uid,))
    return cursor.fetchall()

def main():
    db_path = "extension_db.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    date = "2023-10-15"  # Example date, replace as needed
    
    print("Total Time per Category per Day:")
    for row in get_total_time_per_category_per_day(cursor, date, 4):
        print(row)
    print("\nTotal Time per Category per Week:")
    for row in get_total_time_per_category_per_week(cursor, date, 4):
        print(row)
    print("\nTotal Time per Website per Day:")
    for row in get_total_time_per_website_per_day(cursor, date, 4):
        print(row)
    print("\nTotal Time per Website per Week:")
    for row in get_total_time_per_website_per_week(cursor, date, 4):
        print(row)
    
    connection.close()

if __name__ == "__main__":
    main()

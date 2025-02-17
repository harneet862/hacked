import sqlite3

def insert_user(cursor, first_name, last_name, google_id):
    query = """
    INSERT INTO Users (FirstName, LastName, GoogleID)
    VALUES (?, ?, ?)
    """
    try:
        cursor.execute(query, (first_name, last_name,google_id))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")

def insert_actual(cursor, url, title, start_time, end_time, date, category):
    query = """
    INSERT INTO Actual ( URL, TITLE, StartTime, EndTime, Date, Category)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (url, title, start_time, end_time, date, category))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting visited entry: {e}")

def insert_expected(cursor, title, start_time, end_time, date, category):
    query = """
    INSERT INTO Expected ( EVENT_TITLE, StartTime, EndTime, Date, Category)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (title, start_time, end_time, date, category))
    except sqlite3.IntegrityError as e:
        print(f"Error inserting visited entry: {e}")
        
def get_total_time_per_category_per_day(cursor, date):
    query = """
    SELECT 
        Category,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE Date = ?
    GROUP BY Category;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

def get_total_time_per_category_per_week(cursor, date):
    query = """
    SELECT 
        Category,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', ?)
    GROUP BY Category;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

def get_total_time_per_website_per_day(cursor, date):
    query = """
    SELECT 
        URL,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE Date = ?
    GROUP BY URL;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

def get_total_time_per_website_per_week(cursor, date):
    query = """
    SELECT 
        URL,
        SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
        ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
    FROM Visited
    WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', ?)
    GROUP BY URL;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

def get_user_expected(cursor, date):
    query = """
    SELECT * FROM Expected
    WHERE Date = ?;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

def main():
    db_path = "extension_db.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    date = "2023-10-15"  # Example date, replace as needed
    
    print("Total Time per Category per Day:")
    for row in get_total_time_per_category_per_day(cursor, date):
        print(row)
    print("\nTotal Time per Category per Week:")
    for row in get_total_time_per_category_per_week(cursor, date):
        print(row)
    print("\nTotal Time per Website per Day:")
    for row in get_total_time_per_website_per_day(cursor, date):
        print(row)
    print("\nTotal Time per Website per Week:")
    for row in get_total_time_per_website_per_week(cursor, date):
        print(row)
    
    connection.close()

if __name__ == "__main__":
    main()

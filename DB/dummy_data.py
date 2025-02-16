import sqlite3
import random
from datetime import datetime, timedelta

def insert_dummy_data():
    conn = sqlite3.connect('extension_db.db')
    cursor = conn.cursor()

    # Insert Users
    users = [
        ('John', 'Doe', 'john.doe@example.com', 'google123', '1990-05-15'),
        ('Jane', 'Smith', 'jane.smith@example.com', 'google456', '1985-12-22'),
        ('Alice', 'Johnson', 'alice.j@example.com', 'google789', '1995-08-30'),
        ('Bob', 'Brown', 'bob.b@example.com', 'google111', '1992-03-10'),
        ('Charlie', 'Davis', 'charlie.d@example.com', 'google222', '1998-07-19')
    ]
    cursor.executemany('''
        INSERT INTO Users (FirstName, LastName, Email, GoogleID, DOB)
        VALUES (?, ?, ?, ?, ?)
    ''', users)

    # Insert Visited Data
    categories = ['Productivity', 
                'Education', 
                'Fitness', 
                'Entertainment', 
                'Social Media', 
                'Blogging', 
                'News', 
                'Travel',
                'Other']
    base_date = datetime(2023, 10, 1)
    visited = []
    
    for uid in range(1, 6):  # 5 users
        entries = 500 if uid == 1 else 50  # 500 entries for user 1, 50 for others
        for _ in range(entries):
            date = base_date + timedelta(days=random.randint(0, 30))
            start_time = datetime.combine(date, datetime.min.time()) + timedelta(
                hours=random.randint(6, 22), minutes=random.randint(0, 59))
            end_time = start_time + timedelta(minutes=random.randint(5, 60))
            category = random.choice(categories)
            url = f'https://example{random.randint(1, 100)}.com'
            visited.append((
                uid, 
                url, 
                start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                end_time.strftime('%Y-%m-%d %H:%M:%S'), 
                date.strftime('%Y-%m-%d'), 
                category
            ))
    
    cursor.executemany('''
        INSERT INTO Visited (UID, URL, StartTime, EndTime, Date, Category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', visited)

    conn.commit()
    conn.close()
    print("Large dummy dataset inserted successfully!")

if __name__ == '__main__':
    insert_dummy_data()
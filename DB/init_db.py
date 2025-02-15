import sqlite3

def init_db():
    # Connect to SQLite database (creates if not exists)
    conn = sqlite3.connect('extension_db.db')
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON')
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            GoogleID TEXT NOT NULL UNIQUE,
            DOB TEXT,
            CONSTRAINT email_unique UNIQUE (Email)
        )
    ''')
    
    # Create Visited table with category enum constraint
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Visited (
            UID INTEGER NOT NULL,
            URL TEXT NOT NULL,
            StartTime TEXT NOT NULL,
            EndTime TEXT NOT NULL,
            Date TEXT NOT NULL,
            Category TEXT CHECK(Category IN (
                'Productivity', 
                'Education', 
                'Fitness', 
                'Entertainment', 
                'Social Media', 
                'Blogging', 
                'News', 
                'Travel',
                'Other'
            )),
            FOREIGN KEY (UID) REFERENCES Users(ID)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

if __name__ == '__main__':
    init_db()
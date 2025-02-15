/* Sample queries */

/* Total Time per category per day */
-- Replace 'YYYY-MM-DD' with your target date
SELECT 
    Category,
    SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
    ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
FROM Visited
WHERE Date = 'YYYY-MM-DD'
GROUP BY Category;

/* Total time per category for a week */
-- Replace 'YYYY-MM-DD' with any date in your target week
SELECT 
    Category,
    SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
    ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
FROM Visited
WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', 'YYYY-MM-DD')
GROUP BY Category;

/* Total Time per Website per day */
-- Replace 'YYYY-MM-DD' with your target date
SELECT 
    URL,
    SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
    ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
FROM Visited
WHERE Date = 'YYYY-MM-DD'
GROUP BY URL;

/* Total Timer per Website per day */
-- Replace 'YYYY-MM-DD' with any date in your target week
SELECT 
    URL,
    SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS total_seconds,
    ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS total_hours
FROM Visited
WHERE strftime('%Y-%W', Date) = strftime('%Y-%W', 'YYYY-MM-DD')
GROUP BY URL;


/* Sample Execution of a query:
import sqlite3

def get_daily_categories(date):
    conn = sqlite3.connect('extension_db.db')
    cursor = conn.cursor()
    
    query = '''
        SELECT Category, 
               SUM(strftime('%s', EndTime) - strftime('%s', StartTime)) AS seconds,
               ROUND(SUM((strftime('%s', EndTime) - strftime('%s', StartTime)) / 3600.0), 2) AS hours
        FROM Visited
        WHERE Date = ?
        GROUP BY Category
    '''
    
    cursor.execute(query, (date,))
    results = cursor.fetchall()
    conn.close()
    return results

# Usage
daily_report = get_daily_categories('2023-10-05')
 */
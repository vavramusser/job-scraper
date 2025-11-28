import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time

# database setup
def init_db():
    """Initialize SQLite database with jobs table"""
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  company TEXT,
                  title TEXT,
                  url TEXT UNIQUE,
                  location TEXT,
                  description TEXT,
                  date_found TEXT,
                  is_new INTEGER DEFAULT 1)''')
    conn.commit()
    conn.close()

# store jobs in database
def store_jobs(jobs):
    """Store jobs in database, return list of new jobs"""
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    new_jobs = []
    
    # First, get today's date
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Mark all jobs that weren't found today as old (is_new = 0)
    c.execute('UPDATE jobs SET is_new = 0 WHERE date_found != ?', (today,))
    
    for job in jobs:
        try:
            c.execute('''INSERT INTO jobs (company, title, url, location, description, date_found)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (job['company'], job['title'], job['url'], 
                      job['location'], job.get('description', ''), job['date_found']))
            new_jobs.append(job)
        except sqlite3.IntegrityError:
            # Job already exists (duplicate URL)
            pass
    
    conn.commit()
    conn.close()
    return new_jobs
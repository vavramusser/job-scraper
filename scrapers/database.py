import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time

# database setup
def init_db():
    
    print("Initialize SQLite database with jobs table")
    
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  company TEXT,
                  title TEXT,
                  location TEXT,
                  salary_range TEXT,
                  date_open TEXT,
                  date_close TEXT,
                  date_found TEXT,
                  url TEXT UNIQUE,
                  is_new INTEGER DEFAULT 1)''')
    
    conn.commit()
    conn.close()

# store jobs in database
def store_jobs(jobs):

    print("Store jobs in database, return list of new jobs")

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    new_jobs = []
    
    # get today's date
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    
    # mark all jobs that weren't found today as old (is_new = 0)
    c.execute('UPDATE jobs SET is_new = 0 WHERE date_found != ?', (today,))
    
    for job in jobs:

        try:
            c.execute('''INSERT INTO jobs (company, title, url, location, date_found)
                        VALUES (?, ?, ?, ?, ?)''',
                     (job['company'], job['title'], job['url'], 
                      job['location'], job['date_found']))
            new_jobs.append(job)

        except sqlite3.IntegrityError:
            # job already exists (duplicate URL)
            pass
    
    conn.commit()
    conn.close()
    return new_jobs
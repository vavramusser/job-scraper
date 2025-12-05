from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_jobs():

    # get all jobs from database
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    
    c.execute('''SELECT company, title, location, url, date_found, is_new 
                 FROM jobs 
                 ORDER BY is_new DESC, date_found DESC''')
    
    jobs = c.fetchall()
    conn.close()
    
    # Convert to list of dictionaries for easier template access
    job_list = []
    for job in jobs:
        job_list.append({
            'company': job[0],
            'title': job[1],
            'location': job[2],
            'url': job[3],
            'date_found': job[4],
            'is_new': job[5]
        })
    
    return job_list

@app.route('/')
def index():
    """Main page showing all jobs"""
    print("Index route called!")
    jobs = get_jobs()
    
    new_jobs = [j for j in jobs if j['is_new'] == 1]
    old_jobs = [j for j in jobs if j['is_new'] == 0]
    
    return render_template('index.html', 
                        new_jobs=new_jobs, 
                        old_jobs=old_jobs,
                        total_count=len(jobs))

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, port=5000)
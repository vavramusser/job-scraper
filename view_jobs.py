import sqlite3
from datetime import datetime

def view_jobs():
    """View all jobs in database, with new jobs at the top"""
    
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    
    # Get all jobs, ordered by is_new (1 first) then by date_found (newest first)
    c.execute('''SELECT company, title, location, url, date_found, is_new 
                 FROM jobs 
                 ORDER BY is_new DESC, date_found DESC''')
    
    jobs = c.fetchall()
    conn.close()
    
    if not jobs:
        print("No jobs in database yet.")
        return
    
    print(f"\n{'='*80}")
    print(f"JOBS IN DATABASE: {len(jobs)} total")
    print(f"{'='*80}\n")
    
    new_count = sum(1 for job in jobs if job[5] == 1)
    old_count = len(jobs) - new_count
    
    print(f"NEW jobs: {new_count}")
    print(f"Previously seen: {old_count}\n")
    
    # Display new jobs first
    if new_count > 0:
        print(f"\n{'='*80}")
        print("NEW JOBS")
        print(f"{'='*80}\n")
        
        for job in jobs:
            if job[5] == 1:  # is_new
                print(f"Company: {job[0]}")
                print(f"Title: {job[1]}")
                print(f"Location: {job[2]}")
                print(f"Date Found: {job[4]}")
                print(f"URL: {job[3]}")
                print(f"{'-'*80}\n")
    
    # Display old jobs
    if old_count > 0:
        print(f"\n{'='*80}")
        print("PREVIOUSLY SEEN JOBS")
        print(f"{'='*80}\n")
        
        for job in jobs:
            if job[5] == 0:  # not new
                print(f"Company: {job[0]}")
                print(f"Title: {job[1]}")
                print(f"Location: {job[2]}")
                print(f"Date Found: {job[4]}")
                print(f"URL: {job[3]}")
                print(f"{'-'*80}\n")

def mark_all_as_seen():
    """Mark all jobs as seen (is_new = 0)"""
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('UPDATE jobs SET is_new = 0')
    conn.commit()
    rows_updated = c.rowcount
    conn.close()
    print(f"Marked {rows_updated} jobs as seen.")

if __name__ == "__main__":
    view_jobs()
    
    # Uncomment the line below if you want to mark all jobs as "seen" after viewing
    # mark_all_as_seen()
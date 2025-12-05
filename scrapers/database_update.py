import sqlite3

def add_description_column():
    """Add description column to existing database"""
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    
    try:
        # Check if column already exists
        c.execute("PRAGMA table_info(jobs)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'description' not in columns:
            c.execute('ALTER TABLE jobs ADD COLUMN description TEXT')
            conn.commit()
            print("Added 'description' column to database")
        else:
            print("'description' column already exists")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    add_description_column()
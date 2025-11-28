import sqlite3
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("SELECT COUNT(*), SUM(is_new) FROM jobs")
total, new_count = c.fetchone()
print(f"Total jobs: {total}, New jobs: {new_count}, Old jobs: {total - (new_count or 0)}")

c.execute("SELECT title, is_new FROM jobs LIMIT 5")
for row in c.fetchall():
    print(f"  {row[0]}: is_new={row[1]}")
conn.close()
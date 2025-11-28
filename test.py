import sqlite3
conn = sqlite3.connect('jobs.db')
c = conn.cursor()

# Check Abt descriptions
c.execute("SELECT title, length(description) FROM jobs WHERE company='Abt Global' LIMIT 3")
print("Abt Global jobs:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]} characters")

# Check PHI descriptions for comparison
c.execute("SELECT title, length(description) FROM jobs WHERE company='PHI' LIMIT 3")
print("\nPHI jobs:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]} characters")

conn.close()
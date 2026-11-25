"""Q3: Import users (name,email) from CSV into SQLite with validation + dedupe."""
import csv, re, sqlite3, sys

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def import_csv(csv_path, db_path="users.db"):
    ok = bad = 0
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                name, email = (row.get("name") or "").strip(), (row.get("email") or "").strip().lower()
                if not name or not EMAIL.match(email):
                    bad += 1; print(f"[skip] invalid row: {row}"); continue
                cur = conn.execute("INSERT OR IGNORE INTO users(name,email) VALUES (?,?)", (name, email))
                ok += cur.rowcount
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    print(f"inserted={ok} skipped_invalid={bad} total_in_db={total}")

if __name__ == "__main__":
    import_csv(sys.argv[1] if len(sys.argv) > 1 else "users.csv")

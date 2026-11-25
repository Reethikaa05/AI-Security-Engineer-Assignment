"""Q1: Fetch books from a REST API -> store in SQLite -> display.
API: Open Library search (no key needed). Falls back to bundled sample data if offline."""
import sqlite3, requests

API = "https://openlibrary.org/search.json"
DB = "books.db"
SAMPLE = [
    {"title": "Clean Code", "author_name": ["Robert C. Martin"], "first_publish_year": 2008},
    {"title": "Designing Data-Intensive Applications", "author_name": ["Martin Kleppmann"], "first_publish_year": 2017},
    {"title": "The Pragmatic Programmer", "author_name": ["Andrew Hunt"], "first_publish_year": 1999},
]

def fetch_books(query="python", limit=10):
    try:
        r = requests.get(API, params={"q": query, "limit": limit,
                         "fields": "title,author_name,first_publish_year"}, timeout=10)
        r.raise_for_status()
        return r.json().get("docs", [])
    except requests.RequestException as e:
        print(f"[warn] API unreachable ({e.__class__.__name__}); using sample data")
        return SAMPLE

def init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, author TEXT, year INTEGER,
        UNIQUE(title, author))""")

def store(conn, books):
    rows = [(b.get("title"), ", ".join(b.get("author_name", ["Unknown"])),
             b.get("first_publish_year")) for b in books if b.get("title")]
    # parameterised query -> no SQL injection; INSERT OR IGNORE -> idempotent re-runs
    conn.executemany("INSERT OR IGNORE INTO books(title,author,year) VALUES (?,?,?)", rows)
    conn.commit()

def display(conn):
    print(f"{'ID':<4}{'Title':<45}{'Author':<25}{'Year'}")
    print("-" * 82)
    for i, t, a, y in conn.execute("SELECT id,title,author,year FROM books ORDER BY year"):
        print(f"{i:<4}{t[:43]:<45}{a[:23]:<25}{y}")

if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        init_db(conn)
        store(conn, fetch_books())
        display(conn)

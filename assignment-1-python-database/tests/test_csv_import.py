import sqlite3, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from q3_csv_import import import_csv

def test_import_validates_and_dedupes(tmp_path):
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("name,email\nAsha,asha@example.com\nRavi,RAVI@example.com\n"
                        "Bad,not-an-email\nAsha,asha@example.com\n")
    db = tmp_path / "u.db"
    import_csv(str(csv_file), str(db))
    rows = sqlite3.connect(db).execute("SELECT name,email FROM users ORDER BY id").fetchall()
    assert rows == [("Asha", "asha@example.com"), ("Ravi", "ravi@example.com")]

def test_import_is_idempotent(tmp_path):
    csv_file = tmp_path / "users.csv"; csv_file.write_text("name,email\nAsha,asha@example.com\n")
    db = tmp_path / "u.db"
    import_csv(str(csv_file), str(db)); import_csv(str(csv_file), str(db))
    assert sqlite3.connect(db).execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1

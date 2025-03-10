import duckdb
import hashlib

DB_PATH = "database/security.db"  # ✅ Consistent database file name

def verify_user(username: str, password: str) -> bool:
    """Authenticates a user in DuckDB."""
    con = duckdb.connect(DB_PATH)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    result = con.execute("SELECT COUNT(*) FROM users WHERE username=? AND password_hash=?", 
                          (username, hashed_password)).fetchone()[0]
    
    con.close()

    if result > 0:
        print(f"Authentication successful for user '{username}'")
        return True  
    else:
        print(f"Authentication failed for user '{username}'")
        return False  


def create_user(username: str, password: str) -> None:
    """Creates a new user in DuckDB with a hashed password, preventing duplicates."""
    conn = duckdb.connect(DB_PATH)

    existing_user = conn.execute("SELECT COUNT(*) FROM users WHERE username=?", [username]).fetchone()[0]

    if existing_user > 0:
        print(f"Error: Username '{username}' already exists!")
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, hashed_password])
        print(f"User '{username}' created successfully!")

    conn.close()


def create_user_database() -> None:
    """Creates the users table if it does not exist."""
    conn = duckdb.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT  -- Store hashed passwords
        )
    """)

    conn.close()
    print("User database initialized!")

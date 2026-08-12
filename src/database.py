import sqlite3


def connect_database(db_path):
    """
    Open a SQLite database connection and enable foreign key enforcement.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(cursor):
    """
    Create the database tables required by Attack Surface Notebook.
    """

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS endpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            path TEXT NOT NULL,
            UNIQUE(method, path)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authentication (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint_id INTEGER NOT NULL,
            scheme_name TEXT NOT NULL,
            FOREIGN KEY (endpoint_id) REFERENCES endpoints(id),
            UNIQUE(endpoint_id, scheme_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            required INTEGER NOT NULL,
            FOREIGN KEY (endpoint_id) REFERENCES endpoints(id),
            UNIQUE(endpoint_id, name, location)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint_id INTEGER NOT NULL,
            signal TEXT NOT NULL,
            FOREIGN KEY (endpoint_id) REFERENCES endpoints(id),
            UNIQUE(endpoint_id, signal)
        )
    """)


def save_endpoint(cursor, method, path):
    """
    Save an endpoint and return its database ID.

    If the endpoint already exists, return the existing ID.
    """
    cursor.execute(
        "INSERT OR IGNORE INTO endpoints (method, path) VALUES (?, ?)",
        (method, path)
    )

    cursor.execute(
        "SELECT id FROM endpoints WHERE method = ? AND path = ?",
        (method, path)
    )

    row = cursor.fetchone()
    return row[0]


def save_authentication(cursor, endpoint_id, scheme_name):
    """
    Save an authentication scheme for an endpoint.
    Duplicate endpoint/scheme pairs are ignored.
    """
    cursor.execute(
        """
        INSERT OR IGNORE INTO authentication (endpoint_id, scheme_name)
        VALUES (?, ?)
        """,
        (endpoint_id, scheme_name)
    )

def save_parameter(cursor, endpoint_id, name, location, required):

    cursor.execute(
        """
        INSERT OR IGNORE INTO parameters (endpoint_id, name, location, required)
        VALUES (?, ?, ?, ?)
        """,
        (endpoint_id, name, location, required)
    )


def save_review_signal(cursor, endpoint_id, signal):

    cursor.execute(
        """
        INSERT OR IGNORE INTO review_signals (endpoint_id, signal)
        VALUES (?, ?)
        """,
        (endpoint_id, signal)
    )

def save_analysis_result(cursor, result):
    endpoint_id = save_endpoint(
        cursor,
        result["method"],
        result["path"]
    )

    for scheme in result.get("security", []):
        save_authentication(
            cursor,
            endpoint_id,
            scheme
        )

    for param in result.get("parameters", []):
        save_parameter(
            cursor=cursor,
            endpoint_id=endpoint_id,
            name=param["name"],
            location=param["in"],
            required=param["required"]
        )

    for signal in result.get("signals", []):
        save_review_signal(
            cursor,
            endpoint_id,
            signal
        )
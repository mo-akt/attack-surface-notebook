import sqlite3

from src.database import (
    create_tables,
    save_endpoint,
    save_authentication,
    save_parameter,
    save_review_signal,
    save_analysis_result,
)

def create_test_database():
    """Create an isolated in-memory database for each test."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    create_tables(cursor)

    return conn, cursor


def test_save_new_endpoint():
    """A new endpoint should be stored and its ID returned."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "GET",
        "/users/{id}"
    )

    cursor.execute(
        "SELECT id, method, path FROM endpoints"
    )
    row = cursor.fetchone()

    assert endpoint_id == row[0]
    assert row[1] == "GET"
    assert row[2] == "/users/{id}"

    conn.close()


def test_save_existing_endpoint_returns_same_id():
    """Saving the same endpoint twice should not create a duplicate."""
    conn, cursor = create_test_database()

    first_id = save_endpoint(
        cursor,
        "GET",
        "/users/{id}"
    )

    second_id = save_endpoint(
        cursor,
        "GET",
        "/users/{id}"
    )

    cursor.execute(
        "SELECT COUNT(*) FROM endpoints"
    )
    count = cursor.fetchone()[0]

    assert first_id == second_id
    assert count == 1

    conn.close()
def test_save_authentication():
    """Authentication scheme should be linked to the correct endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "GET",
        "/profile"
    )

    save_authentication(
        cursor,
        endpoint_id,
        "BearerAuth"
    )

    cursor.execute(
        "SELECT endpoint_id, scheme_name FROM authentication"
    )
    row = cursor.fetchone()

    assert row == (endpoint_id, "BearerAuth")

    conn.close()


def test_duplicate_authentication_is_ignored():
    """The same authentication scheme should not be duplicated for one endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "GET",
        "/profile"
    )

    save_authentication(cursor, endpoint_id, "BearerAuth")
    save_authentication(cursor, endpoint_id, "BearerAuth")

    cursor.execute(
        "SELECT COUNT(*) FROM authentication"
    )
    count = cursor.fetchone()[0]

    assert count == 1

    conn.close()

def test_save_parameter():
    """Parameter should be linked to the correct endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "GET",
        "/users/{id}"
    )

    save_parameter(
        cursor,
        endpoint_id,
        "id",
        "path",
        True
    )

    cursor.execute(
        """
        SELECT endpoint_id, name, location, required
        FROM parameters
        """
    )
    row = cursor.fetchone()

    assert row == (endpoint_id, "id", "path", 1)

    conn.close()


def test_duplicate_parameter_is_ignored():
    """The same parameter should not be duplicated for one endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "GET",
        "/users/{id}"
    )

    save_parameter(cursor, endpoint_id, "id", "path", True)
    save_parameter(cursor, endpoint_id, "id", "path", True)

    cursor.execute("SELECT COUNT(*) FROM parameters")
    count = cursor.fetchone()[0]

    assert count == 1

    conn.close()


def test_save_review_signal():
    """Review signal should be linked to the correct endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "DELETE",
        "/admin/users/{id}"
    )

    save_review_signal(
        cursor,
        endpoint_id,
        "destructive-operation"
    )

    cursor.execute(
        """
        SELECT endpoint_id, signal
        FROM review_signals
        """
    )
    row = cursor.fetchone()

    assert row == (endpoint_id, "destructive-operation")

    conn.close()


def test_duplicate_review_signal_is_ignored():
    """The same review signal should not be duplicated for one endpoint."""
    conn, cursor = create_test_database()

    endpoint_id = save_endpoint(
        cursor,
        "DELETE",
        "/admin/users/{id}"
    )

    save_review_signal(cursor, endpoint_id, "destructive-operation")
    save_review_signal(cursor, endpoint_id, "destructive-operation")

    cursor.execute("SELECT COUNT(*) FROM review_signals")
    count = cursor.fetchone()[0]

    assert count == 1

    conn.close()

def test_save_analysis_result():
    """Store a complete endpoint analysis with all related records."""
    conn, cursor = create_test_database()

    result = {
        "method": "DELETE",
        "path": "/admin/users/{id}",
        "security": ["BearerAuth"],
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "required": True
            }
        ],
        "signals": [
            "user-data",
            "admin-surface",
            "destructive-operation"
        ]
    }

    save_analysis_result(cursor, result)

    # Verify the endpoint.
    cursor.execute(
        "SELECT id, method, path FROM endpoints"
    )
    endpoint = cursor.fetchone()

    endpoint_id = endpoint[0]

    assert endpoint[1] == "DELETE"
    assert endpoint[2] == "/admin/users/{id}"

    # Verify authentication.
    cursor.execute(
        """
        SELECT endpoint_id, scheme_name
        FROM authentication
        """
    )
    authentication = cursor.fetchone()

    assert authentication == (
        endpoint_id,
        "BearerAuth"
    )

    # Verify the parameter.
    cursor.execute(
        """
        SELECT endpoint_id, name, location, required
        FROM parameters
        """
    )
    parameter = cursor.fetchone()

    assert parameter == (
        endpoint_id,
        "id",
        "path",
        1
    )

    # Verify review signals.
    cursor.execute(
        """
        SELECT signal
        FROM review_signals
        WHERE endpoint_id = ?
        ORDER BY signal
        """,
        (endpoint_id,)
    )

    signals = [
        row[0]
        for row in cursor.fetchall()
    ]

    assert signals == [
        "admin-surface",
        "destructive-operation",
        "user-data"
    ]

    conn.close()
from datetime import datetime

from app.db.database import get_connection, initialize_database


def create_ticket(
    problem: str,
    category: str = "General",
    priority: str = "Medium",
) -> dict:
    """
    Create and persist a new helpdesk ticket.
    """

    initialize_database()

    problem = problem.strip()
    category = category.strip() or "General"
    priority = priority.strip() or "Medium"

    if not problem:
        raise ValueError("Problem description cannot be empty.")

    valid_priorities = {"Low", "Medium", "High", "Critical"}

    if priority not in valid_priorities:
        priority = "Medium"

    created_at = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tickets (
            ticket_id,
            problem,
            category,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "TEMP",
            problem,
            category,
            priority,
            "Open",
            created_at,
        ),
    )

    database_id = cursor.lastrowid
    ticket_id = f"HD-{1000 + database_id}"

    connection.execute(
        """
        UPDATE tickets
        SET ticket_id = ?
        WHERE id = ?
        """,
        (ticket_id, database_id),
    )

    connection.commit()

    row = connection.execute(
        """
        SELECT *
        FROM tickets
        WHERE id = ?
        """,
        (database_id,),
    ).fetchone()

    connection.close()

    return dict(row)


def list_tickets() -> list[dict]:
    """
    Return all helpdesk tickets, newest first.
    """

    initialize_database()

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM tickets
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_ticket(ticket_id: str) -> dict | None:
    """
    Return a single ticket by ticket ID.
    """

    initialize_database()

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,),
    ).fetchone()

    connection.close()

    return dict(row) if row else None

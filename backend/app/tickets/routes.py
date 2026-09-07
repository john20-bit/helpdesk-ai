from fastapi import APIRouter

from app.db.database import get_connection


router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"],
)


@router.get("")
def get_tickets():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                ticket_id,
                problem,
                category,
                priority,
                status,
                created_at
            FROM tickets
            ORDER BY id DESC
            """
        ).fetchall()

        return {
            "success": True,
            "count": len(rows),
            "tickets": [
                {
                    "id": row["id"],
                    "ticket_number": row["ticket_id"],
                    "problem": row["problem"],
                    "category": row["category"],
                    "priority": row["priority"],
                    "status": row["status"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ],
        }

    finally:
        connection.close()

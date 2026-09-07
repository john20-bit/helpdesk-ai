from app.tickets.service import create_ticket as save_ticket


def create_helpdesk_ticket(
    problem: str,
    category: str = "General",
    priority: str = "Medium",
) -> dict:
    """
    Agent tool for creating a persistent helpdesk ticket.
    """

    ticket = save_ticket(
        problem=problem,
        category=category,
        priority=priority,
    )

    return {
        "tool": "create_helpdesk_ticket",
        "success": True,
        "ticket": ticket,
    }

from app.ai.assistant import generate_helpdesk_response
from app.tools.diagnostics import (
    check_internet,
    check_network,
    check_system,
)
from app.tools.tickets import create_helpdesk_ticket


def detect_category(problem: str) -> str:
    text = problem.lower()

    network_keywords = [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "router",
        "connection",
        "connected but",
        "no internet",
    ]

    printer_keywords = [
        "printer",
        "printing",
        "print",
        "scanner",
    ]

    bluetooth_keywords = [
        "bluetooth",
        "wireless mouse",
        "wireless keyboard",
        "headphone",
        "headphones",
        "speaker",
    ]

    software_keywords = [
        "software",
        "application",
        "app",
        "program",
        "install",
        "installation",
        "crash",
        "not responding",
    ]

    system_keywords = [
        "windows",
        "laptop slow",
        "computer slow",
        "pc slow",
        "system slow",
        "freezing",
    ]

    if any(keyword in text for keyword in network_keywords):
        return "Network"

    if any(keyword in text for keyword in printer_keywords):
        return "Printer"

    if any(keyword in text for keyword in bluetooth_keywords):
        return "Bluetooth"

    if any(keyword in text for keyword in software_keywords):
        return "Software"

    if any(keyword in text for keyword in system_keywords):
        return "System"

    return "General"


def select_tools(category: str) -> list[str]:
    if category == "Network":
        return [
            "check_internet",
            "check_network",
        ]

    if category in {"Software", "System"}:
        return ["check_system"]

    if category in {"Printer", "Bluetooth"}:
        return ["check_system"]

    return []


def execute_tools(tool_names: list[str]) -> list[dict]:
    available_tools = {
        "check_internet": check_internet,
        "check_network": check_network,
        "check_system": check_system,
    }

    results = []

    for tool_name in tool_names:
        tool = available_tools.get(tool_name)

        if tool is None:
            continue

        try:
            results.append(tool())

        except Exception as error:
            results.append(
                {
                    "tool": tool_name,
                    "status": "error",
                    "error": str(error),
                }
            )

    return results


def should_escalate(
    problem: str,
    category: str,
    tool_results: list[dict],
) -> tuple[bool, str]:
    """
    Decide whether the problem should be escalated.

    This decision is deliberately controlled by application logic,
    rather than allowing the LLM to execute arbitrary actions.
    """

    text = problem.lower()

    escalation_keywords = [
        "already tried",
        "still not working",
        "nothing works",
        "tried everything",
        "urgent",
        "critical",
        "cannot work",
        "unable to work",
        "completely down",
    ]

    if any(keyword in text for keyword in escalation_keywords):
        return True, "User indicates that standard troubleshooting has failed."

    for result in tool_results:

        if result.get("status") == "error":
            return True, "A diagnostic tool failed."

        if (
            result.get("tool") == "check_internet"
            and result.get("reachable") is False
        ):
            return True, "Internet connectivity could not be established."

        if (
            result.get("tool") == "check_network"
            and result.get("network_available") is False
        ):
            return True, "No active local network connection was detected."

    return False, ""


def run_agent(problem: str) -> dict:
    """
    Main HelpDesk AI agent workflow.

    1. Understand the problem.
    2. Select safe diagnostic tools.
    3. Execute diagnostics.
    4. Retrieve relevant knowledge.
    5. Generate an evidence-aware response.
    6. Escalate to a ticket when necessary.
    """

    problem = problem.strip()

    if not problem:
        raise ValueError("Problem description cannot be empty.")

    category = detect_category(problem)

    selected_tools = select_tools(category)

    tool_results = execute_tools(selected_tools)

    ai_result = generate_helpdesk_response(
        problem,
        tool_results,
    )

    escalate, escalation_reason = should_escalate(
        problem,
        category,
        tool_results,
    )

    ticket = None

    if escalate:
        priority = "High"

        if any(
            word in problem.lower()
            for word in ["urgent", "critical", "completely down"]
        ):
            priority = "Critical"

        ticket_result = create_helpdesk_ticket(
            problem=problem,
            category=category,
            priority=priority,
        )

        ticket = ticket_result.get("ticket")

    return {
        "agent": "HelpDesk AI",
        "category": category,
        "tools_selected": selected_tools,
        "tool_results": tool_results,
        "response": ai_result,
        "escalation": {
            "required": escalate,
            "reason": escalation_reason,
            "ticket": ticket,
        },
    }

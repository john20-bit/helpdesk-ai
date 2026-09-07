from fastapi import APIRouter

from app.tools.diagnostics import (
    check_internet,
    check_network,
    check_system,
)

router = APIRouter(
    prefix="/api/diagnostics",
    tags=["Diagnostics"],
)


@router.get("")
def run_diagnostics():
    results = []

    for tool in [check_internet, check_network, check_system]:
        try:
            results.append(tool())
        except Exception as error:
            results.append({
                "tool": tool.__name__,
                "status": "error",
                "error": str(error),
            })

    return {
        "success": True,
        "diagnostics": results,
    }

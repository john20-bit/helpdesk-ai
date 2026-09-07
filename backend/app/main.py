from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.routes import router as ai_router
from app.tickets.routes import router as ticket_router
from app.tools.routes import router as diagnostics_router
from app.db.database import initialize_database


initialize_database()

app = FastAPI(
    title="HelpDesk AI",
    description="AI-powered IT Helpdesk Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
app.include_router(ticket_router)
app.include_router(diagnostics_router)


@app.get("/")
def root():
    return {
        "application": "HelpDesk AI",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "HelpDesk AI Backend",
    }

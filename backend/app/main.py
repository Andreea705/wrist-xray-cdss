from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.dashboard import router as dashboard_router
app = FastAPI(title="Pediatric Wrist CDSS")

app.add_middleware(

    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(dashboard_router)

@app.get("/health")
def health():
    return {"status": "ok"}
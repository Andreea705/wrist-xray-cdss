from fastapi import APIRouter, Depends

from app.auth import USERS, current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Demo-Daten, komplett erfunden
PATIENTS = [
    {"id": "P-1001", "age": 8,  "sex": "m", "side": "links",  "arrival": "08:15", "complaint": "Sturz auf die Hand",       "status": "reported"},
    {"id": "P-1002", "age": 12, "sex": "w", "side": "rechts", "arrival": "08:40", "complaint": "Sturz beim Inlineskaten",  "status": "reported"},
    {"id": "P-1003", "age": 5,  "sex": "w", "side": "rechts", "arrival": "09:05", "complaint": "Sturz vom Klettergerüst",  "status": "imaged"},
    {"id": "P-1004", "age": 14, "sex": "m", "side": "links",  "arrival": "09:30", "complaint": "Sportverletzung (Fußball)", "status": "imaged"},
    {"id": "P-1005", "age": 3,  "sex": "m", "side": "rechts", "arrival": "10:10", "complaint": "Sturz vom Sofa",           "status": "waiting"},
    {"id": "P-1006", "age": 10, "sex": "w", "side": "links",  "arrival": "10:25", "complaint": "Fahrradsturz",             "status": "waiting"},
    {"id": "P-1007", "age": 15, "sex": "m", "side": "rechts", "arrival": "10:50", "complaint": "Sturz beim Skateboarden",  "status": "waiting"},
    {"id": "P-1008", "age": 7,  "sex": "w", "side": "links",  "arrival": "11:05", "complaint": "Sturz auf dem Spielplatz", "status": "waiting"},
]


@router.get("")
def dashboard(username: str = Depends(current_user)):
    count = lambda s: sum(1 for p in PATIENTS if p["status"] == s)
    return {
        "hospital": "Kinderklinik Musterstadt (Demo)",
        "department": "Kindertraumatologie",
        "doctor": USERS[username]["name"],
        "stats": {
            "total": len(PATIENTS),
            "waiting": count("waiting"),
            "imaged": count("imaged"),
            "reported": count("reported"),
        },
        "patients": PATIENTS,
    }
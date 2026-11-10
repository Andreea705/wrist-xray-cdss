import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
TOKEN_MINUTES = 60

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(prefix="/auth", tags=["auth"])

# Temporar: utilizatori în memorie. Mai târziu îi mutăm într-o bază de date.
USERS = {
    "dr.popescu": {
        "name": "Dr. Popescu",
        "hash": password_hash.hash("parola-de-test"),
    },
}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form.username)
    if not user or not password_hash.verify(form.password, user["hash"]):
        raise HTTPException(status_code=401, detail="Benutzername oder Passwort falsch")
    exp = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    token = jwt.encode({"sub": form.username, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token ungültig oder abgelaufen")
    username = payload.get("sub")
    if username not in USERS:
        raise HTTPException(status_code=401, detail="Unbekannter Benutzer")
    return username


@router.get("/me")
def me(username: str = Depends(current_user)):
    return {"username": username, "name": USERS[username]["name"]}


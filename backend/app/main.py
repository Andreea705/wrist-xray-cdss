from fastapi import FastAPI

app = FastAPI(title="Pediatric Wrist CDSS")

@app.get("/health")
def health():
    return {"status": "ok"}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from pathlib import Path

app = FastAPI(title="WESTY TOON API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path("westy_toon.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Contact(BaseModel):
    name: str
    phone: str
    email: str = ""
    note: str = ""

@app.get("/api/contacts")
def get_contacts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/contacts")
def add_contact(contact: Contact):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO contacts (name, phone, email, note) VALUES (?, ?, ?, ?)",
        (contact.name, contact.phone, contact.email, contact.note)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.delete("/api/contacts/{contact_id}")
def delete_contact(contact_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
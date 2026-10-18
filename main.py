from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)



app = FastAPI(title="Notes API", version="0.1.0")

notes = {}
next_id = 1

@app.get("/notes")
def get_notes():
    return list(notes.values()) 

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    global next_id
    new_note = note.model_dump()
    new_note["id"] = next_id
    notes[next_id] = new_note
    next_id += 1
    return new_note

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "Hello from Notes API"}
from fastapi import FastAPI, HTTPException, Response
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Notes API", version="0.1.0")

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=80)
    content: Optional[str] = Field(None, min_length=1, max_length=500)

STAR_HEAD_DONE = True
STAR_PATCH_DONE = True
STAR_DELETE_DONE = True

notes = {}
next_id = 1

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    del notes[note_id]
    return Response(status_code=204)

@app.patch("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteUpdate):
    if note_id not in notes:
            raise HTTPException(status_code=404, detail="Note not found")

    note = notes[note_id]
    update_data = note_update.model_dump(exclude_unset=True)
    note.update(update_data)
    return note

@app.head("/notes/{note_id}")
def check_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    return Response(status_code=200, headers={"x-note-exists": "true"})

@app.get("/notes")
def get_notes():
    return list(notes.values()) 

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")

    return notes[note_id]

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
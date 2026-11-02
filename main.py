from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from db import get_connection


app = FastAPI(title="Notes API", version="0.2.0")


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=80)
    content: Optional[str] = Field(None, min_length=1, max_length=500)


STAR_HEAD_DONE = True
STAR_PATCH_DONE = True
STAR_DELETE_DONE = True


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    with get_connection() as conn:
        result = conn.execute(
            """
            INSERT INTO notes (title, content)
            VALUES (%s, %s)
            RETURNING id, title, content
            """,
            (note.title, note.content),
        )
        created_note = result.fetchone()

    return created_note


@app.get("/notes")
def get_notes():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id, title, content FROM notes ORDER BY id"
        )
        notes = result.fetchall()

    return notes


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id, title, content FROM notes WHERE id = %s",
            (note_id,),
        )
        note = result.fetchone()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.patch("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteUpdate):
    update_data = note_update.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Note fields cannot be null",
        )

    with get_connection() as conn:
        result = conn.execute(
            """
            UPDATE notes
            SET title = COALESCE(%s, title),
                content = COALESCE(%s, content)
            WHERE id = %s
            RETURNING id, title, content
            """,
            (
                update_data.get("title"),
                update_data.get("content"),
                note_id,
            ),
        )
        updated_note = result.fetchone()

    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return updated_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    with get_connection() as conn:
        result = conn.execute(
            "DELETE FROM notes WHERE id = %s RETURNING id",
            (note_id,),
        )
        deleted_note = result.fetchone()

    if deleted_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return Response(status_code=204)


@app.head("/notes/{note_id}")
def check_note(note_id: int):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id FROM notes WHERE id = %s",
            (note_id,),
        )
        note = result.fetchone()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return Response(
        status_code=200,
        headers={"x-note-exists": "true"},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "Hello from Notes API"}
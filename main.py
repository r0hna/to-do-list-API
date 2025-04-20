from typing import Union, List
from models.note_model import Note
from fastapi import FastAPI, HTTPException
from database.db import SqlDb

app = FastAPI()

sql_db = SqlDb()  # Create an instance of SqlDb

@app.get("/status")
def status():
    return {"server": "It is running fine."}

# Create a new note
@app.post("/note/add", response_model=Note)
def add_note(note: Note):
    conn = sql_db.db_conn()  # Corrected: Call db_conn as a method
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO notes (id, title, desc, isImp) VALUES (?, ?, ?, ?)",
                       (note.id, note.title, note.desc, note.isImp))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail="Note with this ID already exists.")
    conn.close()
    return note

# Read all notes
@app.get("/notes/all", response_model=List[Note])
def get_notes():
    conn = sql_db.db_conn()  # Corrected: Call db_conn as a method
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    conn.close()
    return [Note(id=row[0], title=row[1], desc=row[2], isImp=bool(row[3])) for row in rows]

# Read a single note by ID
@app.get("/notes/{note_id}", response_model=Note)
def one_note(note_id: int):
    conn = sql_db.db_conn()  # Corrected: Call db_conn as a method
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    return Note(id=row[0], title=row[1], desc=row[2], isImp=bool(row[3]))

# Update a note by ID
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, updated_note: Note):
    conn = sql_db.db_conn()  # Corrected: Call db_conn as a method
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found.")
    cursor.execute("UPDATE notes SET title = ?, desc = ?, isImp = ? WHERE id = ?",
                   (updated_note.title, updated_note.desc, updated_note.isImp, note_id))
    conn.commit()
    conn.close()
    return updated_note

# Delete a note by ID
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = sql_db.db_conn()  # Corrected: Call db_conn as a method
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found.")
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return {"message": f"Note with ID {note_id} has been deleted."}




## Run server
## fastapi run main.py
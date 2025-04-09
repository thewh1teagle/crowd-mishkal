"""
Dev:
    uv run fastapi dev main.py
    http://127.0.0.1:8000/docs

Prod:
    uv run fastapi run main.py
"""

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.mount("/public", StaticFiles(directory="public"), name="public")

def get_db():
    return sqlite3.connect("db.sqlite")

@app.get("/next-line")
def get_next_line():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT line_number, line FROM lines WHERE tagged IS NULL AND skipped = 0 ORDER BY line_number ASC LIMIT 1')
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"line_number": row[0], "line": row[1]}
    return {"line_number": None, "line": None}

class TaggedLine(BaseModel):
    line_number: int
    tagged: str

@app.post("/submit-tagged")
def submit_tagged(data: TaggedLine):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE lines SET tagged = ? WHERE line_number = ?", (data.tagged, data.line_number))
    conn.commit()
    conn.close()
    return {"status": "ok"}

class SkipRequest(BaseModel):
    line_number: int

@app.post("/skip-line")
def skip_line(data: SkipRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE lines SET skipped = 1 WHERE line_number = ?", (data.line_number,))
    conn.commit()
    conn.close()
    return {"status": "skipped"}


@app.get("/download-tagged")
def download_tagged():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT line_number, line, tagged FROM lines
        WHERE tagged IS NOT NULL
        ORDER BY line_number ASC
        '''
    )
    rows = cursor.fetchall()
    conn.close()

    data = [
        {"line_number": line_number, "line": line, "tagged": tagged}
        for line_number, line, tagged in rows
    ]

    headers = {
        "Content-Disposition": "attachment; filename=tagged_lines.json"
    }
    content = json.dumps(data, ensure_ascii=False, indent=2)

    return Response(content, media_type="application/json", headers=headers)


@app.get("/view")
def view_all_lines():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT line_number, line, tagged, being_tagged FROM lines
        ORDER BY line_number ASC
        '''
    )
    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            "line_number": line_number,
            "line": line,
            "tagged": tagged,
            "being_tagged": bool(being_tagged)
        }
        for line_number, line, tagged, being_tagged in rows
    ]

    return data

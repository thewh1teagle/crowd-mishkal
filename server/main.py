"""
Prepare:
    wget https://huggingface.co/datasets/thewh1teagle/hebright/resolve/main/knesset_niqqud.txt.7z
    7z x knesset_niqqud.txt.7z
    head -n 10000 knesset_niqqud.txt > 10000.txt
    sed -i 's/|//g' 10000.txt # remove niqqud male mark
    uv run to_sqlite.py 10000.txt
Dev:
    uv run fastapi dev main.py
    http://127.0.0.1:8000/docs
    http://64.176.165.37:8000

Prod cert:
    # Generate private key
    openssl genpkey -algorithm RSA -out server.key

    # Generate certificate signing request (CSR)
    openssl req -new -key server.key -out server.csr

    # Generate the self-signed certificate
    openssl x509 -req -in server.csr -signkey server.key -out server.crt

    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=server.key --ssl-certfile=server.crt
    https://64.176.165.37:8000
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

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    # Count the total number of lines
    cursor.execute('SELECT COUNT(*) FROM lines')
    total_count = cursor.fetchone()[0]

    # Count the number of tagged lines
    cursor.execute('SELECT COUNT(*) FROM lines WHERE tagged IS NOT NULL')
    tagged_count = cursor.fetchone()[0]

    conn.close()

    return {"total_lines": total_count, "tagged_lines": tagged_count}

@app.get("/next-line")
def get_next_line():
    conn = get_db()
    cursor = conn.cursor()

    # Get the next line that isn't tagged and hasn't been skipped
    cursor.execute('SELECT line_number, line FROM lines WHERE being_tagged = 0 AND tagged IS NULL AND skipped = 0 ORDER BY line_number ASC LIMIT 1')
    row = cursor.fetchone()

    if row:
        line_number = row[0]

        # Set being_tagged to True for this line
        cursor.execute('UPDATE lines SET being_tagged = 1 WHERE line_number = ?', (line_number,))
        conn.commit()

        conn.close()
        return {"line_number": row[0], "line": row[1]}

    conn.close()
    return {"line_number": None, "line": None}

class TaggedLine(BaseModel):
    line_number: int
    tagged: str

@app.post("/submit-tagged")
def submit_tagged(data: TaggedLine):
    conn = get_db()
    cursor = conn.cursor()

    # Update the line with the tagged information
    cursor.execute("UPDATE lines SET tagged = ?, being_tagged = 0 WHERE line_number = ?", (data.tagged, data.line_number))
    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.post("/clear-being-tagged")
def clear_being_tagged():
    conn = get_db()
    cursor = conn.cursor()

    # Reset the being_tagged status for all lines
    cursor.execute("UPDATE lines SET being_tagged = 0")
    conn.commit()
    conn.close()

    return {"status": "ok"}


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

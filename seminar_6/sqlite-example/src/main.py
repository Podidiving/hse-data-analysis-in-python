from fastapi import FastAPI
import sqlite3

app = FastAPI()
sqlite3_db_name = "db.db"

def create_table_if_not_exists():
    with sqlite3.connect(sqlite3_db_name) as con:
        cmd = "CREATE TABLE IF NOT EXISTS name (first_column integer PRIMARY KEY, second_column integer)"
        con.execute(cmd)
        con.commit()


@app.on_event("startup")
def startup_event():
    create_table_if_not_exists()


@app.post("/api/set")
def set_kv(fc: int, sc: int):
    with sqlite3.connect(sqlite3_db_name) as con:
        con.execute("INSERT INTO name VALUES (?, ?)", (fc, sc))
        con.commit()


@app.get("/api/get/{fc}")
def get_kv(fc: str):
    with sqlite3.connect(sqlite3_db_name) as con:
        cursor = con.execute("SELECT second_column FROM name WHERE first_column = :first_column", {"first_column": fc})
        rows = cursor.fetchone()
        return {"sc": rows[0]}

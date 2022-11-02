from .connect import connect_to_db

def add_record(record):
    cur, con = connect_to_db()
    res = cur.executemany("INSERT INTO logs VALUES(?, ?)", record)
    res.fetchone()
    con.commit()
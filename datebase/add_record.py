
def add_record(cur, con, record):
    res = cur.executemany("INSERT INTO logs VALUES(?, ?)", record)
    res.fetchone()
    con.commit()
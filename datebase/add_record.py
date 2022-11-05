import sqlite3

from .connect import connect_to_db

def add_record(record):
    cur, con = connect_to_db()

    try:
        cur.execute("SELECT * FROM logs")

        data_list = cur.fetchall()
        print('--------' + '\t\t-------------')
        for item in data_list:
            print(item)

    except sqlite3.OperationalError:
        print("No such table: logs")
        if sqlite3.OperationalError:  # if this error occurs
            try:
                print("Creating a new table: ")
                cur.execute('''
                    CREATE TABLE logs(
                    time datatime, 
                    count int
                );''')

                print("New table created successfully!!!")

            except sqlite3.Error() as e:
                print(e, " occured")


    res = cur.executemany("INSERT INTO logs VALUES(?, ?)", record)
    res.fetchone()
    con.commit()
    con.close()
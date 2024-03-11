import sqlite3

def execute(prompt, values, database="gym.db"):
    """ Execute a prompt into database """
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(prompt, values)
    con.commit()
    con.close()


def query(prompt, values=None, database="gym.db"):
    """ Query database """
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if values:
        data = cur.execute(prompt, values).fetchall()
    else:
        data = cur.execute(prompt).fetchall()
    con.close()
    return data
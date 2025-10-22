import sqlite3

def get_users():
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ID_utente, mail_utente, username, immagine_profilo, tipo FROM utenti'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


def add_user(user):

    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utenti(mail_utente,username,password,immagine_profilo, tipo) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['mail_utente'], user['username'], user['password'], user['immagine_profilo'], user['tipo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def get_user_by_mail_utente(mail_utente):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE mail_utente = ?'
    cursor.execute(sql, (mail_utente,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_username(username):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE username = ?'
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_ID(ID_utente):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE ID_utente = ?'
    cursor.execute(sql, (ID_utente,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

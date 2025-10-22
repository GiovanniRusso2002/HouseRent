import sqlite3


def add_foto(percorso_file,ID_annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO foto(percorso_file, ID_annuncio) VALUES(?,?)'
    cursor.execute(sql, (percorso_file, ID_annuncio))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_foto_by_ID_annuncio(ID_annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT percorso_file FROM foto WHERE ID_annuncio = ?'
    cursor.execute(sql, (ID_annuncio,))
    post = cursor.fetchall()

    cursor.close()
    conn.close()

    return post


def delete_image(ID_annuncio, percorso_file):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM foto WHERE ID_annuncio=? AND percorso_file=? '
    cursor.execute(sql, (ID_annuncio,percorso_file))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def check_count_foto(ID_annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT COUNT(*) AS count FROM foto WHERE ID_annuncio = ?'
    cursor.execute(sql, (ID_annuncio,))
    count_foto = cursor.fetchone()['count']
    cursor.close()
    conn.close()
    return count_foto

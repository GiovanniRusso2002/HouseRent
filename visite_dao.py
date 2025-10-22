import sqlite3


def get_visite_personali(ID_utente):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ID_visita, annunci.ID_annuncio, utenti.ID_utente, mail_utente , username, immagine_profilo, indirizzo, data, fascia_oraria, stato, motivazione, visite.tipo FROM annunci, utenti, visite WHERE annunci.ID_annuncio = visite.ID_annuncio AND visite.ID_utente = ? AND annunci.ID_utente = utenti.ID_utente'
    cursor.execute(sql, (ID_utente,))
    visite_personali = cursor.fetchall()

    cursor.close()
    conn.close()
    return visite_personali

def get_visite_locatore(ID_utente):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ID_visita, annunci.ID_annuncio, U2.ID_utente, U2.mail_utente , U2.username, U2.immagine_profilo, indirizzo, data, fascia_oraria, stato, motivazione, visite.tipo FROM annunci, utenti U1, utenti U2, visite WHERE annunci.ID_annuncio = visite.ID_annuncio AND  U1.ID_utente = ? AND annunci.ID_utente = U1.ID_utente AND U2.ID_utente = visite.ID_utente'
    cursor.execute(sql, (ID_utente,))
    visite_locatore = cursor.fetchall()

    cursor.close()
    conn.close()
    return visite_locatore

def add_visita(visita):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO visite(ID_utente, ID_annuncio, data, fascia_oraria, stato, motivazione, tipo) VALUES(?,?,?,?,?,?,?)'
    cursor.execute(sql, (visita['ID_utente'], visita['ID_annuncio'], visita['data'], visita['fascia_oraria'], visita['stato'], visita['motivazione'], visita['tipo']))
   
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


def check_visita(visita):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM visite WHERE ID_annuncio = ? AND data = ? AND fascia_oraria = ? AND stato = 'accettata' "
    cursor.execute(sql, (visita['ID_annuncio'], visita['data'], visita['fascia_oraria']))
    check = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(check):
        return True
    return False


def confirm_visita(conferma):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    if conferma['motivazione'] =='':
        sql = 'UPDATE visite SET stato = ? WHERE ID_visita = ?'
        cursor.execute(sql, (conferma['stato_finale'],  conferma['ID_visita']))

    else:
        sql = 'UPDATE visite SET stato = ?, motivazione = ? WHERE ID_visita = ?'
        cursor.execute(sql, (conferma['stato_finale'], conferma['motivazione'], conferma['ID_visita']))

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



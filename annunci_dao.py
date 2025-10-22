import sqlite3



def get_annunci_by_ID(ID_utente_locatore, current_ID_utente, bit_locali):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if bit_locali: 
        sql = "SELECT annunci.ID_annuncio, titolo, indirizzo,descrizione, prezzo, locali, username, immagine_profilo FROM annunci, utenti WHERE visibile = 1 AND utenti.ID_utente != ? AND annunci.ID_utente = utenti.ID_utente AND annunci.ID_annuncio NOT IN (SELECT visite.ID_annuncio FROM visite, utenti U2, annunci A2 WHERE visite.ID_annuncio = A2.ID_annuncio AND visite.ID_utente = U2.ID_utente AND U2.ID_utente = ? AND stato != 'rifiutata' )  ORDER BY locali"
    else:
        sql = "SELECT annunci.ID_annuncio, titolo, indirizzo,descrizione, prezzo, locali, username, immagine_profilo FROM annunci, utenti WHERE visibile = 1 AND utenti.ID_utente != ? AND annunci.ID_utente = utenti.ID_utente AND annunci.ID_annuncio NOT IN (SELECT visite.ID_annuncio FROM visite, utenti U2, annunci A2 WHERE visite.ID_annuncio = A2.ID_annuncio AND visite.ID_utente = U2.ID_utente AND U2.ID_utente = ? AND stato != 'rifiutata' ) ORDER BY prezzo DESC"

    cursor.execute(sql, (ID_utente_locatore,current_ID_utente))
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

def get_annuncio(ID_annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ID_annuncio, annunci.ID_utente, mail_utente, locali, annunci.tipo,  titolo, indirizzo, descrizione, visibile, arredo,  prezzo, username, immagine_profilo FROM annunci, utenti WHERE annunci.ID_utente = utenti.ID_utente AND ID_annuncio =  ?'
    cursor.execute(sql, (ID_annuncio,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post

def add_annuncio(annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO annunci(ID_utente, locali, tipo, titolo, indirizzo, descrizione, visibile, arredo, prezzo) VALUES(?,?,?,?,?,?,?,?,?)'
    cursor.execute(sql, (annuncio['ID_utente'], annuncio['locali'], annuncio['tipo'], annuncio['titolo'], annuncio['indirizzo'], annuncio['descrizione'], annuncio['visibile'], annuncio['arredo'], annuncio['prezzo']))
    last_ID_annuncio = cursor.lastrowid
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        
        conn.rollback()

    cursor.close()
    conn.close()

    return (success,last_ID_annuncio)


def get_annunci_locatore_by_ID(ID_utente_locatore):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

   
    sql = "SELECT annunci.ID_annuncio, titolo, indirizzo,descrizione, prezzo, locali, username, visibile, immagine_profilo FROM annunci, utenti WHERE annunci.ID_utente =  ? AND annunci.ID_utente = utenti.ID_utente"

    cursor.execute(sql, (ID_utente_locatore,))
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

def update_annuncio(annuncio):
    conn = sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE annunci SET locali = ?, tipo = ?, titolo= ?, descrizione = ?, visibile = ?, arredo = ?, prezzo = ? WHERE ID_annuncio = ?'
    cursor.execute(sql, (annuncio['locali'], annuncio['tipo'], annuncio['titolo'], annuncio['descrizione'], annuncio['visibile'], annuncio['arredo'], annuncio['prezzo'], annuncio['ID_annuncio']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
    
        conn.rollback()

    cursor.close()
    conn.close()

    return success


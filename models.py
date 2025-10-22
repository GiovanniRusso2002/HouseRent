from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id, mail_utente, username, password,immagine_profilo, tipo):
        self.id = id
        self.mail_utente = mail_utente
        self.username = username
        self.password = password
        self.immagine_profilo = immagine_profilo
        self.tipo = tipo
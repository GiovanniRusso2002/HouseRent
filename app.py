# import module
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime, timedelta

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import utenti_dao, foto_dao, annunci_dao, visite_dao #importa i file delle entità sul app.py

from models import User

# Import the Image module from the PIL (Python Imaging Library) package. Used to preprocess the images uploaded by the users. Ensure 'Pillow' is installed before running the application by using the command 'pip install Pillow'

from PIL import Image

PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

# create the application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret key di Affitti Bari'

login_manager = LoginManager()
login_manager.init_app(app)

# define the homepage
@app.route('/')
def home():
    
    foto_db = []
    bit_locali = 0

    if current_user.is_authenticated:
        if current_user.tipo == 'locatore':
            annunci_db_result = annunci_dao.get_annunci_by_ID(current_user.id, current_user.id,bit_locali)
        else:
            annunci_db_result = annunci_dao.get_annunci_by_ID('',current_user.id,bit_locali)
    else:
        annunci_db_result = annunci_dao.get_annunci_by_ID('', '',bit_locali)
   
    annunci_db = [dict(row) for row in annunci_db_result]

    for annuncio_db in annunci_db:
        if annuncio_db['locali'] == 5:
           annuncio_db['locali'] ='5+'

        foto_result=foto_dao.get_foto_by_ID_annuncio(annuncio_db['ID_annuncio'])
        foto_db = [dict(row) for row in foto_result]
        
        annuncio_db['foto'] = foto_db[0]['percorso_file']
        
    return render_template('home.html', annunci=annunci_db)

@app.route('/locali_cresc')
def home_locali():
    foto_db = []
    bit_locali = 1

    if current_user.is_authenticated:
        if current_user.tipo == 'locatore':
            annunci_db_result = annunci_dao.get_annunci_by_ID(current_user.id, current_user.id,bit_locali)
        else:
            annunci_db_result = annunci_dao.get_annunci_by_ID('',current_user.id,bit_locali)
    else:
        annunci_db_result = annunci_dao.get_annunci_by_ID('', '',bit_locali)
   
    annunci_db = [dict(row) for row in annunci_db_result]

    for annuncio_db in annunci_db:
        if annuncio_db['locali'] == 5:
           annuncio_db['locali'] ='5+'

        foto_result=foto_dao.get_foto_by_ID_annuncio(annuncio_db['ID_annuncio'])
        foto_db = [dict(row) for row in foto_result]
        
        annuncio_db['foto'] = foto_db[0]['percorso_file']
        
    return render_template('home.html', annunci=annunci_db)

# define the single annuncio page    
@app.route('/annunci/<int:ID_annuncio>')
def single_annuncio(ID_annuncio):
    start = datetime.now().date() + timedelta(days=1)
    end = datetime.now().date() + timedelta(days=7)
    foto_db = []
    annuncio_db_result = annunci_dao.get_annuncio(ID_annuncio)
    annuncio_db = dict(annuncio_db_result)
    if annuncio_db['locali'] == 5:
        annuncio_db['locali'] ='5+'

    result = foto_dao.get_foto_by_ID_annuncio(ID_annuncio)

    for row in result:
        foto_db.append(row['percorso_file'])

    return render_template('annuncio.html', annuncio=annuncio_db, foto = foto_db, start = start, end = end)


@app.route('/edit_annuncio/<int:ID_annuncio>')
@login_required
def edit_annuncio(ID_annuncio):
    foto_db = []
    annuncio_db_result = annunci_dao.get_annuncio(ID_annuncio)
    annuncio_db = dict(annuncio_db_result)
    if annuncio_db['locali'] == 5:
        annuncio_db['locali'] ='5+'

    result = foto_dao.get_foto_by_ID_annuncio(ID_annuncio)

    for row in result:
        foto_db.append(row['percorso_file'])

    return render_template('edit_annuncio.html', annuncio=annuncio_db, foto = foto_db)


@app.route('/annunci_locatore')
@login_required
def annunci_locatore():
    
    foto_db = []
    annunci_db_result = annunci_dao.get_annunci_locatore_by_ID(current_user.id)
    annunci_db = [dict(row) for row in annunci_db_result]

    for annuncio_db in annunci_db:
        if annuncio_db['locali'] == 5:
           annuncio_db['locali'] ='5+'

        foto_result=foto_dao.get_foto_by_ID_annuncio(annuncio_db['ID_annuncio'])
        foto_db = [dict(row) for row in foto_result]
        
        annuncio_db['foto'] = foto_db[0]['percorso_file']
        
    return render_template('pagina_locatore.html', annunci=annunci_db)


@app.route('/annuncio/update', methods=['POST'])
@login_required
def update_annuncio():

    annuncio = request.form.to_dict()
    if annuncio['locali'] == '': 
        app.logger.error('Devi selezionare il numero di locali')
        return redirect(url_for('annunci_locatore'))
    
    if annuncio['descrizione'] == '': 
        app.logger.error('Devi scrivere una descrizione')
        return redirect(url_for('annunci_locatore'))

    if annuncio['tipo'] == '':
        app.logger.error('Devi selezionare un tipo')
        return redirect(url_for('annunci_locatore'))


    if('arredo' in annuncio): 
        if(annuncio['arredo']=="on"): 
            annuncio['arredo']=1
    else:
        annuncio['arredo']=0

    if('visibile' in annuncio):
        if(annuncio['visibile']=="on"):
            annuncio['visibile']=1
    else:
        annuncio['visibile']=0

    annuncio['prezzo'] = float(annuncio['prezzo'])
    if annuncio['prezzo'] <=0:
        app.logger.error('Prezzo non valido')
        return redirect(url_for('annunci_locatore'))


    annuncio['ID_utente'] = current_user.id
    if annuncio['locali'] == '5+':
        annuncio['locali'] = 5
    else:
        annuncio['locali'] = int(annuncio['locali'])

    count = 0

    for i in range(0,5):
        if f'immagini_selezionate{i}' in annuncio:
            count= count+1

    num_foto = foto_dao.check_count_foto(annuncio['ID_annuncio']) 

    if num_foto == count: #IMPORTANTE: verifico se il numero delle foto originali è maggiore di 0 perchè non voglio permettere all'utente di cancellare tutte le foto nel caso in cui nel caricamento delle nuove ci siano errori di caricamento!! 

        app.logger.error('Nella cancellazione deve rimanere almeno una foto!')
        flash('Nella cancellazione deve rimanere almeno una foto prima della modifica!', 'danger')
        return redirect(url_for('annunci_locatore'))
    
    for i in range(0,5):
        if f'immagini_selezionate{i}' in annuncio:
            success = foto_dao.delete_image(annuncio['ID_annuncio'], annuncio[f'immagini_vecchie{i}'])
            if success:
                app.logger.info('Foto eliminata correttamente')
            else:
                app.logger.error('Errore nella cancellazione')


    annuncio_images = []
    for i in range(0,5):
        new_image = request.files.get(f'immagini_nuove{i}')
        if new_image is not None and new_image.filename!= '':
            annuncio_images.append(new_image)

    if any(annuncio_image.filename for annuncio_image in annuncio_images):
            count = 0
            for annuncio_image in annuncio_images:
        
                if annuncio_image:

                    # Open the user-provided image using the Image module
                    img = Image.open(annuncio_image)

                    # Get the width and height of the image
                    width, height = img.size

                    # Calculate the new height while maintaining the aspect ratio based on the desired width
                    new_height = height/width * POST_IMG_WIDTH

                    # Define the size for thumbnail creation with the desired width and calculated height
                    size = POST_IMG_WIDTH, new_height
                    img.thumbnail(size, Image.Resampling.LANCZOS)

                    # Extracting file extension from the image filename
                    ext = annuncio_image.filename.split('.')[-1]
                    # Getting the current timestamp in seconds
                    secondi = int(datetime.now().timestamp())       

                    # Saving the image with a unique filename in the 'static' directory
                    img.save('static/@' + current_user.username.lower() + '-' + str(secondi) + '-' + str(count) +'.' + ext)

                

                    foto_dao.add_foto('@' + current_user.username.lower() + '-' + str(secondi)+ '-' + str(count) + '.' + ext,annuncio['ID_annuncio'] )
                    count = count+1
  
    success = annunci_dao.update_annuncio(annuncio)  
    if success:
        flash('Annuncio modificato!', 'success')
        app.logger.info('Annuncio modificato corettamente')
    else:
        flash('Errore durante la modifica!', 'success')
        app.logger.error('Errore nella modifica dell annuncio: riprova!')

    return redirect(url_for('edit_annuncio',ID_annuncio = annuncio['ID_annuncio']))


@app.route('/profilo')
@login_required
def profilo():
    visite_personali_db = []
    visite_locatore_db = []
    visite_personali_result = visite_dao.get_visite_personali(current_user.id)

    visite_personali_db = [dict(row) for row in visite_personali_result]

    for visita_personale in visite_personali_db:
        
        foto_result=foto_dao.get_foto_by_ID_annuncio(visita_personale['ID_annuncio'])
        foto_db = [dict(row) for row in foto_result]
        
        visita_personale['foto'] = foto_db[0]['percorso_file']
        

    if current_user.tipo == 'locatore':
        visite_locatore_result = visite_dao.get_visite_locatore(current_user.id)

        visite_locatore_db = [dict(row) for row in visite_locatore_result]

        for visita_locatore in visite_locatore_db:
        
            foto_result=foto_dao.get_foto_by_ID_annuncio(visita_locatore['ID_annuncio'])
            foto_db = [dict(row) for row in foto_result]
            
            visita_locatore['foto'] = foto_db[0]['percorso_file']
        
    return render_template('profilo.html', visite_personali= visite_personali_db, visite_locatore = visite_locatore_db)

@app.route('/visita/confirm', methods=['POST'])
@login_required
def confirm_visita():
    conferma = request.form.to_dict()

    if conferma['stato_finale'] == '':
        app.logger.error('Nessuna opzione!')
        return redirect(url_for('profilo'))
    
    if conferma['stato_finale'] == 'rifiutata' and conferma['motivazione'] =='':
        app.logger.error('Visita rifiutata senza motivazione!')
        flash('Per rifiutare una visita serve la motivazione!','danger')
        return redirect(url_for('profilo'))
    
    if conferma['stato_finale'] == 'accettata':
        conferma['motivazione']=''
    

    success = visite_dao.confirm_visita(conferma)

    if success:
        app.logger.info('Conferma effettuata correttamente')
    else:
        app.logger.error('Errore nella conferma della visita: riprova!')
        return redirect(url_for('profilo'))

            
    flash('Visita modificata!', 'success')
    return redirect(url_for('profilo'))


@app.route('/visita/new', methods=['POST'])
@login_required
def new_visita():

    visita = request.form.to_dict()
#Per non permettere all'utente di prenotare una fascia oraria passata nella stessa giornata viene negata la possibilità agli utenti di prenotare una visita il giorno stesso
    if visita['data'] == '' or datetime.strptime(visita['data'], '%Y-%m-%d').date() <= date.today() or  datetime.strptime(visita['data'], '%Y-%m-%d').date() > date.today() + timedelta(days=7) :
        app.logger.error('Data errata!')
        return redirect(url_for('single_annuncio', ID_annuncio=visita['ID_annuncio']))
        
    if visita['fascia_oraria'] == '':
        app.logger.error('La richiesta deve avere una fascia oraria!')
        return redirect(url_for('single_annuncio', ID_annuncio=visita['ID_annuncio']))
    
    if visita['tipo'] == '':
        app.logger.error('La richiesta deve avere una modalità!')
        return redirect(url_for('single_annuncio', ID_annuncio=visita['ID_annuncio']))

    
    visita['ID_annuncio'] = int(visita['ID_annuncio'])
    visita['ID_utente'] = int(current_user.id)
    visita['stato'] = 'richiesta'
    visita['motivazione'] = ''

    if visite_dao.check_visita(visita) == True: #verifica se ci sono date nella stessa fascia oraria e nello stesso giorno 
        flash('C\'è già una prenotazione accettata nella stessa fascia oraria: riprova!', 'danger')
        return redirect(url_for('single_annuncio', ID_annuncio=visita['ID_annuncio']))

    success = visite_dao.add_visita(visita)

    if success:
        app.logger.info('Visita creata correttamente')
    else:
        app.logger.error('Errore nella creazione della visita: riprova!')
        return redirect(url_for('single_annuncio', ID_annuncio=visita['ID_annuncio']))

            
    flash('Visita confermata!', 'success')
    return redirect(url_for('home'))


@app.route('/annuncio/new', methods=['POST'])
@login_required 
def new_annuncio():
            
    annuncio = request.form.to_dict() 

    if annuncio['locali'] == '':
        app.logger.error('Devi selezionare il numero di locali')
        return redirect(url_for('home'))

    if annuncio['tipo'] == '':
        app.logger.error('Devi selezionare un tipo')
        return redirect(url_for('home'))

    annuncio_images = request.files.getlist('immagini_annuncio')
    if len(annuncio_images) > 5:
        app.logger.error('Puoi caricare massimo 5 foto')
        return redirect(url_for('home'))
        
    if('arredo' in annuncio): 
        if(annuncio['arredo']=="on"): 
            annuncio['arredo']=1
    else:
        annuncio['arredo']=0

    if('visibile' in annuncio):
        if(annuncio['visibile']=="on"): 
            annuncio['visibile']=1
    else:
        annuncio['visibile']=0

    annuncio['prezzo'] = float(annuncio['prezzo'])
    
    if annuncio['prezzo'] <=0:
        app.logger.error('Prezzo non valido')
        return redirect(url_for('home'))

    annuncio['ID_utente'] = current_user.id
    if annuncio['locali'] == '5+':
        annuncio['locali'] = 5
    else:
        annuncio['locali'] = int(annuncio['locali'])  
    (success,last_ID_annuncio) = annunci_dao.add_annuncio(annuncio)

    if success:
        flash('Annuncio creato correttamente','success')
        
        count = 0
        for annuncio_image in annuncio_images:
    
            if annuncio_image:

                # Open the user-provided image using the Image module
                img = Image.open(annuncio_image)

                # Get the width and height of the image
                width, height = img.size

                # Calculate the new height while maintaining the aspect ratio based on the desired width
                new_height = height/width * POST_IMG_WIDTH

                # Define the size for thumbnail creation with the desired width and calculated height
                size = POST_IMG_WIDTH, new_height
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Extracting file extension from the image filename
                ext = annuncio_image.filename.split('.')[-1]
                # Getting the current timestamp in seconds
                secondi = int(datetime.now().timestamp())       

                # Saving the image with a unique filename in the 'static' directory
                img.save('static/@' + current_user.username.lower() + '-' + str(secondi) + '-' + str(count) +'.' + ext)

                foto_dao.add_foto('@' + current_user.username.lower() + '-' + str(secondi)+ '-' + str(count) + '.' + ext,last_ID_annuncio )
                count = count+1

    else:
        flash('Errore nella creazione del Annuncio: riprova!','danger')

    return redirect(url_for('home'))




# define the signup page
@app.route('/iscriviti')
def iscriviti():
    return render_template('signup.html')

@app.route('/iscriviti', methods=['POST'])
def iscriviti_post():

    nuovo_utente_form = request.form.to_dict()

    user_in_db_username = utenti_dao.get_user_by_username(nuovo_utente_form.get('username'))

    if user_in_db_username:
        flash('C\'è già un utente registrato con questo username', 'danger')
        return redirect(url_for('iscriviti'))
    
    user_in_db_mail_utente = utenti_dao.get_user_by_mail_utente(nuovo_utente_form.get('mail_utente'))

    if user_in_db_mail_utente:
        flash('C\'è già un utente registrato con questa mail', 'danger')
        return redirect(url_for('iscriviti'))
    else:
        img_profilo = ''
        usr_image = request.files['immagine_profilo']
        if usr_image:
            # Open the user-provided image using the Image module
            img = Image.open(usr_image)

            # Get the width and height of the image
            width, height = img.size

            # Calculate the new width while maintaining the aspect ratio
            new_width = PROFILE_IMG_HEIGHT * width / height

            # Define the size for thumbnail creation with the desired height and calculated width
            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # Calculate the coordinates for cropping the image to a square shape
            left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
            top = 0
            right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
            bottom = PROFILE_IMG_HEIGHT

            # Crop the image using the calculated coordinates to create a square image
            img = img.crop((left, top, right, bottom))

            # Extracting file extension from the image filename
            ext = usr_image.filename.split('.')[-1]

            # Saving the image with a unique filename in the 'static' directory
            img.save('static/' + nuovo_utente_form.get('username').lower() + '.' + ext)

            img_profilo = nuovo_utente_form.get('username').lower() + '.' + ext
        

        

        nuovo_utente_form['password'] = generate_password_hash(nuovo_utente_form.get('password'))
    
        if img_profilo:
            nuovo_utente_form['immagine_profilo'] = img_profilo
        else: nuovo_utente_form['immagine_profilo'] = 'user.jpg'

        

        success = utenti_dao.add_user(nuovo_utente_form)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('iscriviti'))



@app.route('/login', methods=['POST'])
def login():

  utente_form = request.form.to_dict()

  utente_db = utenti_dao.get_user_by_mail_utente(utente_form['mail_utente'])

  if not utente_db or not check_password_hash(utente_db['password'], utente_form['password']):
    flash('Credenziali non valide, riprova', 'danger')
    return redirect(url_for('home'))
  else:
    new = User(id = utente_db["ID_utente"], mail_utente=utente_db['mail_utente'], username=utente_db['username'], password=utente_db['password'], immagine_profilo=utente_db['immagine_profilo'], tipo= utente_db['tipo'] )
    login_user(new, True)
    flash('Bentornato ' + utente_db['username'] + '!', 'success')

    return redirect(url_for('home'))



@login_manager.user_loader
def load_user(ID_utente):

    db_user = utenti_dao.get_user_by_ID(ID_utente)
    if db_user is not None:
        user = User(id = db_user['ID_utente'], mail_utente=db_user['mail_utente'], username=db_user['username'],	password=db_user['password'], immagine_profilo=db_user['immagine_profilo'], tipo= db_user['tipo'])
    else:
        user = None

    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home')) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
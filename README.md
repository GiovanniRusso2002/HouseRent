# HouseRent — Rental Listings (Affitti Bari)

This is a small Flask web application for listing and managing rental properties. It's a simple prototype used for testing features like user registration, authentication, property posting, image upload and resizing, and scheduling visits.

Key features
- Browse public rental listings with photos and basic details (title, address, rooms, price).
- User registration and login (Flask-Login).
- Two user roles: "locatore" (property owner) and regular user.
- Locatore users can create, edit and manage their announcements and accept/reject visit requests.
- Users can book visits for announcements within a one-week window and choose time slots.
- Image uploads are processed with Pillow (resized/cropped) and saved to the `static/` folder.

Tech stack and dependencies
- Python 3.x
- Flask — web framework (routes and templates)
- Flask-Login — session management and user authentication
- SQLite (file): simple relational database stored at `db/affitti.db`
- Pillow (PIL) — image processing for thumbnails/cropping
- Bootstrap 5 (CDN) — UI styling found in the templates

Project layout (important files)
- `app.py` — Flask application, routes and image handling
- `models.py` — simple User model (Flask-Login UserMixin)
- `annunci_dao.py`, `utenti_dao.py`, `foto_dao.py`, `visite_dao.py` — simple DAO modules using `sqlite3` to interact with `db/affitti.db`
- `templates/` — Jinja2 templates for pages (home, annuncio, profile, signup, etc.)
- `static/` — styles, user and post images
- `db/affitti.db` — SQLite database file (not always committed; see notes)

Quick setup (Windows PowerShell)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
``` 

2. Install dependencies:

```powershell
pip install Flask Flask-Login Pillow
```

3. Ensure the database exists and has the required schema. This project uses `db/affitti.db`. If you don't have the DB file, you will need to create it and run the SQL schema (not included here). Check `db/` for a database file or ask the project owner for the schema.

4. (Optional) Add sample images into `new_images/` or `static/` if you want to create sample announcements.

Run the application
1. From the project root run:

```powershell
python app.py
```

2. Open your browser at http://127.0.0.1:3000/ (app runs on port 3000 by default)

Default test credentials

- Locators (locatore):
	- adam97@gmail.com / adam97
	- bob64@gmail.com / bob64
- Clients (regular users):
	- alice94@gmail.com / alice94
	- alessandra03@gmail.com / alessandra03

Notes, assumptions and caveats
- The app stores images in the `static/` folder using generated filenames. Uploaded images are resized/cropped using Pillow.
- The DAO modules use direct SQLite connections (`sqlite3.connect('db/affitti.db')`). Ensure `db/affitti.db` is present and readable by the app.
- The app sets `app.config['SECRET_KEY']` in `app.py` with a hard-coded value. For production, move secrets to environment variables.
- There is no automated migration or schema management; if you need to recreate the database, ask for the schema or export a working `affitti.db`.
- This README assumes a local development run. The app was deployed previously on PythonAnywhere.

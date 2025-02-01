from flask import Flask, request, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import fields
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from json_menu import json_file, JSONAdminView
import time
import piexif
import json
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/live/src'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#login_manager.login_view = 'login'

admin = Admin()
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class JSONField(fields.JSONField):
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return json.dumps(self.data, ensure_ascii=False, indent=2)
        else:
            return ''

class JSONView(ModelView):
    form_overrides = {
        'my_field': JSONField,
    }

admin.add_view(ModelView(User, db.session))
admin.add_view(JSONAdminView(name="Manage JSON", endpoint="json_admin"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def insert_photo(lat, lon, photo, time, author):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data.append({"lat": lat, "lon": lon, "photo": photo, "time": time, "author": author})
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def get_latlong(file):
    try:
        img = Image.open(file)
        exif_data = piexif.load(img.info.get("exif"))
        if not exif_data:
            return None, None
        gps_data = exif_data.get("GPS", {})
    
        if not gps_data:
            return None, None
    
        def convert_to_degrees(value):
            """Convert GPS coordinates to degrees format"""
            d, m, s = value
            return d[0] / d[1] + (m[0] / m[1]) / 60 + (s[0] / s[1]) / 3600
    
        lat = convert_to_degrees(gps_data[2]) if 2 in gps_data else None
        lon = convert_to_degrees(gps_data[4]) if 4 in gps_data else None
    
        if 1 in gps_data and gps_data[1] == b'S':  # Latitude South
            lat = -lat
        if 3 in gps_data and gps_data[3] == b'W':  # Longitude West
            lon = -lon
        return lat, lon
    except:
        return None, None
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not username or not email or not password:
            return render_template('register.html', msg='All fields are required')

        if not is_valid_email(email):
            return render_template('register.html', msg='Invalid email format')

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return render_template('register.html', msg='User already exists')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to login page after registration

    return render_template('register.html')  # Render the register page for GET requests


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', msg='Invalid credentials')

    return render_template('login.html')

@app.route('/update_email', methods = ['GET', 'POST'])
def update_email():
    if request.method == 'POST':
        new_email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=current_user.username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            user.email = new_email
            db.session.commit()
            return render_template('profile.html', msg="Pomyślnie zaktualizowano adres e-mail!")
        else:
            return render_template('profile.html', msg="Błędne hasło!")

@app.route('/update_password', methods = ['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(username=current_user.username).first()
        if user and (user.email == email and password == confirm_password):
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            return render_template('profile.html', msg="Pomyślnie zaktualizowano hasło!")
        else:
            return render_template('profile.html', msg="Błędny e-mail!")
        
@app.route('/delete_account', methods = ['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        password = request.form.get('password')
        checkbox = request.form.get('master_safe')
        user = User.query.filter_by(username=current_user.username).first()
        if checkbox:
            if user and bcrypt.check_password_hash(user.password, password):
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                return render_template('profile.html', msg="Błędne hasło!")
        else:
            return render_template('profile.html', msg="Opcja jest nieodwracalna i wymaga dodatkowego zatwierdzenia.")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/parrot_map')
def parrot_map():
    return render_template('parrot_map.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        loc_option = request.form['latlong_option']
        f = request.files['file']
        if not f:
            return render_template('parrot_map.html', msg='Nie załączono żadnego zdjęcia!')
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(path)
        print('file uploaded successfully')
        if(loc_option == 'exif'):
            lat, lon = get_latlong(path)
            if(lat == None or lon == None):
                return render_template('parrot_map.html', msg='Nie udało odczytać się lokalizacji z obrazu!')
            else:
                insert_photo(lat, lon, f.filename, time.time(), current_user.username)
        elif(loc_option == 'manual' or loc_option == 'gps'):
            insert_photo(request.form['lat'], request.form['lon'], f.filename, int(time.time()), current_user.username)
        return redirect(url_for('parrot_map'))

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin.init_app(app)
    app.run(host='0.0.0.0', port='5000', debug=True)

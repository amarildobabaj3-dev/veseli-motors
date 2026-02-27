from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_master_final_2026'

# Konfigurimi i Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'motors_final.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modeli i Perdoruesit
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Modeli i Makines (Me 4 foto dhe opsionet e plota)
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50))
    modeli = db.Column(db.String(50))
    viti = db.Column(db.Integer)
    cmimi = db.Column(db.Float)
    karburanti = db.Column(db.String(20))
    kambio = db.Column(db.String(20))
    kilometrat = db.Column(db.Integer)
    foto1 = db.Column(db.Text)
    foto2 = db.Column(db.Text)
    foto3 = db.Column(db.Text)
    foto4 = db.Column(db.Text)
    celulari = db.Column(db.String(20))
    pershkrimi = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# KRIJIMI I DATABASE DHE ADMINIT TE PERHERSHEM
with app.app_context():
    db.create_all()
    # Kjo e ben qe 'pronari' te jete gjithmone aktiv
    admin_exists = User.query.filter_by(username='pronari').first()
    if not admin_exists:
        new_admin = User(username='pronari', password='saadi123')
        db.session.add(new_admin)
        db.session.commit()
        print("Admini 'pronari' u aktivizua me sukses!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if not User.query.filter_by(username=user).first():
            new_user = User(username=user, password=pw)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/salloni')
def salloni():
    query = request.args.get('search')
    # Renditja sipas vitit (desc) - Makinat e reja dalin te parat
    if query:
        makinat = Makina.query.filter(Makina.marka.contains(query)).order_by(Makina.viti.desc()).all()
    else:
        makinat = Makina.query.order_by(Makina.viti.desc()).all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/detaje/<int:id>')
def detaje(id):
    makina = Makina.query.get_or_404(id)
    return render_template('detajet.html', makina=makina)

@app.route('/shto', methods=['GET', 'POST'])
def shto():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        m = Makina(
            marka=request.form.get('marka'), modeli=request.form.get('modeli'),
            viti=request.form.get('viti'), cmimi=request.form.get('cmimi'),
            karburanti=request.form.get('karburanti'), kambio=request.form.get('kambio'),
            kilometrat=request.form.get('kilometrat'), celulari=request.form.get('celulari'),
            foto1=request.form.get('foto1'), foto2=request.form.get('foto2'),
            foto3=request.form.get('foto3'), foto4=request.form.get('foto4'),
            pershkrimi=request.form.get('pershkrimi'), user_id=session['user_id']
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/fshij/<int:id>')
def fshij(id):
    m = Makina.query.get(id)
    if not m: return redirect(url_for('salloni'))
    # Pronari fshin cdo makine, te tjeret vetem te tyren
    if session.get('username') == 'pronari' or m.user_id == session.get('user_id'):
        db.session.delete(m)
        db.session.commit()
    return redirect(url_for('salloni'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
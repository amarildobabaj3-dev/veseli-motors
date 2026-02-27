from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_premium_key'

# LIDHJA ME DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(app)

# MODELI I PËRDORUESIT
class Perdoruesi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# MODELI I MAKINËS
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50))
    modeli = db.Column(db.String(50))
    viti = db.Column(db.Integer)
    cmimi = db.Column(db.Integer)
    karburanti = db.Column(db.String(20))
    kambio = db.Column(db.String(20))
    kilometrat = db.Column(db.String(50))
    celulari = db.Column(db.String(20)) # Numri i WhatsApp
    foto1 = db.Column(db.Text)
    foto2 = db.Column(db.Text)
    foto3 = db.Column(db.Text)
    foto4 = db.Column(db.Text)
    pershkrimi = db.Column(db.Text)
    user_id = db.Column(db.Integer)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = Perdoruesi(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = Perdoruesi.query.filter_by(username=u, password=p).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            # Këtu verifikohet admini
            if u == 'pronari' and p == 'saadi123':
                session['is_admin'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/salloni')
def salloni():
    # Renditja: Viti më i ri del i pari
    makinat = Makina.query.order_by(Makina.viti.desc()).all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/shto', methods=['GET', 'POST'])
def shto_makine():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        reja = Makina(
            marka=request.form['marka'], modeli=request.form['modeli'],
            viti=request.form['viti'], cmimi=request.form['cmimi'],
            karburanti=request.form['karburanti'], kambio=request.form['kambio'],
            kilometrat=request.form['kilometrat'], celulari=request.form['celulari'],
            foto1=request.form['foto1'], foto2=request.form.get('foto2', ''),
            foto3=request.form.get('foto3', ''), foto4=request.form.get('foto4', ''),
            pershkrimi=request.form['pershkrimi'], user_id=session['user_id']
        )
        db.session.add(reja)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/fshij/<int:id>')
def fshij_makine(id):
    makina = Makina.query.get_or_4_0_4(id)
    # Vetëm admini ose ai që e ka hedhur makinën mund ta fshijë
    if session.get('is_admin') or (session.get('user_id') == makina.user_id):
        db.session.delete(makina)
        db.session.commit()
    return redirect(url_for('salloni'))

@app.route('/makina/<int:id>')
def detajet(id):
    makina = Makina.query.get_or_4_0_4(id)
    return render_template('detajet.html', makina=makina)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Krijimi i llogarisë tënde automatikisht
        admin = Perdoruesi.query.filter_by(username='pronari').first()
        if not admin:
            admin_i_ri = Perdoruesi(username='pronari', password='saadi123')
            db.session.add(admin_i_ri)
            db.session.commit()
    app.run(debug=True)
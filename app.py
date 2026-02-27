from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_secret'

# LIDHJA ME DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(app)

# MODELI I PLOTË I MAKINËS
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50))
    modeli = db.Column(db.String(50))
    viti = db.Column(db.Integer)
    cmimi = db.Column(db.Integer)
    karburanti = db.Column(db.String(20))
    kambio = db.Column(db.String(20))
    kilometrat = db.Column(db.String(50))
    celulari = db.Column(db.String(20)) 
    foto1 = db.Column(db.Text)
    foto2 = db.Column(db.Text)
    foto3 = db.Column(db.Text)
    foto4 = db.Column(db.Text)
    pershkrimi = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/salloni')
def salloni():
    makinat = Makina.query.all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/shto', methods=['GET', 'POST'])
def shto_makine():
    if request.method == 'POST':
        reja = Makina(
            marka=request.form['marka'],
            modeli=request.form['modeli'],
            viti=request.form['viti'],
            cmimi=request.form['cmimi'],
            karburanti=request.form['karburanti'],
            kambio=request.form['kambio'],
            kilometrat=request.form['kilometrat'],
            celulari=request.form['celulari'],
            foto1=request.form['foto1'],
            foto2=request.form.get('foto2', ''),
            foto3=request.form.get('foto3', ''),
            foto4=request.form.get('foto4', ''),
            pershkrimi=request.form['pershkrimi']
        )
        db.session.add(reja)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/makina/<int:id>')
def detajet(id):
    makina = Makina.query.get_or_4_0_4(id)
    return render_template('detajet.html', makina=makina)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
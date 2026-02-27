from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_top_secret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'veseli_final.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50), nullable=False)
    modeli = db.Column(db.String(50), nullable=False)
    viti = db.Column(db.Integer)
    cmimi = db.Column(db.Float)
    karburanti = db.Column(db.String(20))
    kambio = db.Column(db.String(20))
    kilometrat = db.Column(db.Integer)
    foto_url = db.Column(db.String(500))
    foto_2 = db.Column(db.String(500))
    pershkrimi = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/salloni')
def salloni():
    makinat = Makina.query.all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/makina/<int:id>')
def detajet(id):
    makina = Makina.query.get_or_404(id)
    return render_template('detajet.html', makina=makina)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['is_admin'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/shto', methods=['GET', 'POST'])
def shto():
    if not session.get('is_admin'): return redirect(url_for('home'))
    if request.method == 'POST':
        m = Makina(
            marka=request.form['marka'], modeli=request.form['modeli'],
            viti=request.form['viti'], cmimi=request.form['cmimi'],
            karburanti=request.form['karburanti'], kambio=request.form['kambio'],
            kilometrat=request.form['kilometrat'], foto_url=request.form['foto'],
            foto_2=request.form['foto2'], pershkrimi=request.form['pershkrimi']
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
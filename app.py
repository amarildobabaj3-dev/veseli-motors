from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_premium_key'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'veseli_v4.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelet
class Perdoruesi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50), nullable=False)
    modeli = db.Column(db.String(50), nullable=False)
    viti = db.Column(db.Integer, nullable=False)
    cmimi = db.Column(db.Float, nullable=False)
    pershkrimi = db.Column(db.Text)
    foto_url = db.Column(db.String(200))

with app.app_context():
    db.create_all()
    # Krijon adminin automatikisht nese nuk ekziston
    if not Perdoruesi.query.filter_by(username='admin').first():
        admin = Perdoruesi(username='admin', password='admin123', is_admin=True)
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/salloni')
def salloni():
    search = request.args.get('search')
    if search:
        makinat = Makina.query.filter(Makina.marka.contains(search) | Makina.modeli.contains(search)).all()
    else:
        makinat = Makina.query.all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/makina/<int:id>')
def detajet(id):
    makina = Makina.query.get_or_404(id)
    return render_template('detajet.html', makina=makina)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Perdoruesi.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        ne_user = Perdoruesi(username=request.form['username'], password=request.form['password'])
        db.session.add(ne_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/shto', methods=['GET', 'POST'])
def shto():
    if not session.get('is_admin'): return redirect(url_for('home'))
    if request.method == 'POST':
        m = Makina(marka=request.form['marka'], modeli=request.form['modeli'], 
                   viti=request.form['viti'], cmimi=request.form['cmimi'],
                   pershkrimi=request.form['pershkrimi'], foto_url=request.form['foto'])
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
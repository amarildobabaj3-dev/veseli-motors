from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_ultimate_key'

# Konfigurimi i Databazës
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'motors_final.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelet
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50))
    modeli = db.Column(db.String(50))
    viti = db.Column(db.Integer)
    cmimi = db.Column(db.Float)
    karburanti = db.Column(db.String(20))
    kambio = db.Column(db.String(20))
    kilometrat = db.Column(db.Integer)
    foto_url = db.Column(db.Text) # E bera Text per Copy-Paste te gjate
    pershkrimi = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

# --- LOGJIKA E FAQES ---

@app.route('/')
def index():
    # Nese eshte i loguar, e dergon direkt te Salloni
    if 'user_id' in session:
        return redirect(url_for('salloni'))
    # Nese JO, e dergon te Sign Up qe te krijoje llogari
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('salloni'))
        
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if User.query.filter_by(username=user).first():
            return "Ky emër ekziston! Provo tjetër."
        
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
            # KETU BEHET TI PRONAR
            if user.username == 'pronari':
                session['is_admin'] = True
            return redirect(url_for('salloni'))
    return render_template('login.html')

@app.route('/salloni')
def salloni():
    if 'user_id' not in session:
        return redirect(url_for('signup'))
    makinat = Makina.query.all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/shto', methods=['GET', 'POST'])
def shto():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        m = Makina(
            marka=request.form.get('marka'), modeli=request.form.get('modeli'),
            viti=request.form.get('viti'), cmimi=request.form.get('cmimi'),
            karburanti=request.form.get('karburanti'), kambio=request.form.get('kambio'),
            kilometrat=request.form.get('kilometrat'), foto_url=request.form.get('foto'),
            pershkrimi=request.form.get('pershkrimi'), owner_id=session['user_id']
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/fshij/<int:id>')
def fshij(id):
    # Vetem ti si pronari mund te fshish cdo makine
    if not session.get('is_admin'):
        return "Nuk ke leje!", 403
    makina = Makina.query.get(id)
    if makina:
        db.session.delete(makina)
        db.session.commit()
    return redirect(url_for('salloni'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signup'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
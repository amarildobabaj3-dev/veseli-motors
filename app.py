from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_sekret_shume'

# Konfigurimi i Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'veseli_motors.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelimi i Makines
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50), nullable=False)
    modeli = db.Column(db.String(50), nullable=False)
    viti = db.Column(db.Integer, nullable=False)
    cmimi = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    makinat = Makina.query.all()
    # Shikon nëse përdoruesi është admin për të treguar butonin e shtimit
    is_admin = session.get('admin_logged_in', False)
    return render_template('index.html', makinat=makinat, is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Këtu vendos username dhe pass tëndin
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/shto', methods=['GET', 'POST'])
def shto_makine():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        m = Makina(
            marka=request.form.get('marka'),
            modeli=request.form.get('modeli'),
            viti=request.form.get('viti'),
            cmimi=request.form.get('cmimi')
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('shto_makine.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
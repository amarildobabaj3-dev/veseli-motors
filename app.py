from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'veseli_motors_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veseli_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tabela e makinave në Database
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emri = db.Column(db.String(100))
    cmimi = db.Column(db.String(20))
    foto = db.Column(db.String(500))
    viti = db.Column(db.String(10))
    numri_kontaktit = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salloni')
def salloni():
    makinat = Makina.query.all()
    return render_template('salloni.html', makinat=makinat)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vetëm ti me këto të dhëna bëhesh Admin
        if request.form.get('username') == 'admin' and request.form.get('password') == 'veseli123':
            session['admin'] = True
            return redirect(url_for('salloni'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Këtu e dërgojmë te login sapo regjistrohet
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/shto_makine', methods=['GET', 'POST'])
def shto_makine():
    if request.method == 'POST':
        m = Makina(
            emri=request.form.get('emri'), 
            cmimi=request.form.get('cmimi'), 
            foto=request.form.get('foto'), 
            viti=request.form.get('viti'),
            numri_kontaktit=request.form.get('numri')
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')

@app.route('/fshij/<int:id>')
def fshij(id):
    if 'admin' in session: # Kontrolli i sigurisë për ty
        m = Makina.query.get(id)
        if m:
            db.session.delete(m)
            db.session.commit()
    return redirect(url_for('salloni'))

if __name__ == '__main__':
    app.run(debug=True)
    # Tabela e re me opsionet që kërkove
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emri = db.Column(db.String(100))
    cmimi = db.Column(db.String(20))
    foto = db.Column(db.String(500))
    foto2 = db.Column(db.String(500)) # Foto e dytë
    foto3 = db.Column(db.String(500)) # Foto e tretë
    viti = db.Column(db.String(10))
    karburanti = db.Column(db.String(20)) # Opsioni i ri
    pershkrimi = db.Column(db.Text)      # Hapësira për përshkrim
    numri_kontaktit = db.Column(db.String(20))

@app.route('/shto_makine', methods=['GET', 'POST'])
def shto_makine():
    if request.method == 'POST':
        m = Makina(
            emri=request.form.get('emri'), 
            cmimi=request.form.get('cmimi'), 
            foto=request.form.get('foto'),
            foto2=request.form.get('foto2'),
            foto3=request.form.get('foto3'),
            viti=request.form.get('viti'),
            karburanti=request.form.get('karburanti'),
            pershkrimi=request.form.get('pershkrimi'),
            numri_kontaktit=request.form.get('numri')
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('salloni'))
    return render_template('shto_makine.html')
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 
    
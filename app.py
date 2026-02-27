from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'veseli_motors_sekret'

# Konfigurimi i Database
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'veseli_final.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelimi i Makines
class Makina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(50), nullable=False)
    modeli = db.Column(db.String(50), nullable=False)
    viti = db.Column(db.Integer, nullable=False)
    cmimi = db.Column(db.Float, nullable=False)

# Krijimi i Database automatikisht
with app.app_context():
    db.create_all()

# Faqja Kryesore (Salloni)
@app.route('/')
def index():
    makinat = Makina.query.all()
    return render_template('index.html', makinat=makinat)

# Faqja per te shtuar makina
@app.route('/shto', methods=['GET', 'POST'])
def shto_makine():
    if request.method == 'POST':
        m = Makina(
            marka=request.form['marka'],
            modeli=request.form['modeli'],
            viti=request.form['viti'],
            cmimi=request.form['cmimi']
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('shto_makine.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
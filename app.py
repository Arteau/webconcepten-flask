from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from logging.handlers import RotatingFileHandler
# from flask_session import Session
import sqlite3 as sql
import sys
from sqlite3 import Error
from flask import g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from pprint import pprint
from base64 import b64encode

app = Flask(__name__)

# SESSION_TYPE = "redis"
# app.config.from_object(__name__)
# Session(app)


class RegisterForm(Form):
    name = StringField('Naam', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Paswoord', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Paswoorden zijn niet gelijk aan elkaar.')
    ])
    confirm = PasswordField('Confirmeer paswoord')

DATABASE = 'D:/School/WebConcepten/webconcepten-flask/school.db'

def connect_db():
    return sql.connect(DATABASE)

def getLeraarData(c):
    c.execute("SELECT id FROM leraren")
    leraarId = c.fetchall()
    c.execute("SELECT naam FROM leraren")
    leraarNamen = c.fetchall()
    c.execute("SELECT voornaam FROM leraren")
    leraarVoornamen = c.fetchall()
    c.execute("SELECT foto FROM leraren")
    leraarFotos = c.fetchall()
    c.execute("SELECT email FROM leraren")
    leraarEmails = c.fetchall()
    leraarData = {'id' : leraarId, 'namen' : leraarNamen, 'voornamen' : leraarVoornamen, 'fotos' : leraarFotos, 'emails' : leraarEmails}
    return leraarData

def getRichtingData(c):
    c.execute("SELECT id FROM richtingen")
    richtingId = c.fetchall()
    c.execute("SELECT naam FROM richtingen")
    richtingNamen = c.fetchall()
    c.execute("SELECT beschrijving FROM richtingen")
    richtingBeschrijvingen = c.fetchall()
    richtingData = {'id' : richtingId, 'namen' : richtingNamen, 'beschrijvingen' : richtingBeschrijvingen}
    return richtingData    

def getKlasData(c):
    c.execute("SELECT id FROM klassen")
    klasId = c.fetchall()
    c.execute("SELECT naam FROM klassen")
    klasNamen = c.fetchall()
    c.execute("SELECT numCode FROM klassen")
    klasNumCodes = c.fetchall()
    c.execute("SELECT richting_id FROM klassen")
    klasRichtingId = c.fetchall()
    c.execute("SELECT leraar_id FROM klassen")
    klasLeraarId = c.fetchall()
    klasData = {'id' : klasId, 'namen' : klasNamen, 'numCode' : klasNumCodes}
    return klasData 


# Routes
@app.route('/')
def home():

    return render_template('home.html')
    
@app.route('/aanbod')
def aanbod():
    return render_template('aanbod.html')


@app.route('/wieiswie')
def wieiswie():
    return render_template('wieiswie.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/intranet')
def intranet():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM leraren")
    lerarenRows = cur.fetchall()
    cur.execute("SELECT * FROM richtingen")
    richtingenRows = cur.fetchall()
    cur.execute("SELECT * FROM klassen")
    klassenRows = cur.fetchall()
    conn.close()
    return render_template('intranet.html', lerarenRows = lerarenRows, richtingenRows = richtingenRows, klassenRows = klassenRows)

@app.route('/verwijderrichting/<int:entry_id>', methods=['POST', 'GET'])
def verwijderrichting(entry_id):
    if request.method == 'POST':      
        conn = connect_db()
        conn.row_factory = sql.Row
        cur = conn.cursor()
        verwijder_id = int(entry_id)
        cur.execute("DELETE FROM richtingen WHERE id=?", [verwijder_id])
        conn.commit()
        msg = "Richting succesvol verwijderd."
        conn.close()
        return render_template("resultaat.html", msg = msg)
    else:
        msg = "Richting is niet verwijderd, fout!"
        return render_template("resultaat.html", msg = msg)

@app.route('/nieuwerichting', methods=['POST', 'GET'])
def nieuwerichting():
    if request.method == 'POST':
        try:
            naam = request.form['naam']
            omschrijving = request.form['omschrijving']

            with connect_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO richtingen (naam, omschrijving) VALUES (?,?)", (naam, omschrijving))
                conn.commit()
                msg = "Richting toevoegen succesvol!"
        except:
            conn.rollback()
            msg = "Er is iets fout gegaan bij het toevoegen van een richting aan de database."

        finally:

            return render_template("resultaat.html", msg = msg)
            conn.close()

@app.route('/verwijderklas/<int:entry_id>', methods=['POST', 'GET'])
def verwijderklas(entry_id):
    if request.method == 'POST':      
        conn = connect_db()
        conn.row_factory = sql.Row
        cur = conn.cursor()
        verwijder_id = int(entry_id)
        cur.execute("DELETE FROM klassen WHERE id=?", [verwijder_id])
        conn.commit()
        msg = "Klas succesvol verwijderd."
        conn.close()
        return render_template("resultaat.html", msg = msg)
    else:
        msg = "Klas is niet verwijderd, fout!"
        return render_template("resultaat.html", msg = msg)

@app.route('/nieuweklas', methods=['POST', 'GET'])
def nieuweklas():
    if request.method == 'POST':
        try:
            naam = request.form['naam']
            numCode = request.form['numCode']
            leraar_id = request.form['leraar_id']
            richting_id = request.form['richting_id']

            with connect_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO klassen (naam, numCode, leraar_id, richting_id) VALUES (?,?,?,?)", (naam, numCode, leraar_id, richting_id))
                conn.commit()
                msg = "Klas toevoegen succesvol!"
        except:
            conn.rollback()
            msg = "Er is iets fout gegaan bij het toevoegen van een klas aan de database."

        finally:

            return render_template("resultaat.html", msg = msg)
            conn.close()

   
@app.route('/verwijderleraar/<int:entry_id>', methods=['POST', 'GET'])
def verwijderleraar(entry_id):
    if request.method == 'POST':      
        conn = connect_db()
        conn.row_factory = sql.Row
        cur = conn.cursor()
        verwijder_id = int(entry_id)
        cur.execute("DELETE FROM leraren WHERE id=?", [verwijder_id])
        conn.commit()
        msg = "Leraar succesvol verwijderd."
        conn.close()
        return render_template("resultaat.html", msg = msg)
    else:
        msg = "Leraar is niet verwijderd, fout!"
        return render_template("resultaat.html", msg = msg)

@app.route('/nieuweleraar', methods=['POST', 'GET'])
def nieuweleraar():
    if request.method == 'POST':
        try:
            naam = request.form['naam']
            voornaam = request.form['voornaam']
            email = request.form['email']
            foto = request.form['foto']

            with connect_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO leraren (naam, voornaam, email, foto) VALUES (?,?,?,?)", (naam, voornaam, email, foto))
                conn.commit()
                msg = "Leraar toevoegen succesvol!"
        except:
            conn.rollback()
            msg = "Er is iets fout gegaan bij het toevoegen van een leraar aan de database."

        finally:

            return render_template("resultaat.html", msg = msg)
            conn.close()


@app.route('/registreer', methods=['GET', 'POST'])
def registreren():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))


        flash("Je bent succesvol geregistreerd en kan nu inloggen.")

        redirect(url_for('home'))
    return render_template('registreer.html',form=form)



# Run
if __name__ == '__main__':
    app.secret_key='secretkey123'
    app.run(debug=True)
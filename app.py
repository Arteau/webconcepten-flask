from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import logging
from logging.handlers import RotatingFileHandler
import sqlite3 as sql
import sys
from sqlite3 import  Error
from flask import g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from pprint import pprint
from base64 import b64encode

app = Flask(__name__)

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
    # leraren = getLeraarData(cur)
    # richtingen = getRichtingData(cur)
    # klassen = getKlasData(cur)
    # return render_template('intranet.html', leraren = leraren, richtingen = richtingen, klassen = klassen)

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
            print('in post except')
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
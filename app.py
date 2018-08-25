from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

import sqlite3 as sql
import sys
from sqlite3 import  Error
from flask import g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from pprint import pprint

app = Flask(__name__)

class RegisterForm(Form):
    name = StringField('Naam', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Paswoord', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Paswoorden zijn niet gelijk aan elkaar.')
    ])
    confirm = PasswordField('Confirmeer paswoord')


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

    return render_template('intranet.html')


@app.route('/nieuweleraar',methods=['POST', 'GET'])
def nieuweleraar():
    msg = "method is niet post"
    pprint(vars(request.form['naam']))
    if request.method == 'POST':
        try:
            naam = request.form['naam']
            voornaam = request.form['voornaam']
            email = request.form['email']
            foto = request.form['foto']

            with sql.connect("D:\\School\WebConcepten\webconcepten-flask\school.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO leraars (naam, voornaam, email, foto) VALUES (?,?,?,?)", (naam, voornaam, email, foto))
                conn.commit()
                msg = "Leraar toevoegen succesvol!"
        except:
            print('in post except')
            conn.rollback()
            msg = "Er is iets fout gegaan bij het toevoegen van een leraar aan de database."

        finally:
            naam = request.form['naam']
            msg = str(naam)

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
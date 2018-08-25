from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Richtingen
import MySQLdb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

hostname = 'localhost'
username = 'root'
password = ''
database = 'schooldb'






Richtingen = Richtingen()

@app.route('/')
def home():
    conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute( '''SELECT voornaam FROM leeraars WHERE id = 1''' )
    data = cur.fetchall()
    # return render_template('home.html', data = str(data))
    return str(data)

@app.route('/aanbod')
def aanbod():
    return render_template('aanbod.html', richtingen = Richtingen)


class RegisterForm(Form):
    name = StringField('Naam', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Paswoord', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Paswoorden zijn niet gelijk aan elkaar.')
    ])
    confirm = PasswordField('Confirmeer paswoord')

@app.route('/registreer', methods=['GET', 'POST'])
def registreren():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('registreer.html',form=form)
    return render_template('registreer.html',form=form)







if __name__ == '__main__':
    app.run(debug=True)
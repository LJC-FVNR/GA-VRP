import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import GAN as gan
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DATABASE']='wofo.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY']='development key'
app.config['USERNAME']='admin'
app.config['PASSWORD']='default'

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.before_request
def before_request():
    g.db = connect_db()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, gadk=str(cX), imagename='images/drawbestline.jpg')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/gad', methods=['GET', 'POST'])
def gad():
    return render_template('new.html', gadk='X:'+str(cX) + '   Y:' + str(cY), imagename1='images/scatter.jpg')

@app.route('/process', methods=['GET', 'POST'])
def process():
    tsp = gan.GA(50, 300, 0.25, 0.02, cLabel, cX, cY, cD, dLabel, dX, dY, (1, 1))
    tsp.process()
    tsp.drawgen()
    tsp.drawbestline()
    path = tsp.bestcode[-1]
    cal = True
    return render_template('new2.html', gadk='X:'+str(cX) + '   Y:' + str(cY), imagename1='images/scatter.jpg'
                           , imagename2='images/drawbestline.jpg', path=str(path))

if __name__ == '__main__':
    customer = pd.read_csv('Customer.csv')
    distribution = pd.read_csv("Distribution.csv")
    cLabel = np.array(customer.iloc[:, 0])
    cX = np.array(customer.iloc[:, 1])
    cY = np.array(customer.iloc[:, 2])
    cD = np.array(customer.iloc[:, 3])
    dLabel = np.array(distribution.iloc[:, 0])
    dX = np.array(distribution.iloc[:, 1])
    dY = np.array(distribution.iloc[:, 2])
    origin = (1, 1)
    plt.plot(cX, cY, 'o')
    plt.plot(dX, dY, 'o')
    plt.plot(1, 1, 'o')
    for i in range(cX.shape[0]):
        plt.text(cX[i], cY[i], cLabel[i], family='serif', ha='right', wrap=True)
        plt.text(cX[i], cY[i]+0.5, 'Demand:'+cD[i], family='serif', ha='right', wrap=True)
    for i in range(dX.shape[0]):
        plt.text(dX[i], dY[i], dLabel[i], family='serif', ha='right', wrap=True)
    plt.savefig('./static/images/scatter.jpg')
    plt.show()
    cal = False
    app.run(debug=True)

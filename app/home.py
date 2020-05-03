from flask import Flask, request, redirect, render_template, json, session, jsonify,url_for
from app import app,database

@app.route('/home')
def home():
    sess = json.loads(session['user_auth'])
    first = sess.get('_FirstName')
    last = sess.get('_LastName')
    return render_template("home.html", name=first+' '+last)
from flask import Flask, render_template, request, redirect
from app import app

@app.route('/login')
def login():
    return render_template('login.html')

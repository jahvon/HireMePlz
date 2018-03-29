from flask import Flask, render_template, request, redirect
from app import app

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('registration')
def registration():
    return render_template('registration.html')
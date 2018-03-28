from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
from app import views, models

db = models.db

# Load default config and override config from an environment variable
app.config.update(dict(
	DEBUG=True,
    SECRET_KEY="KrabbyPattyFormula",
	SQLALCHEMY_TRACK_MODIFICATIONS=False,
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'hireme.db')
))

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()

    db.session.commit()

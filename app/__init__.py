from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
from app import views, models

db = models.db
Employer = models.Employers
Applicants = models.Applicants
Listings = models.Listings
Applications = models.Applications

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

    # Create Users
    models.insertApplicant(None, "jahvon", "123456", "jmd179@pitt.edu", "Introduction", "experience", "education", "skills")

    db.session.commit()

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

	models.insertApplicant("jahvon", "123456", "jmd179@pitt.edu", "Introduction", "experience", "education", "skills", "achievements")
	models.insertEmployer("University of Pittsburgh", "123456", "pitt@pitt.edu", "description")
	models.insertListing(1, "Software engineer", "description")
        models.insertListing(1, "QA Tester", "description")
        models.insertListing(1, "Project Manager", "description")
        models.insertListing(1, "Software Development Intern")
	models.insertApplication(1, 1, 1)

	db.session.commit()

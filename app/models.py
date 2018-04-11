from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


##Applicant Profile Information
##ID: Integer, Primary Key
##Username: String, MUST BE UNIQUE
#Password: String
##Email: String, MUST BE UNIQUE
##Introduction: String
##Experience: String
##Education: String
##Skills: String
##Achievements: String

##ID Field is referenced in Applications
class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    introduction = db.Column(db.String(500), unique = False, nullable = False)
    experience = db.Column(db.String(500), unique = False, nullable = False)
    education = db.Column(db.String(500), unique = False, nullable = False)
    skills = db.Column(db.String(500), unique = False, nullable = False)
    achievements = db.Column(db.String(500), unique = True, nullable = False)

    applications = db.relationship('Applications', backref = 'applicants', lazy = True)


##Employer Profile Information
##ID: Integer, Primary Key
##Name: String, Unique
##Email: String, NOT UNIQUE (more convenient testing)
##Description: String

##ID Field is referenced as a foreign key in 'Listings' and 'Applications' tables
class Employers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(80), unique = False, nullable = False)
    description = db.Column(db.String(80), unique = False, nullable = False)

    listings = db.relationship('Listings', backref = 'employer_listings', lazy = True)
    applications = db.relationship('Applications', backref = 'employer_applications', lazy = True)



##Stores information about each job listing
##ID: Integer, Primary Key
##Employer_ID: Integer, Primary Key, Foreign Key referencing Employers(ID)
##Description: String

##Has a value (ID, in this case) used as a foreign key in Applications
class Listings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_ID = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    location = db.Column(db.String(80), nullable = False)
    employer = db.Column(db.String(80), nullable = False)
    posted = db.Column(db.DateTime, nullable=False,default=datetime.now())
    description = db.Column(db.String(500), nullable = False)

    applications = db.relationship('Applications', backref = 'listing_applications', lazy = True)

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    applicant_ID = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable = False)
    listing_ID = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable = False)
    employer_ID = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable = False)
    status = db.Column(db.String(80), nullable = False, default="Received")

class Skipped(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    applicant_ID = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable = False)
    listing_ID = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable = False)

##INSERT METHODS##

def insertApplicant(username, password, email, introduction, experience, education, skills, achievements):

    new_applicant = Applicants( username=username, password=password, email=email,
            introduction=introduction, experience=experience, education=education, skills=skills,
            achievements = achievements)
    db.session.add(new_applicant)
    db.session.commit()

def insertEmployer(name, password, email, description):

    new_employer = Employers(name=name, password=password, email=email, description=description)
    db.session.add(new_employer)
    db.session.commit()

def insertListing(emp_ID, name, description, employer_name, location):

    new_listing = Listings(emp_ID=emp_ID, name=name, description=description, employer=employer_name, location=location)
    db.session.add(new_listing)
    db.session.commit()

def insertApplication(applicant_ID, listing_ID, employer_ID):

    new_application = Applications(applicant_ID=applicant_ID, listing_ID=listing_ID, employer_ID=employer_ID)
    db.session.add(new_application)
    db.session.commit()

def insertSkipped(applicant_ID, listing_ID):

    new_skip = Skipped(applicant_ID=applicant_ID, listing_ID=listing_ID)
    db.session.add(new_skip)
    db.session.commit()

##QUERY METHODS##

#Returns true if query can find a record matching the username and password
def tryLoginApplicant(uname, pw):
    user = Users.query.filter_by(username = uname, password = pw)
    if (user is None):
        return False
    else:
        return True

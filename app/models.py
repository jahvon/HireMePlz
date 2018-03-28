from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


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

    listings = db.relationship('Listings', backref = 'employers', lazy = True)
    applications = db.relationship('Applications', backref = 'employers', lazy = True)



##Stores information about each job listing
##ID: Integer, Primary Key
##Employer_ID: Integer, Primary Key, Foreign Key referencing Employers(ID)
##Description: String

##Has a value (ID, in this case) used as a foreign key in Applications
class Listings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_ID = db.Column(db.Integer, db.ForeignKey('employers.id'), primary_key = True,
            nullable = False)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(500), nullable = False)

    applications = db.relationship('Applications', backref = 'employers', lazy = True)

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    applicant_ID = db.Column(db.Integer, db.ForeignKey('applicant.id'),
            primary_key = True, nullable = False)
    listing_ID = db.Column(db.Integer, db.ForeignKey('listings.id'), primary_key = True,
            nullable = False)
    employer_ID = db.Column(db.Integer, db.ForeignKey('employers.id'), 
            primary_key = True, nullable = False)



##INSERT METHODS##

def insertApplicant(id, username, password, email, introduction, experience, education, skills):

    new_applicant = Applicants(id, username, password, email, introduction,
            experience, education, skills)
    db.session.add(new_applicant)
    db.session.commit()

def insertEmployer(id, name, password, email, description):

    new_employer = Employers(id, name, password, email, description)
    db.session.add(new_employer)
    db.session.commit()

def insertListing(id, emp_ID, name, description):

    new_listing = Listings(id, emp_ID, name, description)
    db.session.add(new_listing)
    db.session.commit()

def insertApplication(id, applicant_ID, listing_ID, employer_ID):

    new_application = Applications(id, applicant_ID, listing_ID, employer_ID)
    db.session.add(new_listing)
    db.session.commit()

##QUERY METHODS##

#Returns true if query can find a record matching the username and password
def tryLoginApplicant(uname, pw):
    user = Users.query.filter_by(username = uname, password = pw)
    if (user is None):
        return False
    else:
        return True

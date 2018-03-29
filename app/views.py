from flask import Flask, render_template, request, redirect, url_for, session
from app import app, models
import sys

@app.route("/")
def default():
	return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
	# Check if user already logged in
    if "username" in session:
	       return redirect(url_for("home"))
	# Take incoming info if not
    elif request.method == "POST":
        userType = "Employer"
        user = models.Employers.query.filter_by(email=request.form['email'], password=request.form['password']).first()
        if user is None:
            userType = "Applicant"
            user = models.Applicants.query.filter_by(email=request.form['email'], password=request.form['password']).first()

        if user is None:
            error = "Invalid login credentials"
        else:
            if userType is "Employer":
                session["username"] = user.name
            else:
                session["username"] = user.username
            session["usertype"] = userType
            session["userid"] = user.id
            return redirect(url_for("home"))
    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('usertype', None)
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_conf = request.form['conf_password']
        accType = request.form['accType']
        about = request.form['about']
        if models.Employers.query.filter_by(email=email).first() or models.Applicants.query.filter_by(email=email).first():
            error = "Email is taken"
            return render_template("registration.html", error=error)
        elif password != password_conf:
            error = "Passwords does not match"
            return render_template("registration.html", error=error)
        else:
            if accType == "Employer":
                models.insertEmployer(name=name, password=password, email=email, description=about)
            elif accType == "Applicant":
                models.insertApplicant(username=name, password=password, email=email,
                        introduction=about, experience="", education="", skills="",
                        achievements = "")
            info = request.form['name']+", your account has been created. You can log in now."
            return render_template("registration.html", info=info)
    else:
        return render_template("registration.html")

@app.route('/home')
def home():
	if "username" not in session:
		return redirect(url_for("login"))
	else:
		if session["usertype"] == "Applicant":
			return redirect(url_for("jobs"))
		elif session["usertype"] == "Employer":
			return redirect(url_for("applications"))

@app.route('/jobs', methods=["GET", "POST"])
def jobs():
    appliedApps = models.Applications.query.filter_by(applicant_ID=session['userid'])
    numApps = appliedApps.count()
    jobs = models.Listings.query.outerjoin(models.Applications, models.Listings.id==models.Applications.listing_ID).filter(models.Applications.applicant_ID!=session['userid']).first()
    return render_template('jobs.html', numApps=numApps, jobs=jobs)

@app.route('/applications')
def applications():
    return render_template('jobs.html')

@app.route('/profile/<userid>')
def profile(userid):
    user = models.Applicants.query.filter_by(id=userid).first()
    if session["usertype"] == "Applicant" and str(session["userid"]) != str(userid):
        return redirect(url_for("home"))
    else:
        return render_template('profile.html', user=user)

@app.route('/editprofile', methods=["GET", "POST"])
def editprofile():
    if session["usertype"] == "Employer":
        return redirect(url_for("home"))
    else:
        user = models.Applicants.query.filter_by(id=session['userid']).first()
        return render_template('editprofile.html', user=user)

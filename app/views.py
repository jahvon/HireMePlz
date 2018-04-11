from flask import Flask, render_template, request, redirect, url_for, session
from app import app, models
from datetime import datetime
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
        user = models.Employers.query.filter_by(
            email=request.form['email'], password=request.form['password']).first()
        if user is None:
            userType = "Applicant"
            user = models.Applicants.query.filter_by(
                email=request.form['email'], password=request.form['password']).first()

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
                models.insertEmployer(
                    name=name, password=password, email=email, description=about)
            elif accType == "Applicant":
                models.insertApplicant(username=name, password=password, email=email,
                                       introduction=about, experience="", education="", skills="",
                                       achievements="")
            info = request.form['name'] + \
                ", your account has been created. You can log in now."
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
	skippedApps = models.Skipped.query.filter_by(applicant_ID=session['userid'])
	numApps = appliedApps.count()
	job = models.Listings.query.order_by(models.Listings.id).first()
	curID = job.id
	while(appliedApps.filter_by(listing_ID=job.id).count()>0 or skippedApps.filter_by(listing_ID=job.id).count()>0):
		curID = curID+1
		job = models.Listings.query.filter(models.Listings.id > curID).order_by(models.Listings.id).first()
		if (job==None):
			break

	return render_template('jobs.html', numApps=numApps, job=job)


@app.route('/applications')
def applications():
    empApps = models.Listings.query.filter_by(emp_ID=session['userid'])
    numApps = empApps.count()
    jobs = empApps.all()
    return render_template('listings.html', numApps=numApps, listings=jobs)


@app.route('/applicants/<appid>')
def applicants(appid):
    application = models.Listings.query.filter_by(id=appid).first()
    applicants = models.Applications.query.join(models.Applicants, models.Applications.applicant_ID == models.Applicants.id).filter(
        models.Applications.listing_ID == appid).all()
    if session["usertype"] == "Applicant" or str(session["userid"]) != str(application.emp_ID):
        return redirect(url_for("home"))
    else:
        return render_template('jobapplicants.html', application=application, applicants=applicants)


@app.route('/profile/<userid>')
def profile(userid):
    user = models.Applicants.query.filter_by(id=userid).first()
    appliedApps = models.Applications.query.filter_by(applicant_ID=session['userid'])
    numApps = appliedApps.count()
    if session["usertype"] == "Applicant" and str(session["userid"]) != str(userid):
        return redirect(url_for("home"))
    else:
        return render_template('profile.html', user=user, numApps=numApps)


@app.route('/editprofile', methods=["GET", "POST"])
def editprofile():
    if session["usertype"] == "Employer":
        return redirect(url_for("home"))
    else:
        user = models.Applicants.query.filter_by(id=session['userid']).first()
        appliedApps = models.Applications.query.filter_by(applicant_ID=session['userid'])
        numApps = appliedApps.count()
        if request.method == "POST":
            about = request.form['introduction']
            achievements = request.form['achievements']
            skills = request.form['skills']
            education = request.form['education']
            work = request.form['experience']
            user.introduction = about
            user.achievements = achievements
            user.skills = skills
            user.education = education
            user.experience = work
            models.db.session.commit()
            return render_template('editprofile.html', user=user, numApps=numApps)
        else:
            return render_template('editprofile.html', user=user, numApps=numApps)


@app.route('/apply/<jobid>')
def applyToJob(jobid):
    job = models.Listings.query.filter_by(id=jobid).first()
    models.insertApplication(applicant_ID=int(
        session['userid']), listing_ID=int(jobid), employer_ID=job.emp_ID)
    return redirect(url_for("jobs"))

@app.route('/skip/<jobid>')
def skipJob(jobid):
    job = models.Skipped.query.filter_by(id=jobid).first()
    models.insertSkipped(applicant_ID=int(
        session['userid']), listing_ID=int(jobid))
    return redirect(url_for("jobs"))

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

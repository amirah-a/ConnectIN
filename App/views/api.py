from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for, flash
from App.controllers import user, auth
from flask_login import login_required, current_user

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def get_api_docs():
    return render_template('index.html')


@api_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userL = auth.authenticate(request.form["username"], request.form["password"])
        if userL:
            auth.login_user(userL, False)
            return redirect(url_for('api_views.profile'))
        else:
            return ("Login Failed")
    else:
        return render_template('login.html')

@api_views.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == "POST":
        test = user.is_user(request.form["username"], request.form["email"])
        if not test:
            temp = user.create_user(firstName=request.form["fname"], lastName=request.form["lname"],
            username=request.form["username"],  email=request.form["email"], password=request.form["password"] )
            
            auth.login_user(temp, False)
            return redirect(url_for('api_views.createProfile'))
        elif test== "Username":
            flash("Username is already in use")
        elif test == "Email":
            flash("Email is already in use")
        return redirect(url_for('api_views.signUp'))

    else:
        return render_template('signUp.html')

@api_views.route('/profile', methods=['GET'])
@login_required
def profile():
    return ("Welcome " + current_user.firstName)

@api_views.route('/create-profile', methods=['GET', 'POST'])
@login_required
def createProfile():
    if request.method == "POST":
        user.add_profile_data(id=current_user.id, year=request.form['year'], 
        degree=request.form['degree'], department=request.form['department'],
        faculty=request.form['faculty'], job=request.form['history'], profile_pic=request.files['upload_file'])
        return ("Sucess")

    return render_template('createProfile.html')

# route to display profile
@api_views.route('/user-profile', methods=['GET'])
def view_profile():
    return render_template('profile.html')

@api_views.route('/logout', methods=['GET'])
@login_required
def logout():
    auth.logout_user()
    return ("logged out")
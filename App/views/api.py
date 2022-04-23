from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for, flash, jsonify
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
            return redirect(url_for('api_views.view_profile', id=current_user.id))
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
        return redirect(url_for('api_views.dashboard'))

    return render_template('createProfile.html')

# route to display profile
@api_views.route('/user-profile/<id>', methods=['GET'])
@login_required
def view_profile(id):
    users= user.get_user_by_id(id)
    return render_template('profile.html', user=users)

# route to display profile
@api_views.route('/my-profile', methods=['GET'])
@login_required
def my_profile():
    return render_template('profile.html', user=current_user)

@api_views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        return redirect(url_for('api_views.search', type=request.form['queryType'], key=request.form['search']))
    users = user.get_all_users()
    return render_template('dashboard.html', users = users)

@api_views.route('/logout', methods=['GET'])
@login_required
def logout():
    auth.logout_user()
    return ("logged out")

@api_views.route('/search/<type>/<key>', methods=['GET'])
@login_required
def search(type, key):
    if type == "2":
        filterBy = "year"
    elif type == "3":
        filterBy = "degree"
    elif type == "4":
        filterBy = "department"
    elif type == "5":
        filterBy = "faculty"
    elif type == "6":
        filterBy = "experience"
    else:
        filterBy = "firstName"
    users = user.search_for_users(type, key)
    return render_template('dashboard.html', users = users)
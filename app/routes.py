from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import Registration, Login
from app.models import Users, Posts
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

posts = [
    {
        'title': "Post1",
        'author': "Bobby",
        'date': "2019/05/01",
        'time': "15:27:10",
        'content': "lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt ornare massa eget egestas purus viverra accumsan in nisl nisi scelerisque eu ultrices vitae auctor eu augue ut lectus arcu bibendum at varius vel pharetra vel turpis nunc eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim facilisis gravida neque"
    },
    {
        'title': "Post2",
        'author': "Bobby",
        'date': "2019/05/02",
        'time': "12:01:00",
        'content': "nisi porta lorem mollis aliquam ut porttitor leo a diam sollicitudin tempor id eu nisl nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit amet risus nullam eget felis eget nunc lobortis mattis aliquam faucibus purus in massa tempor nec feugiat nisl pretium fusce id velit ut tortor pretium viverra"
    },
    {
        'title': "Post3",
        'author': "Randy",
        'date': "2019/05/03",
        'time': "22:20:00",
        'content': "dolor purus non enim praesent elementum facilisis leo vel fringilla est ullamcorper eget nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum dui faucibus in ornare quam viverra orci sagittis eu volutpat odio facilisis mauris sit amet massa vitae tortor condimentum lacinia quis vel eros donec ac odio tempor"
    },
    {
        'title': "Post4",
        'author': "Dany",
        'date': "2019/05/04",
        'time': "08:08:00",
        'content': "proin fermentum leo vel orci porta non pulvinar neque laoreet suspendisse interdum consectetur libero id faucibus nisl tincidunt eget nullam non nisi est sit amet facilisis magna etiam tempor orci eu lobortis elementum nibh tellus molestie nunc non blandit massa enim nec dui nunc mattis enim ut tellus elementum sagittis"
    },
    {
        'title': "Post5",
        'author': "Seven of Nine",
        'date': "2019/05/05",
        'time': "11:34:30",
        'content': "pellentesque adipiscing commodo elit at imperdiet dui accumsan sit amet nulla facilisi morbi tempus iaculis urna id volutpat lacus laoreet non curabitur gravida arcu ac tortor dignissim convallis aenean et tortor at risus viverra adipiscing at in tellus integer feugiat scelerisque varius morbi enim nunc faucibus a pellentesque sit amet"
    }
]

@app.route("/")
def index():
    return render_template("index.html", title='studentDS', posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Registration()
    if form.validate_on_submit():
        #  Use validated form info to create a new user with username, email, and (hashed)password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username = form.username.data, email = form.email.data, password = hashed_pw, )
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created!", category='success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    #  If user is logged in and tries to access login page, redirect them to index
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #  Increment user's number of visits
            user.visited += 1
            db.session.commit()

            #  Log in user and redirect to page they were attempting to visit
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("index"))
        
        #  If submitted password doesn't match db, flash warning and keep on login page
        else:
            flash(f"Unsuccessful login, please check email and password", category="danger")
    return render_template("login.html", title="Log In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")    

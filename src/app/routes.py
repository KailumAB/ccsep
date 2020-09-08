from flask import render_template, flash, redirect, url_for, request, Markup, escape
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, SearchForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("index"))
    posts = Post.all_posts()
    return render_template("index.html", title="Home", form = form,
            posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/explore", methods=["GET"])
@login_required
def explore():
    form = SearchForm()
    search_term = request.values.get("search")
    posts = Post.all_posts()
    filtered_posts = None

    if search_term is not None:
        filtered_posts = None
        try:
            filtered_posts = db.session.query(Post).filter(text("body LIKE '%%%s%%'" % search_term)).all()
            #filtered_posts = db.session.query(Post).filter(Post.body.like(search_term)).all()
        except OperationalError as e:
            flash(str(e))
            return redirect(url_for("explore"))

    if filtered_posts is None or filtered_posts == "" or search_term == "":
        return render_template("explore.html", title="Explore", form=form, posts=posts, search_term=None)
    return render_template("explore.html", title="Explore", form=form, posts=filtered_posts, search_term=Markup(escape(search_term)))

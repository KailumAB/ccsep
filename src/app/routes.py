from flask import render_template, flash, redirect, url_for, request, Markup, escape
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, SearchForm, AdminForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return redirect(url_for("admin"))

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

# @app.route("/explore", methods=["GET"])
# @login_required
# def explore():
#     form = SearchForm()
#     search_term = request.values.get("search")
#     posts = Post.all_posts()
#     filtered_posts = None
#
#     if search_term is not None:
#         filtered_posts = None
#         try:
#             filtered_posts = db.session.query(Post).filter(text("body LIKE '%%%s%%'" % search_term)).all()
#             #filtered_posts = db.session.query(Post).filter(Post.body.like(search_term)).all()
#         except OperationalError as e:
#             flash(str(e))
#             return redirect(url_for("explore"))
#
#     if filtered_posts is None or filtered_posts == "" or search_term == "":
#         return render_template("explore.html", title="Explore", form=form, posts=posts, search_term=None)
#     return render_template("explore.html", title="Explore", form=form, posts=filtered_posts, search_term=Markup(escape(search_term)))

@app.route("/admin", methods=["GET"])
@login_required
def admin():
    form = AdminForm()
    search_term = request.values.get("search")
    id = request.values.get("id")
    engine = create_engine('mysql+pymysql://root:password@172.16.0.2:3306/demodb', echo=True)
    conn = engine.connect()
    result = None
    fields = {}
    id_list = None

    with engine.connect() as con:
        statement = text("""SELECT id FROM user ORDER BY id""")

        id_list = con.execute(statement).fetchall()

    if search_term is not None and id is not None:
        try:
            with engine.connect() as con:

                statement = text("""SELECT %s FROM user WHERE id = %s""" % (search_term, id))

                result = con.execute(statement).fetchone()
                for column, value in result.items():
                    fields = {**fields, **{column: value}}

        except (OperationalError, ProgrammingError) as e:
            return redirect(url_for("admin"))

    fields.pop('password', None)

    if result is None or id == "" or search_term == "":
        return render_template("admin.html", title="Explore", form=form, fields=fields, id_list=id_list, search_term=None)
    return render_template("admin.html", title="Explore", form=form, fields=fields, id_list=id_list, search_term=Markup(escape(search_term)))

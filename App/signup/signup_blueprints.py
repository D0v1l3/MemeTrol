from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from App import login_manager
from App.signup.signup_form import SignupForm
from App.signup.signup_models import User, db


signup_blueprints = Blueprint(
    "signup_blueprints", __name__, template_folder="templates", static_folder="static"
)


@signup_blueprints.route("/signup", methods=["GET", "POST"])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("home_blueprints.dashboard"))
        flash("A user already exists with that email address.")
    return render_template(
        "signup.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("login_blueprints.login"))

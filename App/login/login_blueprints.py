from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import current_user, login_user, login_required, logout_user

from App import login_manager
from App.login.login_form import LoginForm
from App.signup.signup_models import User

login_blueprints = Blueprint(
    "login_blueprints", __name__, template_folder="templates", static_folder="static"
)


@login_blueprints.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_blueprints.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home_blueprints.dashboard"))
        flash("Invalid username/password combination")
        return redirect(url_for("login_blueprints.login"))
    return render_template(
        "login.html",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
    )


@login_blueprints.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("login_blueprints.login"))

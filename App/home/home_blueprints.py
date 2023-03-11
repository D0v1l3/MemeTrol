import os.path

from flask import Blueprint, render_template, request, redirect, session
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageFont, ImageDraw
from App.signup.signup_models import Memes
from App import db
from pynter.pynter import generate_captioned


cwd = os.getcwd()
UPLOAD_FOLDER = cwd + "/App/static"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

home_blueprints = Blueprint(
    "home_blueprints", __name__, template_folder="templates", static_folder="static"
)


@home_blueprints.route("/", methods=["GET"])
def mainroute():
    record = Memes.query.all()

    return render_template(
        "main.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        body="You are now logged in!",
        record=record,
    )


@home_blueprints.route("/tmeme", methods=["GET"])
def topmeme():
    record = Memes.query.all()
    print(len(record))

    return render_template(
        "topmeme.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        body="You are now logged in!",
        record=record,
    )


@home_blueprints.route("/myaccount", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        file = request.files["myFile"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        return render_template(
            "index.html",
            title="Flask-Login Tutorial",
            template="dashboard-template",
            current_user=current_user,
            body="You are now logged in!",
            filename=file.filename,
        )
    return render_template(
        "index.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
        filename="",
    )


@home_blueprints.route("/savememe/<string:filename>")
@login_required
def saved(filename):
    record = Memes(name=filename, user_id=current_user.id)
    db.session.add(record)
    db.session.commit()
    return redirect("/myaccount")


@home_blueprints.route("/showpic/<string:filename>")
@login_required
def show(filename):
    return render_template(
        "index.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
        filename=filename,
    )


@home_blueprints.route("/mymemes")
@login_required
def my_memes():
    record = Memes.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "mymeme.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
        record=record,
    )


@home_blueprints.route("/delete/<int:id>")
@login_required
def delete_my_memes(id):
    record = Memes.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect("/mymemes")


@home_blueprints.route("/addtexttoimage/<string:filename>", methods=["GET", "POST"])
@login_required
def addtext(filename):
    if request.method == "POST":
        firsttext = str(request.form.get("uppertext"))

        image_path = UPLOAD_FOLDER + "/" + filename
        font_path = UPLOAD_FOLDER + "/fonts/montserrat/Montserrat-Black.ttf"

        image = Image.open(image_path)
        width, height = image.size

        white_height = 200
        new_image = Image.new("RGB", (width, height + white_height), color="white")
        new_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(new_image)
        text = firsttext.upper()
        font_size = 50
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (width - text_width) / 2
        text_y = height + (white_height - text_height) / 2
        draw.text((text_x, text_y), text, fill="black", font=font)

        new_image.save(os.path.join(UPLOAD_FOLDER, filename))

    return render_template(
        "index.html",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
        filename=filename,
    )

from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages
from sqlalchemy.sql.expression import false
from management.models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db

views = Blueprint("views", __name__)


@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note sort:)",category="error")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added !",category="success")
    messages = get_flashed_messages()
    return render_template("index.html", user=current_user if current_user.is_authenticated else None)
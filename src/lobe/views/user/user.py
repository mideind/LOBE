import traceback
import uuid

import click
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required, roles_accepted
from flask_security.utils import hash_password
from sqlalchemy import or_

from lobe.database_functions import resolve_order, sessions_day_info
from lobe.forms import (
    ExtendedRegisterForm,
    RoleForm,
    UserEditForm,
    VerifierRegisterForm,
)
from lobe.models import Recording, Role, Session, User, db

user = Blueprint("user", __name__, template_folder="templates")

# we want to convert this class to a click command
# and attach that command to the flask cli via the blueprint
# so that we can run it from the command line


@user.cli.command("add_default_roles")
def add_default_roles():
    roles = [
        {
            "name": "admin",
            "description": "Umsjónarhlutverk með aðgang að notendastillingum",
        },
        {
            "name": "Notandi",
            "description": "Venjulegur notandi með grunn aðgang",
        },
        {
            "name": "Greinir",
            "description": "Greinir með takmarkað aðgengi",
        },
    ]
    existing_roles = [role.name for role in Role.query.all()]
    for i, r in enumerate(roles):
        if r["name"] not in existing_roles:
            role = Role()
            role.name = r["name"]
            role.description = r["description"]
            db.session.add(role)
            print("Creating role:", r["name"])

    db.session.commit()


@user.cli.command("add")
@click.option("--email", prompt=True)
@click.option("--name", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def add_user(email: str, name: str, password: str):
    # we need to do the roles in the function because we need to query the db
    roles = Role.query.all()
    selected_roles = []
    if len(roles) > 0:
        role_select = None
        while role_select not in [r.id for r in roles]:
            click.echo("Select a role")
            role_select = int(
                input("".join(["[{}] - {} : {}\n".format(role.id, role.name, role.description) for role in roles]))
            )
        selected_roles.append(Role.query.get(role_select).name)
        app.user_datastore.create_user(
            email=email, password=hash_password(password), name=name, roles=selected_roles, uuid=uuid.uuid4()
        )
        db.session.commit()
        print("User with email {} has been created".format(email))


@user.route("/users/")
@login_required
@roles_accepted("admin")
def user_list():
    page = int(request.args.get("page", 1))
    users = User.query.order_by(
        resolve_order(
            User,
            request.args.get("sort_by", default="name"),
            order=request.args.get("order", default="desc"),
        )
    ).paginate(page=page, per_page=app.config["USER_PAGINATION"])
    return render_template("user_list.jinja", users=users, section="user")


@user.route("/users/<int:id>/")
@login_required
@roles_accepted("admin", "Notandi")
def user_detail(id):
    page = int(request.args.get("page", 1))
    user = User.query.get(id)
    recordings = (
        Recording.query.filter(Recording.user_id == id)
        .order_by(
            resolve_order(
                Recording,
                request.args.get("sort_by", default="created_at"),
                order=request.args.get("order", default="desc"),
            )
        )
        .paginate(page=page, per_page=app.config["RECORDING_PAGINATION"])
    )
    return render_template("user.jinja", user=user, recordings=recordings, section="user")


@user.route("/users/<int:id>/times", methods=["GET"])
@login_required
@roles_accepted("admin", "Notandi")
def user_time_info(id):
    user = User.query.get(id)
    sessions = Session.query.filter(or_(Session.user_id == user.id, Session.manager_id == user.id)).order_by(
        Session.created_at
    )

    day_info, total_est_work_time, total_session_duration = sessions_day_info(sessions, user)

    return render_template(
        "user_time.jinja",
        user=user,
        sessions=sessions,
        day_info=day_info,
        total_est_work_time=total_est_work_time,
        total_session_duration=total_session_duration,
    )


@user.route("/users/<int:id>/edit/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def user_edit(id):
    user = User.query.get(id)
    form = UserEditForm(obj=user)
    if request.method == "POST":
        try:
            form = UserEditForm(request.form, obj=user)
            if form.validate():
                form.populate_obj(user)
                db.session.commit()
                flash("Notanda var breytt", category="success")
        except Exception as error:
            app.logger.error("Error updating a user : {}\n{}".format(error, traceback.format_exc()))

    return render_template(
        "forms/model.jinja",
        user=user,
        form=form,
        type="edit",
        action=url_for("user.user_edit", id=id),
        section="user",
    )


@user.route("/users/<int:id>/toggle_admin/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def user_toggle_admin(id):
    ds_user = app.user_datastore.get_user(id)
    if ds_user.has_role("admin"):
        app.user_datastore.remove_role_from_user(ds_user, "admin")
        app.user_datastore.add_role_to_user(ds_user, "Notandi")
        flash("Notandi er ekki lengur vefstjóri", category="success")
    else:
        app.user_datastore.add_role_to_user(ds_user, "admin")
        app.user_datastore.remove_role_from_user(ds_user, "Notandi")
        flash("Notandi er nú vefstjóri", category="success")
    db.session.commit()
    return redirect(url_for("user.user_detail", id=id))


@user.route("/users/<int:id>/make_verifier/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def user_make_verifier(id):
    ds_user = app.user_datastore.get_user(id)
    app.user_datastore.add_role_to_user(ds_user, "Greinir")
    flash("Notandi er nú greinandi", category="success")
    db.session.commit()
    return redirect(url_for("user.user_detail", id=id))


@user.route("/users/create/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def user_create():
    form = ExtendedRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = app.user_datastore.create_user(
                name=form.name.data,
                email=form.email.data,
                password=hash_password(form.password.data),
                uuid=uuid.uuid4(),
                roles=["admin" if form.is_admin.data else "Notandi"],
            )
            form.populate_obj(new_user)
            db.session.commit()
            flash("Nýr notandi var búinn til", category="success")
            return redirect(url_for("user.user_list"))
        except Exception as error:
            app.logger.error("Error creating a user : {}\n{}".format(error, traceback.format_exc()))
            flash("Villa kom upp við að búa til nýjan notanda", category="warning")
    return render_template(
        "forms/model.jinja",
        form=form,
        type="create",
        action=url_for("user.user_create"),
        section="user",
    )


@user.route("/users/create_verifier", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def verifier_create():
    form = VerifierRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = app.user_datastore.create_user(
                name=form.name.data,
                email=form.email.data,
                password=hash_password(form.password.data),
                uuid=uuid.uuid4(),
                roles=["Greinir"],
            )
            form.populate_obj(new_user)

            flash("Nýr greinir var búinn til", category="success")
            return redirect(url_for("user.user_list"))

        except Exception as error:
            app.logger.error("Error creating a user : {}\n{}".format(error, traceback.format_exc()))
            flash("Villa kom upp við að búa til nýjan greini", category="warning")
    return render_template(
        "forms/model.jinja",
        form=form,
        type="create",
        action=url_for("user.verifier_create"),
        section="user",
    )


@user.route("/users/<int:id>/delete/")
@login_required
@roles_accepted("admin")
def delete_user(id):
    user = db.session.query(User).get(id)
    name = user.name
    db.session.delete(user)
    db.session.commit()
    flash("{} var eytt".format(name), category="success")
    return redirect(url_for("user.user_list"))


@user.route("/roles/create/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def role_create():
    form = RoleForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            role = Role()
            form.populate_obj(role)
            db.session.add(role)
            db.session.commit()
        except Exception as error:
            app.logger.error("Error creating a role : {}\n{}".format(error, traceback.format_exc()))
    return render_template(
        "forms/model.jinja",
        form=form,
        type="create",
        action=url_for("user.role_create"),
        section="role",
    )


@user.route("/roles/<int:id>/edit/", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def role_edit(id):
    role = Role.query.get(id)
    form = RoleForm(request.form, obj=role)

    if request.method == "POST" and form.validate():
        try:
            form.populate_obj(role)
            db.session.commit()
            flash("Hlutverki var breytt", category="success")
        except Exception as error:
            app.logger.error("Error updating a role : {}\n{}".format(error, traceback.format_exc()))
    return render_template(
        "forms/model.jinja",
        role=role,
        form=form,
        type="edit",
        action=url_for("user.role_edit", id=id),
        section="role",
    )

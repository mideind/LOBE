import traceback

import click
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_security import login_required, roles_accepted

from lobe.database_functions import resolve_order
from lobe.forms import ConfigurationForm
from lobe.models import ADMIN_ROLE, USER_ROLE, Collection, Configuration, db

configuration = Blueprint("configuration", __name__, template_folder="templates")


@configuration.cli.command("add_default")
def add_default():
    main_conf = Configuration.query.filter_by(name="Aðalstilling").count()
    if main_conf:
        click.echo("Configuration already exists.")
        return
    conf = Configuration()
    conf.name = "Aðalstilling"
    db.session.add(conf)
    db.session.commit()
    click.echo("Configuration added.")


@configuration.route("/confs/")
@login_required
@roles_accepted(ADMIN_ROLE, USER_ROLE)
def conf_list():
    page = int(request.args.get("page", 1))
    confs = Configuration.query.order_by(
        resolve_order(
            Configuration,
            request.args.get("sort_by", default="created_at"),
            order=request.args.get("order", default="desc"),
        )
    ).paginate(page=page, per_page=app.config["CONF_PAGINATION"])

    return render_template("conf_list.jinja", confs=confs, section="other")


@configuration.route("/confs/<int:id>/")
@login_required
@roles_accepted(ADMIN_ROLE, USER_ROLE)
def conf_detail(id):
    conf = Configuration.query.get(id)
    collections = Collection.query.filter(Collection.configuration_id == id)
    return render_template("conf.jinja", conf=conf, collections=collections, section="other")


@configuration.route("/confs/<int:id>/edit/", methods=["GET", "POST"])
@login_required
@roles_accepted(ADMIN_ROLE)
def edit_conf(id):
    conf = Configuration.query.get(id)
    form = ConfigurationForm(obj=conf)
    if request.method == "POST":
        try:
            form = ConfigurationForm(request.form, obj=conf)
            if form.validate():
                form.populate_obj(conf)
                db.session.commit()
                flash("Stillingum var breytt", category="success")
                return redirect(url_for("configuration.conf_detail", id=conf.id))
        except Exception as error:
            app.logger.error("Error updating a configuration : {}\n{}".format(error, traceback.format_exc()))

    return render_template(
        "forms/model.jinja",
        form=form,
        type="edit",
        action=url_for("configuration.edit_conf", id=id),
        section="other",
    )


@configuration.route("/confs/create/", methods=["GET", "POST"])
@login_required
@roles_accepted(ADMIN_ROLE)
def create_conf():
    form = ConfigurationForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            configuration = Configuration()
            form.populate_obj(configuration)
            db.session.add(configuration)
            db.session.commit()
            return redirect(url_for("configuration.conf_detail", id=configuration.id))
        except Exception as error:
            flash("Error creating configuration.", category="danger")
            app.logger.error("Error creating configuration {}\n{}".format(error, traceback.format_exc()))

    return render_template(
        "forms/model.jinja",
        form=form,
        action=url_for("configuration.create_conf"),
        section="other",
    )


@configuration.route("/confs/<int:id>/delete/", methods=["GET"])
@login_required
@roles_accepted(ADMIN_ROLE)
def delete_conf(id):
    conf = Configuration.query.get(id)
    name = conf.printable_name
    if conf.is_default:
        flash("Ekki er hægt að eyða aðalstillingum", category="warning")
        return redirect(conf.url)
    try:
        db.session.delete(conf)
        db.session.commit()
        flash(f"{name} var eytt", category="success")
    except Exception as error:
        app.logger.error("Error deleting a configuration : {}\n{}".format(error, traceback.format_exc()))
    return redirect(url_for("configuration.conf_list"))
    return redirect(url_for("configuration.conf_list"))

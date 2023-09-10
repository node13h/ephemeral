# Copyright (C) 2019 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import logging
import os

from flask import (
    Flask,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.middleware.proxy_fix import ProxyFix

from ephemeral.data import MessageNotFoundError, add_message, get_message

application = Flask(__name__)
application.wsgi_app = ProxyFix(
    application.wsgi_app, x_for=1, x_host=1, x_proto=1, x_port=1
)
application.secret_key = os.environ.get("EPHEMERAL_SECRET_KEY", None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@application.before_request
def csrf_protect():
    if request.method == "GET":
        if "_csrf_token" not in session:
            random_token = os.urandom(32)
            session["_csrf_token"] = base64.b64encode(random_token).decode("latin-1")

    elif request.method == "POST":
        token = session.get("_csrf_token", None)
        if not token or token != request.form.get("_csrf_token"):
            abort(403)


@application.route("/")
def root():
    return render_template("root.html")


@application.route("/show/<msg_id>", methods=["POST", "GET"])
def show(msg_id):
    if request.method == "POST":
        try:
            body = get_message(msg_id, request.form["pin"])
        except MessageNotFoundError:
            return render_template("not_found.html", msg_id=msg_id), 404
        else:
            logger.info("SHOW {}".format(msg_id))
            response = make_response(render_template("show.html", body=body))

            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

            return response

    return render_template("pin.html", csrf_token=session.get("_csrf_token", None))


@application.route("/link/<msg_id>")
def link(msg_id):
    return render_template(
        "link.html", url="{}".format(url_for("show", _external=True, msg_id=msg_id))
    )


@application.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        msg_id = add_message(request.form["body"], request.form["pin"])
        return redirect(url_for("link", msg_id=msg_id))
    else:
        return render_template("add.html", csrf_token=session.get("_csrf_token", None))

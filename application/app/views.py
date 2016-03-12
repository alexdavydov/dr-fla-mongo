from flask import Blueprint, request
from werkzeug import exceptions

from controllers import query_db, parse_input, insert_data, get_date

views = Blueprint('views', __name__)


@views.route("/count", methods=["GET"])
def count():
    if not request.args.get("uid") or not request.args.get("date"):
        raise exceptions.BadRequest("Missing required parameter")
    uid = int(request.args.get("uid"))
    (req_date, next_day) = get_date(request.args.get("date"))
    try:
        res = query_db(req_date, next_day, uid)
    except:
        raise exceptions.InternalServerError("Database query failed")
    return "{}".format(res)


@views.route("/store", methods=["POST"])
def store():
    if request.headers["Content-Type"] == "application/json":
        try:
            body = request.json
        except:
            raise exceptions.BadRequest("Bad JSON input")
    else:
        raise exceptions.UnsupportedMediaType(
            "Bad content type, expected application/json, got {}"
            .format(request.headers["Content-Type"]))
    insert_data(parse_input(body))
    return "OK"

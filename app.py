from flask import Flask, redirect, make_response, render_template, request, url_for
import dbmanager as db
from dbmanager import add_visitor
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def landing_page():
    uid = "silly"
    if request.method == 'GET':
        links = db.fetch_user_urls(uid)
        return render_template("dashboard.html", links=links)
    elif request.method == 'POST' and request.form.get("method") == 'PUT':
        short_url = request.form.get("short-link")
        long_url = request.form.get("long-link")
        new_short_url = request.form.get("new-short-link")
        isActive = request.form.get("isActive")
        if isActive == "on":
            isActive = 1
        else:
            isActive = 0
        db.update_url(shortURL=short_url, longURL=long_url, newShortURL=new_short_url, isActive=isActive)
        return redirect(url_for("landing_page"))
    elif request.method == 'DELETE':
        short_url = request.headers.get("short-link")
        db.delete_url(short_url)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    elif request.method == 'POST':
        #Registering/Deleting/Modifying a URL
        short_url = request.form.get("short-link")
        long_url = request.form.get("long-link")
        isActive = request.form.get("isActive")
        if isActive == "true":
            isActive = True
        else:
            isActive = False
        db.create_new_url(uid, short_url, long_url, isActive)
        return redirect(url_for("landing_page"))




@app.route("/favicon.ico")
def favicon():
    return "no"
@app.route("/<route>")
def reroute(route):
    new_route = db.fetch_long_url(route)
    if new_route is not None:
        db.add_visitor(route)
        return redirect(new_route,303)
    else:
        return "not found"


if __name__ == '__app__':
    db.create_tables()
    app.run("localhost", 8080)
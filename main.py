from flask import Flask, redirect, make_response, render_template
import dbmanager as db

app = Flask(__name__)

@app.route('/')
def landing_page():
    links = db.fetch_urls("silly")
    return render_template("dashboard.html", links=links)

@app.route("/favicon.ico")
def favicon():
    return "no"
@app.route("/<route>")
def reRoute(route):
    newRoute = db.fetch_long_url(route)
    if newRoute != None:
        return redirect(newRoute,303)
    else:
        return "not found"



if __name__ == '__main__':
    db.create_tables()
    app.run("localhost", 8080)
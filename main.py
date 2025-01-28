from flask import Flask, redirect, make_response
import dbmanager as db

app = Flask(__name__)

@app.route('/')
def landing_page():
    return "Hello!"

@app.route("/favicon.ico")
def favicon():
    return None
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
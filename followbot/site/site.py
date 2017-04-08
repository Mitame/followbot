from flask import render_template, request
from flask_oauthlib.client import OAuth, session
import os

from . import app, api

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        acct = request.form["acct"]
        state = api.user_unfollow(acct)

        if state == api.STATE_NOTFOUND:
            return render_template("index.html", message="Could not find an account with that name")
        elif state == api.STATE_UNFOLLOWED:
            return render_template("index.html", message="We've unfollowed that account and won't follow it again")
        elif state == api.STATE_ADDED_NOFOLLOW:
            return render_template("index.html", message="We weren't following that account, but won't in the future")
        elif state == api.STATE_ALREADY_UNFOLLOWED:
            return render_template("index.html", message="We already stopped following that account")
        else:
            print(state)
            return render_template("index.html", message="We did something and you should be unfollwed.")

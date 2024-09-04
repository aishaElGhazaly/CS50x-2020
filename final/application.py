import os
import requests
import urllib.parse
import json
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import base64
import datetime

from helpers import login_required, apology

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

class SpotifyAPI:
    access_token = None
    expires_in = None
    expires = None

    client_id = client_id
    client_secret = client_secret

    token_url = "https://accounts.spotify.com/api/token"
    method = "POST"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        self.clinet_id = client_id
        self.client_secret = client_secret

    def client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            raise Exception("client_id and client_secret must be set.")

        client_creds = f"{client_id}:{client_secret}"
        cc64 = base64.b64encode(client_creds.encode())
        return cc64.decode()

    def token_header(self):
        cc64 = self.client_credentials()
        return {
            "Authorization": f"Basic {cc64}"
        }

    def token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def auth(self):
        token_url = self.token_url
        token_data = self.token_data()
        token_header = self.token_header()

        request = requests.post(token_url, data=token_data, headers=token_header)
        resp = request.json()

        if request.status_code not in range(200, 299):
            raise Exception("Authentication Failed.")

        self.access_token = resp['access_token']
        self.expires_in = resp['expires_in']
        now = datetime.datetime.now()
        self.expires = now + datetime.timedelta(seconds=self.expires_in)

    def get_access_token(self):
        token = self.access_token
        expires = self.expires
        now = datetime.datetime.now()

        if expires < now:
            self.auth()
            return self.get_access_token()
        else:
            return token

    def resource_header(self):
        access_token = self.get_access_token()

        header = {
            "Authorization": f"Bearer {access_token}"
        }

        return header

    def get_resource(self, _id, r_type):
        endpoint = f"https://api.spotify.com/v1/{r_type}/{_id}"
        header = self.resource_header()

        request = requests.get(endpoint, headers=header)

        if request.status_code in range(200, 299):
            return request.json()
        else:
            print("Response status code: " + str(request.status_code))
            return {}

    def search(self, query, q_type, **kwargs):
        header = self.resource_header()
        endpoint = f"https://api.spotify.com/v1/search?q={query}&type={q_type}&limit=32"
        response = requests.get(endpoint, headers=header)

        search = response.json()

        if response.status_code in range(200, 299):
            return search
        else:
            print("Response status code: " + str(response.status_code))
            return {}

    def get_album(self, _id):
        return self.get_resource(_id, "albums")

    def get_artist(self, _id):
        return self.get_resource(_id, "artists")

    def get_track(self, _id):
        return self.get_resource(_id, "tracks")

    def new_releases(self, **kwargs):
        header = self.resource_header()
        endpoint = "https://api.spotify.com/v1/browse/new-releases?limit=40"

        for key, value in kwargs.items():
            if key == "country":
                endpoint = f"https://api.spotify.com/v1/browse/new-releases?country={value}&limit=40"

        response = requests.get(endpoint, headers=header)

        new_releases = response.json()

        return new_releases

spotify = SpotifyAPI(client_id, client_secret)
spotify.auth()

countries = sorted(["DZ", "EG", "MA", "ZA", "TN", "BH", "HK",
        "IN", "ID", "IL", "JP", "JO", "KW", "LB", "MY", "OM",
        "PS", "PH", "QA", "SA", "SG", "TW", "TH", "AE", "VN",
        "AD", "AT", "BE", "BG", "CY", "CZ", "DK", "EE", "FI",
        "FR", "DE", "GR", "HU", "IS", "IE", "IT", "LV", "LI",
        "LT", "LU", "MT", "MC", "NL", "NO", "PL", "PT", "RO",
        "SK", "ES", "SE", "CH", "TR", "GB", "RU", "BY", "KZ",
        "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI",
        "XK", "CA", "CR", "DO", "SV", "GT", "HN", "MX", "NI",
        "PA", "US", "AR", "BO", "BR", "CL", "CO", "EC", "PY",
        "PE", "UY", "AU", "NZ"])


db = SQL("sqlite:///info.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect("/new-releases")

@app.route("/new-releases", methods=["GET", "POST"])
def new_releases():
    if request.method == "GET":
        releases = spotify.new_releases()
        return render_template("new-releases.html", releases=releases, countries=countries)
    else:
        region = request.form.get("sym")
        if region == None:
            releases = spotify.new_releases()
        else:
            releases = spotify.new_releases(country=region)

        return render_template("new-releases.html", releases=releases, countries=countries)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        query = request.form.get("query")
        if not query:
            return apology("You Must Search For Something.")

        q_type = (request.form.get("q_type")).lower()
        if not q_type:
            return apology("You Must Specify The Type.")

        results = spotify.search(query, q_type)

        return render_template("search_res.html", results=results, query=query, q_type=q_type)

@app.route("/register", methods=["GET", "POST"])
def register():
    #Register user
    if request.method == "GET":
        return render_template("register.html")
    else:
        #Username and Error checking
        username = request.form.get("username")
        if not username:
            return apology("Must insert username.")

        usernames = db.execute("SELECT username FROM users")

        for check in range(len(usernames)):
            if username == usernames[check]['username']:
                return apology("Username already taken.")

        #Password and Error checking
        password = request.form.get("password")
        if not password:
            return apology("Must insert password.")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("Passwords must match.")

        if len(password) < 8:
            return apology("Password must be 8 or more characters.")

        if password.isalpha() == True or password.isdigit() == True:
            return apology("Password must contain alphabetical characters and numbers.")

        #hash and confirmation
        password_hash = generate_password_hash(password)

        #Save data
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=password_hash)
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print(db.execute("SELECT * FROM users"))

        # Redirect user to home page
        return redirect("/new-releases")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/new-releases")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        records = db.execute("SELECT * FROM fav_records WHERE user_id=:user_id", user_id=session['user_id'])
        artists = db.execute("SELECT * FROM fav_artists WHERE user_id=:user_id", user_id=session['user_id'])

        if (len(records) == 0 and len(artists) == 0):
            return render_template("profileZ.html")
        else:
            return render_template("profileT.html", records=records, artists=artists)
    else:
        favA = request.form.get("favA")
        if (favA):
            searchA = spotify.search(favA, "artist")
            artist = [searchA['artists']['items'][0]['name'], searchA['artists']['items'][0]['id'], searchA['artists']['items'][0]['images'][0]['url']]

            db.execute("INSERT INTO fav_artists (user_id, name, id, image) VALUES (:user_id, :name, :id, :image)",
                           user_id=session['user_id'], name=artist[0], id=artist[1], image=artist[2])

        title = request.form.get("title")
        artist = request.form.get("artist")

        search = spotify.search(title + " " + artist, "album")
        result = [search['albums']['items'][0]['name'], search['albums']['items'][0]['artists'][0]['name'], search['albums']['items'][0]['id'], search['albums']['items'][0]['images'][1]['url'], search['albums']['items'][0]['images'][2]['url'], search['albums']['items'][0]['external_urls']['spotify']]

        db.execute("INSERT INTO fav_records (user_id, record, artist, record_id, artwork, icon, url) VALUES (:user_id, :record, :record_id, :artist, :artwork, :icon, :url)",
                       user_id=session['user_id'], record=result[0], artist=result[2], record_id=result[1], artwork=result[3], icon=result[4], url=result[5])

        records = db.execute("SELECT * FROM fav_records WHERE user_id=:user_id", user_id=session['user_id'])
        artists = db.execute("SELECT * FROM fav_artists WHERE user_id=:user_id", user_id=session['user_id'])

        return render_template("profileT.html", records=records, artists=artists)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "GET":
        table = db.execute("SELECT * FROM fav_records WHERE user_id=:user_id", user_id=session['user_id'])
        return render_template("edit.html", table=table)
    else:
        favA = request.form.get("favA")
        if (favA):
            searchA = spotify.search(favA, "artist")
            artist = [searchA['artists']['items'][0]['name'], searchA['artists']['items'][0]['id'], searchA['artists']['items'][0]['images'][0]['url']]
            db.execute("DELETE FROM fav_artists WHERE user_id=:user_id", user_id=session['user_id'])
            db.execute("INSERT INTO fav_artists (user_id, name, id, image) VALUES (:user_id, :name, :id, :image)",
                           user_id=session['user_id'], name=artist[0], id=artist[1], image=artist[2])
            return redirect("/profile")

        rec_id = request.form.get("id")
        if rec_id:
            db.execute("DELETE FROM fav_records WHERE record_id=:record_id", record_id=rec_id)

        table = db.execute("SELECT * FROM fav_records WHERE user_id=:user_id", user_id=session['user_id'])

        return render_template("edit.html", table=table)
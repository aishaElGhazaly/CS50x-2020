import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    """Relative data"""
    portfolio = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price, SUM(total) AS total FROM transactions WHERE user_id = :user_id GROUP BY user_id, symbol", user_id=session['user_id'])

    """User's cash"""
    monz = db.execute("SELECT cash FROM users WHERE id = :id",
                      id=session['user_id'])
    cash = monz[0]['cash']

    """Calculating the total"""
    total = cash
    for subtotal in range(len(portfolio)):
        total += portfolio[subtotal]['total']

    return render_template("index.html", portfolio=portfolio, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        """Retrieving data from form"""
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)

        """Error checking"""
        if not symbol:
            return apology("Must provide stock sym.")

        if not shares:
            return apology("Must provide number of stocks.")

        if symbol.isalpha() != True:
            return apology("Type a valid stock symbol.")

        if shares.isdigit() != True:
            return apology("Type a valid No. of shares.")

        if quote == None:
            return apology("Stock doesn't exist.")

        if int(shares) < 0:
            return apology("Can't buy negative shares.")

        if int(shares) == 0:
            return apology("No shares. No problem.")

        stock = quote['price'] * float(shares)

        """User's cash"""
        monz = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session['user_id'])

        cash = monz[0]['cash']

        """Buy stock"""
        if cash < stock:
            return apology("Non sufficient funds to complete transaction.")
        else:
            cash -= stock
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session['user_id'])
            db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, total, time) VALUES (:user_id, :symbol, :name, :shares, :price, :total, :time)",
                       user_id=session['user_id'], symbol=quote['symbol'], name=quote['name'], shares=shares, price=quote['price'], total=stock, time=datetime.datetime.now())

            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    portfolio = db.execute("SELECT * FROM transactions WHERE user_id = :user_id ORDER BY time DESC", user_id=session['user_id'])

    return render_template("history.html", portfolio=portfolio)


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

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote == None:
            return apology("Stock doesn't exist.")

        return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        """Username and Error checking"""
        username = request.form.get("username")
        if not username:
            return apology("Must insert username.")

        usernames = db.execute("SELECT username FROM users")

        for check in range(len(usernames)):
            if username == usernames[check]['username']:
                return apology("Username already taken.")

        """Password and Error checking"""
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

        """hash and confirmation"""
        password_hash = generate_password_hash(password)

        """Save data"""
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=password_hash)

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        """only stocks the user owns"""
        stocks = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id=:user_id", user_id=session["user_id"])

        symbols = []
        for symb in range(len(stocks)):
            symbols.append(stocks[symb]['symbol'])

        return render_template("sell.html", symbols=symbols)
    else:
        """Retrieving data from form"""
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)

        """No. of shares of stock"""
        qty = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id=:user_id AND symbol=:symbol",
                         user_id=session["user_id"], symbol=symbol)
        NOS = qty[0]['shares']

        """Error checking"""
        if not shares:
            return apology("Must provide a number of stocks")

        if shares.isdigit() != True:
            return apology("Type a valid No. of shares.")

        if int(shares) < 0:
            return apology("Can't sell negative shares.")

        if int(shares) == 0:
            return apology("No shares. No problem.")

        if int(shares) > NOS:
            return apology("Can't sell what you don't own.")

        stock = quote['price'] * float(shares)

        """User's cash"""
        monz = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session['user_id'])

        cash = monz[0]['cash']
        cash += stock

        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session['user_id'])

        """Save data"""
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, total, time) VALUES (:user_id, :symbol, :name, :shares, :price, :total, :time)",
                   user_id=session['user_id'], symbol=quote['symbol'], name=quote['name'], shares=(0 - int(shares)), price=quote['price'], total=(0 - int(stock)), time=datetime.datetime.now())

        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """add cash to account"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        session["cash"] = request.form.get("amount")

        if session["cash"].isdigit() != True:
            return apology("Type a valid amount.")
        return redirect("/confirm")


@app.route("/confirm", methods=["GET", "POST"])
@login_required
def confirm():
    """Password confirmation"""
    if request.method == "GET":
        return render_template("confirm.html")
    else:
        """Password and Error checking"""
        password = request.form.get("password")
        if not password:
            return apology("Must insert password.")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("Passwords must match.")

        """Password hash"""
        password_hash = generate_password_hash(password)

        hashval = db.execute("SELECT hash FROM users WHERE id=:id", id=session["user_id"])

        """User's cash"""
        monz = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session['user_id'])

        cash = monz[0]['cash']
        cash += float(session["cash"])

        """Match Check"""
        if check_password_hash(hashval[0]["hash"], password_hash):
            return apology("Password incorrect.")
        else:
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session["user_id"])
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

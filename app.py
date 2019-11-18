from flask import Flask, render_template, redirect, request, session
from infrastructure import south
from shortestpath import Dijkstra
import csv
import math
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

password="titech"
usn="admin"
app = Flask("__name__")
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
Session(app)
def reading(bs, cons):
  #print(bs)
  #print(cons)
  x1 = []
  y1 = []
  x2 = []
  y2 = []
  for con in cons:
    if not con:
      continue
    for b in bs:
      if not b:
        continue
      if b[0] == con[0]:
        x1.append(b[1])
        y1.append(b[2])
      elif b[0] == con[1]:
        x2.append(b[1])
        y2.append(b[2])
  return [x1,x2,y1,y2]

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods = ["GET","POST"])
def index():
  if request.method == "POST":
    source = request.form.get("from").lower().replace(" ","_")
    dest = request.form.get("to").lower().replace(" ","_")
    ds = Dijkstra(source, dest, south)
    distance = ds["dist"]
    paths = ds["path"]
    ways = []
    file3= open("building.csv","r")
    reader2 = csv.reader(file3)
    bs = list(reader2)
    for path in paths:
      for b in bs:
        if b[0] == path:
          ways.append([path,b[1],b[2]])
    connections = [[paths[it], paths[it+1]] for it in range(len(paths)-1)]
    x1,x2,y1,y2 = reading(ways,connections)
    file3.close()
    return render_template("index.html",x1 = x1, x2=x2, y1=y1, y2=y2, dist=distance*0.5)

  else:
    return render_template("try.html",vals = [])

@app.route("/login",methods=["GET","POST"])	
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
        if request.form.get("password") !=password or request.form.get("username") != usn:
          return apology("username or password is not correct",403)

        # Remember which user has logged in
        session["user_id"] = "admin"
        
        # Redirect user to home page
        
        return redirect("/administrator")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
		
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/administrator")
@app.route("/administrator",methods = ["GET","POST"])
@login_required
def backend():
  if request.method == "GET":
    return render_template("backend.html", success=False)
  else:
    file= open("connection.csv","r")
    reader1 = csv.reader(file)
    cons = list(reader1)
    file3= open("building.csv","r")
    reader2 = csv.reader(file3)
    bs = list(reader2)
    x1,x2,y1,y2 = reading(bs,cons)
    file1 = open("building.csv","a")
    file2 = open("connection.csv","a")
    writer1 = csv.writer(file1,lineterminator="\n")
    writer2 = csv.writer(file2,lineterminator="\n")
    bName = request.form.get("bName")
    posX = request.form.get("posX")
    posY = request.form.get("posY")
    b1 = request.form.get("first")
    b2 = request.form.get("second")
    #dist = request.form.get("distance")
    dist = 0
    for b in bs:
      if not b:
        continue
      for c in bs:
        if not c:
          continue
        if b[0] == b1 and c[0] == b2:
          dist = math.sqrt((float(b[1])-float(c[1]))**2 + (float(b[2])-float(c[2]))**2)
    dist = int(100*dist)
    dist = float(dist/100)
    if bName and posX and posY:
      writer1.writerow((bName, posX, posY))
    elif b1 and b2 and dist:
      writer2.writerow((b1,b2,dist))
    file1.close()
    file2.close()
    file3.close()
    file.close()
    return render_template("backend.html", success=True, x1 = x1, x2 = x2, y1 = y1, y2=y2)

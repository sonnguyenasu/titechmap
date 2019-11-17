from flask import Flask, render_template, redirect, request
from infrastructure import south
from shortestpath import Dijkstra
import csv
app = Flask("__name__")

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

@app.route("/", methods = ["GET","POST"])
def index():
  if request.method == "POST":
    source = request.form.get("from")
    dest = request.form.get("to")
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
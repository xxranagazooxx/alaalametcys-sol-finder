#!flask/bin/python
from flask import Flask, jsonify
from models import get_solution

app = Flask(__name__)
SECMAP = {
    # translate uri to db namespace
    "CP": "C/P",
    "SB": "S/B",
    "BB" : "B/B",
    "CARS" : "CARS"}

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/api/v1.0/<string:mod>/<string:sec>/<int:num>", methods=["GET"])
#XXX: rename
def getsol(mod, sec, num):

    #TODO: add auth cookie/exploit prevention

    # convert
    rsec = SECMAP.get(sec.upper())
    print "You selected %s | %s | %d \n" % (mod, rsec, num)

    return jsonify(get_solution(mod, rsec, num))

def vote(solid):
    #TODO: validate oauth
    pass

if __name__ == '__main__':
    app.run(debug=True, port=31415)


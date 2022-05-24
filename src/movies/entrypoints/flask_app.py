from flask import Flask, render_template, request
from movies import models
from movie_fetcher import getRecs

app = Flask(__name__)
models.start_mappers()

@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello World!", 200

""" Stuff I added """
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        director = models.Director()
        builder = models.ConcreteBuilder()
        director.builder = builder
        director.buildUser(request.form.get("Email"), request.form.get("Password"), request.form.getlist("interest"))
        return render_template('data.html', user_info = builder.user)

@app.route('/descendingRecs/<preference_key>')
def descendingRecs(preference_key):
    movieList = getRecs(preference_key)
    context = models.Context(models.ConcreteStrategyDescending())
    sortedList = context.sortAccordingToStrategy(movieList)
    return render_template('movies.html', movielist = sortedList)

@app.route('/ascendingRecs/<preference_key>')
def ascendingRecs(preference_key):
    movieList = getRecs(preference_key)
    context = models.Context(models.ConcreteStrategyAscending())
    sortedList = context.sortAccordingToStrategy(movieList)
    return render_template('movies.html', movielist = sortedList)
""" END Stuff I added """
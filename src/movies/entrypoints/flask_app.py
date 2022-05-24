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
        form_data = request.form
        interestList = request.form.getlist("interest")

        preference_key = (int(interestList[0]) + int(interestList[1]) + int(interestList[2])) % 4 + 1

        return render_template('data.html',form_data = form_data, pref_key = preference_key)

def compareRatings(movie):
    return movie.get("rating")

@app.route('/descendingRecs/<preference_key>')
def descendingRecs(preference_key):
    movieList = getRecs(preference_key)
    movieList.sort(key=compareRatings, reverse=True)
    return render_template('movies.html', movielist = movieList)

@app.route('/ascendingRecs/<preference_key>')
def ascendingRecs(preference_key):
    movieList = getRecs(preference_key)
    movieList.sort(key=compareRatings)
    return render_template('movies.html', movielist = movieList)

@app.route("/proy", methods=["GET"])
def project_init():
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """
    director = models.Director()
    builder = models.ConcreteBuilder1()
    director.builder = builder

    director.build_full_featured_user()
    builder.user.list_parts()
    return ("")
""" END Stuff I added """
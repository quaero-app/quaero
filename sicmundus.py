from flask import Flask, render_template, request, Response, session
from finder import*



app = Flask(__name__)

data = process_data("data/Quaero_data.csv")

@app.route('/')
def index():
    return render_template('index.html', step= "query")

@app.route('/query', methods=['GET'])

def query():
    queryfield = request.args['query']
    queryfield = queryfield.lower()
    research = do_search(data, queryfield, None)
    if len(research) > 0:
        dataready, min, max = geojsonize(research)
        return render_template("index.html", output=dataready, min = min, max = max, step="results", query= queryfield, json=research)
    else:
        return render_template("index.html", output=None, query= queryfield, step="results")


@app.route('/documentation')
def documentation():
    return render_template("index.html", step="documentation")


@app.route('/about')
def about():
    return render_template("index.html", step="about")


if __name__ == '__main__':
  app.run (host='0.0.0.0')


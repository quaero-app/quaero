from flask import Flask, render_template, request
from finder import*



app = Flask(__name__)

data = process_data("data/data.csv")


@app.route('/')
def index():
    return render_template('index.html', step= "query")

@app.route('/', methods=['POST'])

def inveniet():
    queryfield = request.form['query']
    queryfield = queryfield.lower()
    research = do_search(data, queryfield, None)
    if len(research) > 0:
        dataready, min, max = geojsonize(research)
        return render_template("index.html", output=dataready, min = min, max = max, step="results")
    else:
        return render_template("index.html", output=None, step="results")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == '__main__':
  app.run (host='0.0.0.0')


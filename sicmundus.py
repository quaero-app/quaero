from flask import Flask, render_template, request
from finder import*



app = Flask(__name__)

data = process_data("data.csv")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def inveniet():
    queryfield = request.form['query']
    research = do_search(data, queryfield, None)
    if len(research) > 0:
        dataready = geojsonize(research)
        return render_template("results.html", output=json.dumps(dataready))
    else:
        return render_template("results.html", output=None)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == '__main__':
  app.run (host='0.0.0.0')


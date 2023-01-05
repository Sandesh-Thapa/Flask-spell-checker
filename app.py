from flask import Flask, render_template, request
from spell_checker import main

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
    results = {}
    if request.method == 'POST':
        website = request.form['website']
        results = main(website)
        results['website'] = website
    return render_template('home.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
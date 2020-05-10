from flask import Flask, request, jsonify, render_template
import scraping_server

app = Flask(__name__)


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/sentiment', methods=['POST'])
def rpsaServe():
    if request.method == 'POST':
        # input =
        # get search words from front page
        results = scraping_server.stream(input)
        return jsonify(results)


if __name__ == '__main__':
    app.run()

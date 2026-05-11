import os

from flask import Flask, send_file, request, jsonify
from scraper import scrape_afa_search_results

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/search")
def search():
    query = request.args.get("query", "農機補助")
    results = scrape_afa_search_results(query)
    return jsonify(results)

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()

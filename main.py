
import os
from flask import Flask, send_file, request, jsonify
# Import the new, focused scraper function
from scraper import scrape_afa_latest_news

app = Flask(__name__)

@app.route("/")
def index():
    print("Serving index.html")
    return send_file('src/index.html')

@app.route("/search")
def search():
    """
    This endpoint now always fetches the latest news, ignoring any search query.
    This aligns with the new strategy to focus on the "Latest News" page.
    """
    # We get the query here just to log it, but we won't use it for the scraping.
    query = request.args.get("keyword", "").strip()
    
    print("="*30)
    # Log the received query, even though we are not using it.
    print(f"Received search request. Query: '{query}' (Note: Query is ignored)")
    
    # Always dispatch to the new, focused scraper
    print("--> Dispatching to scrape_afa_latest_news.")
    results = scrape_afa_latest_news()
    print(f"<-- Latest news fetch completed. Found {len(results)} results.")
    
    print("Request finished. Sending JSON response to client.")
    print("="*30)
    return jsonify(results)

def main():
    print("Starting Flask server with auto-reloader...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

if __name__ == "__main__":
    main()

'''
This file contains the web scraping logic for the農機補助 application.
'''
import requests
from bs4 import BeautifulSoup


def scrape_afa_search_results(query):
    '''
    Scrapes the search results page of the Agriculture and Food Agency of Taiwan (農糧署) for a given query.

    Args:
        query: The search query string.

    Returns:
        A list of dictionaries, where each dictionary represents a search result and contains the title and URL.
    '''
    try:
        search_url = "https://www.afa.gov.tw/search"
        session = requests.Session()

        # Get the search page to extract the CSRF token
        response = session.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
        csrf_token_element = soup.find("input", {"name": "_csrf"})
        if not csrf_token_element:
            print("Could not find CSRF token.")
            return []
        csrf_token = csrf_token_element.get("value")

        # Prepare the POST data
        payload = {
            "_csrf": csrf_token,
            "search_intron": "Y",
            "search_item": query,
            "search_item_topic": "OR",
            "search_roc_s": "",
            "search_roc_e": "",
            "search_date_s": "",
            "search_date_e": "",
            "search_class": "",
            "search_node": "",
            "search_page_size": "10",
        }

        # Perform the search using a POST request
        response = session.post(search_url, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "lxml")
        results = []

        # Find all the search result items
        for item in soup.select(".list_item .card_intron a"):
            title = item.get_text(strip=True)
            link = item.get("href")
            if not link.startswith("http"):
              link = "https://www.afa.gov.tw" + link
            results.append({"title": title, "link": link})

        return results

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

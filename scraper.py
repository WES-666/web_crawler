
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Base URL for the AFA website
BASE_URL = "https://www.afa.gov.tw/cht/"

def scrape_afa_latest_news():
    """
    Scrapes the "Latest News" (最新消息) page of the AFA website.
    This is a focused scraper that uses requests and BeautifulSoup.
    """
    print("  [Scraper] Starting: Scrape Latest News")
    latest_news_url = "https://www.afa.gov.tw/cht/index.php?code=list&ids=379"
    results = []

    try:
        print(f"  [Scraper] Fetching URL: {latest_news_url}")
        response = requests.get(latest_news_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("  [Scraper] URL fetched successfully.")

        print("  [Scraper] Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main list container, the ID is now 'agricultural-news'
        list_container = soup.find('div', id='agricultural-news')
        if not list_container:
            print("  [Scraper] ERROR: Could not find the main news list container 'div#agricultural-news'.")
            return []

        # Find all news items, which are 'a' tags with class 'agricultural-news'
        news_items = list_container.find_all('a', class_='agricultural-news')
        print(f"  [Scraper] Found {len(news_items)} potential news items in the list.")

        for item in news_items:
            link = item.get('href')
            if not link:
                continue

            title_tag = item.find('h3')
            title = title_tag.get_text(strip=True) if title_tag else 'No Title'

            date = 'No date'
            date_ribbon = item.find('div', class_='agricultural-news-ribbon')
            if date_ribbon:
                date_span = date_ribbon.find('span')
                if date_span and date_span.contents:
                    # The date is the first text node within the span
                    date = date_span.contents[0].strip()
            
            absolute_link = urljoin(BASE_URL, link)
            results.append({"title": title, "link": absolute_link, "date": date})
        
        print(f"  [Scraper] Finished: Successfully scraped {len(results)} latest news results.")
        return results

    except requests.RequestException as e:
        print(f"  [Scraper] ERROR: An error occurred while fetching the page: {e}")
        return []
    except Exception as e:
        print(f"  [Scraper] ERROR: An error occurred while parsing the page: {e}")
        return []

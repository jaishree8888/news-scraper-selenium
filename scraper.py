import requests
from datetime import datetime, timedelta

def fetch_articles(topic, api_key, date=None):

    url = f"https://newsapi.org/v2/everything?q={topic}"

   

    # Date filter
    if date:
        past_date = datetime.now() - timedelta(days=int(date))
        url += f"&from={past_date.strftime('%Y-%m-%d')}"

    url += f"&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get("articles", [])
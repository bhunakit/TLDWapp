import requests
import json
import os

def fetch_complementary_images(youtube_url, num_images):
    # Replace with your Google Custom Search Engine API key and custom search engine ID
    api_key = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
    cx = os.environ.get('GOOGLE_CUSTOM_SEARCH_CX')

    if not api_key or not cx:
        return []

    api_endpoint = 'https://www.googleapis.com/customsearch/v1'

    # Define the query parameters
    params = {
    'key': api_key,
    'cx': cx,
    'q': youtube_url,
    'searchType': 'image',
    'num': num_images,
    }

    response = requests.get(api_endpoint, params=params)
    response.raise_for_status()

    data = json.loads(response.content)

    image_urls = [item['link'] for item in data.get('items', [])]

    return image_urls

def save_image(image_url, filename):
    response = requests.get(image_url)
    with open(f"/tmp/{filename}", "wb") as f:
        f.write(response.content)




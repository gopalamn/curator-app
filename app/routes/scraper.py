from flask import request, jsonify, abort, Response, Blueprint
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

scraper = Blueprint('scraper', __name__)

@scraper.route('/api/link_preview/', methods=['GET'])
def get_link_preview():
    
    url = request.args.get('url')
    if not url:
        abort(400)

    return jsonify(get_link_metadata(url))

def get_link_metadata(url):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'})
    response = requests.get(url, HEADERS)
    print(response.status_code)

    hostname = urlparse(url).hostname
    hostname = hostname.replace("www.", "")

    title = None
    img = None
    description = None
    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, features="html.parser")

        title = get_title_data(soup)
        description = get_description_data(soup)
        img = get_img_data(soup)
    
    return {
        'hostname': hostname,
        'title': title,
        'img': img,
        'description': description,
        'link': url
    }

def get_title_data(soup):
    title = soup.find('meta', property='og:title')
    if (title and len(title['content']) > 0):
        return title['content']
    
    title = soup.find('meta', {'name': 'twitter:title'})
    if (title and len(title['content']) > 0):
        return title['content']

    title = soup.find('title')
    if (title and len(title.string) > 0):
        return title.string
    
    title = soup.find('meta', {'name': 'title'})
    if (title and len(title['content']) > 0):
        return title['content']

def get_description_data(soup):
    description = soup.find('meta', property='og:description')
    if (description and len(description['content']) > 0):
        return description['content']
    
    description = soup.find('meta', {'name': 'twitter:description'})
    if (description and len(description['content']) > 0):
        return description['content']

    description = soup.find('meta', {"name": "description"})
    if (description and len(description['content']) > 0):
        return description['content']

def get_img_data(soup):

    img = soup.find('meta', property='og:image')
    if (img and len(img['content']) > 0):
        return img['content']
    
    img = soup.find('link', {"rel": "image_src"})
    if (img and len(img['href']) > 0):
        return img['href']

    img = soup.find('meta', {'name': 'og:twitter'})
    if (img and len(img['content']) > 0):
        return img['content']
    
    
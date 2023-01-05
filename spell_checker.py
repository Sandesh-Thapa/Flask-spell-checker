import requests
from bs4 import BeautifulSoup

URL = "https://api.textgears.com/spelling/?key=<Your Key Here>&language=en-US&text="

def scrapePage(page):
    """
    Scrape the page to find its 'h1' and 'h2' tags

    :param page: request body
    :return: url and response code
    """
    soup = BeautifulSoup(page.text, features="html.parser")
    h1 = soup.find_all('h1')
    h2 = soup.find_all('h2')
    return h1, h2

def checkSpelling(text):
    response = requests.get(URL+text, timeout=60)
    return response.json()

def main(website):
    results = {'h1': [], 'h2': []}
    try:
        page = requests.get(website, timeout=60)
        if page.status_code == 404:
            results["error"] = "404 Site not found!"
        elif page.status_code == 403:
            results["error"] = "403 Forbidden!"
        else:
            h1tags, h2tags = scrapePage(page)
            for h1 in h1tags:
                h1 = checkSpelling(h1.text)
                if len(h1['response']['errors']) > 0:
                    results['h1'].append(h1['response']['errors'])
                
            for h2 in h2tags:
                h2 = checkSpelling(h2.text)
                if len(h2['response']['errors']) > 0:
                    results['h2'].append(h1['response']['errors'])
    except:
        results["error"] = "Something went wrong! Try Again!"

    return results
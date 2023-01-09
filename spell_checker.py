import requests
from bs4 import BeautifulSoup

URL = "https://api.textgears.com/spelling/?key=<Your Key Here>&language=en-US&text="

def scrapePage(page):
    """
    Scrape the page to find its 'h1' and 'h2' tags

    :param page: request body
    :return: h1 tags and h2 tags
    """
    soup = BeautifulSoup(page.text, features="html.parser")
    h1 = soup.find_all('h1')
    h2 = soup.find_all('h2')
    return h1, h2

def checkSpelling(text):
    response = requests.get(URL+text, headers={'User-Agent': ''}, timeout=60)
    return response.json()

def main(website):
    results = {'h1': [], 'h2': []}

    page = requests.get(website, headers={'User-Agent': ''}, timeout=60)
    print(page.status_code)
    if page.status_code == 404:
        results["error"] = "404 Site not found!"
    elif page.status_code == 403:
        results["error"] = "403 Forbidden!"
    elif page.status_code == 200:
        h1tags, h2tags = scrapePage(page)
        for h1 in h1tags:
            try:
                h1 = checkSpelling(h1.text)
                if len(h1['response']['errors']) > 0:
                    results['h1'].append(h1['response']['errors'])
            except:
                continue
            
        for h2 in h2tags:
            try:
                h2 = checkSpelling(h2.text)
                if len(h2['response']['errors']) > 0:
                    results['h2'].append(h2['response']['errors'])
            except:
                continue
    else:
        results["error"] = "Something went wrong! Try Again!"

    return results

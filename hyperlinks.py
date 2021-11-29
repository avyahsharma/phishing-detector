from bs4 import BeautifulSoup
import requests
import pandas as pd

data = pd.read_csv('phishing_urls.csv')
frames = []

def getLinks(url):
    ego = url
    if ((ego.startswith("http") == False)):
        ego = "https://" + ego

    reqs = requests.get(ego, verify=False)
    soup = BeautifulSoup(reqs.text.encode('utf8').decode('ascii', 'ignore'), 'html.parser')

    links = []
    for link in soup.find_all('a'):
        links.append([ego, str(link.get('href'))])

    links = pd.DataFrame(links, columns=["from", "to"])
    frames.append(links)

def main(data, frames):
    data["URL"].apply(lambda source: getLinks(source))
    keys = data["URL"].tolist()
    df = pd.concat(frames, keys=keys)
    df.to_csv('hyperlinks.csv')

main(data, frames)
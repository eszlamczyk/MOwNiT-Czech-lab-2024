from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
from queue import PriorityQueue
import re
import multiprocessing
import json
import math


def getStopWords(path):
    List = []
    with open(path, "r") as file:
        for line in file:
            List.append(line.strip())
    return List


# globals
stopWords = getStopWords("Databases/stopwords.txt")


def stopWordsRemoval(x):
    global stopWords
    return not x in stopWords


def TextToBOW(text: str) -> dict:
    def remove_unicode(text):
        return re.sub(r'[^\x00-\x7F]', ' ', text)

    clean_text = remove_unicode(text.lower())
    words = re.split(
        r'[\/;\'\n:().,\s\[\]\-"`?@! ]+', clean_text)
    FilteredText = list(filter(stopWordsRemoval, words))
    BOW = {}
    for word in FilteredText:
        BOW[word] = 1 + BOW.get(word, 0)

    return BOW


def UrlToWorldList(url):
    try:
        page = urlopen(url)
    except:
        return
    html_bytes = page.read()
    try:
        html = html_bytes.decode("utf-8")
    except:
        return
    soup = BeautifulSoup(html, "lxml")
    text = soup.getText()

    return TextToBOW(text)


def save_dict_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)


def load_dict_from_file(filename) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)


def filter_none_values(dictionary: dict):
    return {k: v for k, v in dictionary.items() if v is not None}


def urlFromWebsite(InitialURL: str, amount: int) -> dict:
    print("Finding in: ", InitialURL)
    URLs = {}
    Q = PriorityQueue()
    Q.put((1, InitialURL))
    URLs[InitialURL] = True
    while len(URLs) <= amount and (not Q.empty()):

        print(len(URLs))
        deph, url = Q.get()
        if deph > 3:
            continue
        try:
            page = urlopen(url)
        except:
            # print(url)
            continue

        html_bytes = page.read()
        try:
            html = html_bytes.decode("utf-8")
        except:
            continue
        soup = BeautifulSoup(html, "lxml")
        for link in soup.findAll("a"):
            parsedLink = link.get('href')
            if parsedLink is None:
                continue

            # links sometimes start with for example "/news" or "//bbc.com/news" instead of "https://bbc.com/news"
            # thats why i want to look into both cases, this way it is the fastest

            if InitialURL in parsedLink:
                pass
            elif parsedLink.startswith("//") and parsedLink != "//":
                parsedLink = "https:" + parsedLink
            elif parsedLink.startswith("/") and parsedLink != "/":
                parsedLink = InitialURL + parsedLink
            else:
                continue

            if not URLs.get(parsedLink, False):
                Q.put((deph+1, parsedLink))
                URLs[parsedLink] = True

    print("Parsing: ", InitialURL)
    print("Warning it might take a lot of time (20mins +)")

    for url in list(URLs.keys()):
        URLs[url] = UrlToWorldList(url)

    URLs = filter_none_values(URLs)

    print("Finished looking for URLs in: ",
          InitialURL, ". Found ", len(URLs), " URLs")
    return URLs


def process_url(URL, amount, result_dict):
    result_dict.update(urlFromWebsite(URL, amount))


def getUrlList():
    InitialURLs = [("https://www.bbc.com", 1000),
                   ("https://www.nbcnews.com", 1000),
                   ("https://edition.cnn.com", 1000),
                   ("https://www.foxnews.com", 2000),
                   ("https://people.com", 1500),
                   ("https://www.abc.net.au", 500),
                   ("https://www.news18.com", 2000),
                   ("https://eu.usatoday.com", 700),
                   ("https://news.sky.com", 1000)]

    manager = multiprocessing.Manager()
    URLs = manager.dict()
    jobs = []

    for URL, amount in InitialURLs:
        p = multiprocessing.Process(
            target=process_url, args=(URL, amount, URLs))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    return dict(URLs)


def createBOWs():
    global globalBow, wordIndex
    print("================GettingBOWs==============")

    # Get URLs using multiprocessing
    URLs = getUrlList()
    URLIndexes = {}
    URLIndex = 0
    globalBOW = {}
    for url in list(URLs.keys()):
        URLIndexes[url] = URLIndex
        URLIndex += 1
        globalBOW.update(URLs[url])

    BOWIndex = 0
    for word in list(globalBOW.keys()):
        globalBOW[word] = BOWIndex
        BOWIndex += 1

    save_dict_to_file(URLs, "Databases/URLs.json")
    save_dict_to_file(globalBOW, "Databases/globalBow.json")
    print("=======================DONE=======================")


def calculateIDFs() -> dict:
    print("=====Calculationg Inverse document frequencies====")
    Occurances = {}
    URLs = load_dict_from_file("Databases/URLs.json")
    for _, urlDict in URLs.items():
        for word in list(urlDict.keys()):
            Occurances[word] = 1 + Occurances.get(word, 0)

    N = len(URLs)
    IDF = {}

    for key in Occurances:
        IDF[key] = math.log10(N/Occurances[key])

    save_dict_to_file(IDF, "Databases/IDFs.json")
    print("=======================DONE=======================")

    return IDF


def IndexUrls():
    print("=========INDEXING URLS=========")
    URLs = load_dict_from_file("Databases/URLs.json")
    URLIndexes = {}
    IndexedURLs = {}
    currIndex = 0
    for URL, _ in URLs.items():
        URLIndexes[URL] = currIndex
        IndexedURLs[currIndex] = URL
        currIndex += 1

    save_dict_to_file(IndexedURLs, "Databases/IndexedURLs.json")
    save_dict_to_file(URLIndexes, "Databases/URLIndexes.json")
    print("=======================DONE=======================")

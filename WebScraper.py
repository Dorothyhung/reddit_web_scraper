from bs4 import BeautifulSoup
import requests
from collections import Counter
import nltk
#nltk.download('all')
from nltk import FreqDist
from textblob import TextBlob
import numpy as np
import pandas as pd
import multiprocessing
from multiprocessing import Pool, cpu_count
import sys
import time

def fetch_posts(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    print('Creating requests ...')
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    posts = soup.find_all("div", class_='thing')
    return posts, headers

def collect_text(post): # 
    headers = {'User-Agent': 'Mozilla/5.0'}
    post_path = post.find("a", class_='title may-blank')['href']
    post_url = f'https://old.reddit.com{post_path}'
    post_content = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(post_content.text, 'html.parser')
    text_pointer = soup.find("div", class_='sitetable linklisting').find('div', class_='thing').find('div', class_='entry unvoted').find_all('p')
    post_text = " ".join([paragraph.text for paragraph in text_pointer])
    return post_text

def fetch_post_title(post):
    title = post.find('p', class_="title").text.replace('(self.confessions)', '')
    return title

def print_upvotes(post):
    title = post.find('p', class_="title").text.replace('(self.confessions)', '')
    print(title)
    upvotes = post.find("div", attrs={"class": "score likes"}).text
    if upvotes == "•":
        upvotes = "None"
    result = f'liked {upvotes} times. Title: {title}'
    print(result)

def print_sentiment(post_content):
    blob = TextBlob(str(post_content))
    sentiment = blob.sentiment.polarity
    print("Sentiment= ", sentiment)

def main():
    start_time = time.time()
    url = 'https://old.reddit.com/r/confessions/top/?sort=top&t=all'
    posts, headers = fetch_posts(url)
    coresNr = multiprocessing.cpu_count()
    sys.setrecursionlimit(25000)
    with Pool(coresNr) as p: # cuts time to 32 s
        text = p.map(collect_text, posts)

    #text = [collect_text(post, headers) for post in posts]
    df = pd.DataFrame(np.array(text), columns=['posts'])
    print(df)
    print(f"{(time.time() - start_time):.2f} seconds")


if __name__ == '__main__':
    main()

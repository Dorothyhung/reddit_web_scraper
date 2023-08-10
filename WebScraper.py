from bs4 import BeautifulSoup
import requests
from collections import Counter
import nltk
#nltk.download('all')
from nltk import FreqDist
from textblob import TextBlob

def collect_posts(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    print('Creating requests ...')
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    posts = soup.find_all("div", class_='thing')
    return posts, headers

def collect_text(post, headers):
    title = post.find('p', class_="title").text.replace('(self.confessions)', '')
    print(title)
    post_path = post.find("a", class_='title may-blank')['href']
    post_url = f'https://old.reddit.com{post_path}'
    post_content = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(post_content.text, 'html.parser')
    site_table = soup.find("div", class_='sitetable linklisting')
    post_content = site_table.find('div', class_='thing').find('div', class_='entry unvoted').find_all('p')
    print_sentiment(post_content)

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
    url = 'https://old.reddit.com/r/confessions/top/?sort=top&t=all'
    posts, headers = collect_posts(url)
    for post in posts:
        collect_text(post, headers)

main()


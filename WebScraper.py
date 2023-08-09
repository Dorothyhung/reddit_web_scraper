from bs4 import BeautifulSoup
import requests
import csv
from collections import Counter


import nltk
#nltk.download('all')
from nltk import FreqDist
#from ntlk.corpus import stopwords
from textblob import TextBlob



url = 'https://old.reddit.com/r/confessions/top/?sort=top&t=all'
headers = {'User-Agent': 'Mozilla/5.0'}
print('Creating requests ...')
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
posts = soup.find_all("div", class_='thing')
words = ""
print("Gathering post content ...")
for post in posts:
    title = post.find('p', class_="title").text.replace('(self.confessions)', '')
    print(title)
    upvotes = post.find("div", attrs={"class": "score likes"}).text
    if upvotes == "•":
        upvotes = "None"
    result = f'liked {upvotes} times. Title: {title}'


    post_link = post.find("a", class_='title may-blank')['href']
    #print(post_link)
    post_url = f'https://old.reddit.com{post_link}'
    post_content = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(post_content.text, 'html.parser')
    site_table = soup.find("div", class_='sitetable linklisting')
    post_content = site_table.find('div', class_='thing').find('div', class_='entry unvoted').find_all('p')
    blob = TextBlob(str(post_content))
    sentiment = blob.sentiment.polarity
    print("Sentiment= ", sentiment)
    for paragraph in post_content:
        #print(paragraph.text)
        words = words + paragraph.text

print("Calculating word counts ...")
#freq = Counter(words.split()).most_common()
# freq = FreqDist(words.lower().split())
# print(freq)
# print(freq.most_common())

blob = TextBlob(words)
sentiment = blob.sentiment.polarity
print("Sentiment= ", sentiment)
    # with open('./source/repos/WebScraper/redditconfessions.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([result])

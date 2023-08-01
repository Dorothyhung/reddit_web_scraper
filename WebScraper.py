from bs4 import BeautifulSoup
import requests
import csv

url = 'https://old.reddit.com/r/confessions/top/?sort=top&t=all'
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
posts = soup.find_all("div", class_='thing')
for post in posts:
    title = post.find('p', class_="title").text.replace('(self.confessions)', '')
    upvotes = post.find("div", attrs={"class": "score likes"}).text
    if upvotes == "•":
        upvotes = "None"
    result = f'liked {upvotes} times. Title: {title}'


    post_link = post.find("a", class_='title may-blank')['href']
    print(post_link)
    post_url = f'https://old.reddit.com{post_link}'
    post_content = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(post_content.text, 'html.parser')
    site_table = soup.find("div", class_='sitetable linklisting')
    post_content = site_table.find('div', class_='thing').find('div', class_='entry unvoted').find_all('p')
    for paragraph in post_content:
        print(paragraph.text)



    # with open('./source/repos/WebScraper/redditconfessions.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([result])

# import requests

# username = "espn"
# url = 'https://www.instagram.com/' + username
# r = requests.get(url).text

# start = '"edge_followed_by":{"count":'
# end = '},"followed_by_viewer"'
# followers= r[r.find(start)+len(start):r.rfind(end)]

# start = '"edge_follow":{"count":'
# end = '},"follows_viewer"'
# following= r[r.find(start)+len(start):r.rfind(end)]

# print(followers, following)

# https://www.octoparse.com/blog/how-to-scrape-yahoo-finance
import requests
from bs4 import BeautifulSoup
import pandas as pd
#get the URL using response variable
# my_url = "https://finance.yahoo.com/news"
my_url = "https://www.instagram.com/tsai_ingwen/?hl=en"
response = requests.get(my_url)

#Catching Exceptions
print("response.ok : {} , response.status_code : {}".format(response.ok , response.status_code))
# print("Preview of response.text : ", response.text[:500])
#utility function to download a webpage and return a beautiful soup doc
def get_page(url):
  response = requests.get(url)
  if not response.ok:
    print('Status code:', response.status_code)
    raise Exception('Failed to load page {}'.format(url))
  page_content = response.text
  doc = BeautifulSoup(page_content, 'lxml')
  return doc

#function call
doc = get_page(my_url)
#appropritae tags common to news-headlines to filter out the necessary information.
# a_tags = doc.find_all('a', {'class': "js-content-viewer"})
a_tags = doc.find_all('span')
print(len(a_tags),'a',a_tags)

#print(a_tags[1])
news_list = []

#print top 10 Headlines
for i in range(1,len(a_tags)+1):
  news = a_tags[i-1].text
  news_list.append(news)
  print("Headline "+str(i)+ ":" + news)
news_df = pd.DataFrame(news_list)
news_df.to_csv('Market_News')
# https://finance.yahoo.com/quote/YM=F?p=YM=F&.tsrc=fin-srch
# https://www.octoparse.com/blog/how-to-scrape-yahoo-finance
import requests
from bs4 import BeautifulSoup
import pandas as pd
#get the URL using response variable
# my_url = "https://finance.yahoo.com/news"
# my_url = "https://mis.taifex.com.tw/futures/RegularSession/EquityIndices/FuturesDomestic/"
# my_url = "https://www.wantgoo.com/futures/wtxm&"
my_url = "https://histock.tw/index-tw/FITX"
def get_page(url):
  headers = {"User-Agent":"Mozilla/5.0"}
  response = requests.get(url, headers=headers)
  if not response.ok:
    print('Status code:', response.status_code)
    raise Exception('Failed to load page {}'.format(url))
  page_content = response.text
  doc = BeautifulSoup(page_content, 'html.parser')
  title_tag = doc.title
  print(title_tag)
  # tags = doc.find_all("div", {"c-model":"close"})
  price = doc.find_all("span", id="Price1_lbTPrice")
  price = price[0].string
  change = doc.find_all("span", id="Price1_lbTChange")
  change = change[0].string[1:]
  percent = doc.find_all("span", id="Price1_lbTPercent")
  percent = percent[0].string[:-1]
  print( price, change, percent)
  # price = tags[3].string
  # amp = tags[4].string
  # percent = tags[5].string

  # print(tags, price, amp, percent)
  # b_tag = doc.find_all("span", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")
  # print(b_tag)
  # print(tags.find_all("span"))


  return doc
  return response.text

#function call
doc = get_page(my_url)
# print(doc)

# https://stackoverflow.com/questions/41909065/scrape-data-with-beautifulsoup-results-in-404
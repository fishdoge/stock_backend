
from flask import Flask
import yfinance as yf
import json 
import requests as r
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    return "test   !  "

# read json file 
def readjson(jsonFilePath):
    jdict = {}
    with open(jsonFilePath, encoding='utf-8') as j:
        jdict = json.load(j)
    return jdict

# profit and yield history
@app.route('/tradehistory')
def tradehistory():
  jsonFilePath = r'./get_tx_history/history/yield_tx_dow_22_23.json'
  his = readjson(jsonFilePath)
  data = {"data": his}
  # print(type(his), data)
  return data

# profit and yield history
@app.route('/yphistory')
def yphistory():
  jsonFilePath = r'./get_tx_history/history/yield_m_22_23.json'
  his = readjson(jsonFilePath)
  # print(type(his))
  return his
  
@app.route('/realtime')
def getPrices():
  tx = getTx()
  ym = getYm()
  response = r.get("http://worldtimeapi.org/api/timezone/Asia/Taipei")
  time = json.loads(response.text)
  myRes={"tx": tx, "ym": ym, "time": time}
  # print(type(myRes), myRes, time['datetime'])
  return myRes

def getTx():
  url = "https://histock.tw/index-tw/FITX"
  headers = {"User-Agent":"Mozilla/5.0"}
  response = r.get(url, headers=headers)
  if not response.ok:
    print('Status code:', response.status_code)
    raise Exception('Failed to load page {}'.format(url))
  page_content = response.text
  doc = BeautifulSoup(page_content, 'html.parser')
  title_tag = doc.title
  # print(title_tag)
  price = doc.find_all("span", id="Price1_lbTPrice")
  price = float(price[0].string)
  change = doc.find_all("span", id="Price1_lbTChange")
  change = float(change[0].string[1:])
  percent = doc.find_all("span", id="Price1_lbTPercent")
  percent = float(percent[0].string[:-1])
  # print( price, change, percent)
  return {"open": price-change, "price": price, "change": change, "percent": percent}

def getYm():
  url = "https://finance.yahoo.com/quote/YM=F"
  response = r.get(url, headers={"User-Agent":"Mozilla/5.0"})
  if not response.ok:
    print('Status code:', response.status_code)
    raise Exception('Failed to load page {}'.format(url))
  page_content = response.text
  doc = BeautifulSoup(page_content, 'html.parser')
  title_tag = doc.title.string
  # print(title_tag)
  tags = doc.find_all(["fin-streamer"], limit=7)
  # print(len(tags),tags)
  price = float((tags[3].string).replace(",", ""))
  change = float(tags[4].string)
  percent = float(tags[5].string[1:-2])
  open = float(((doc.find_all("td", {"data-test":"OPEN-value"},  limit=1))[0].string).replace(",", ""))
  # print(tags)
  return {"open": open,"price": price, "change": change, "percent": percent}


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]


# {'SymbolID': 'TXFH3-M', 'SpotID': '', 'DispCName': '臺指期083', 'DispEName': 'TX083', 'Status': '', 'CBidPrice1': '17244.00', 'CBidSize1': '14', 'CAskPrice1': '17246.00', 'CAskSize1': '16', 'CTotalVolume': '10547', 'COpenPrice': '17199.00', 'CHighPrice': '17247.00', 'CLowPrice': '17193.00', 'CLastPrice': '17245.00', 'CRefPrice': '17182.00', 'CCeilPrice': '18900.00', 'CFloorPrice': '15464.00', 'SettlementPrice': '','OpenInterest': '', 'CDate': '20230725', 'CTime': '192844', 'CTestTime': '145955', 'CDiff': '63.00', 'CDiffRate': '0.37', 'CAmpRate': '0.31', 'CBestBidPrice': '17244.00', 'CBestAskPrice': '17246.00', 'CBestBidSize': '14', 'CBestAskSize': '16', 'CTestPrice': '17197.00', 'CTestVolume': '55'}
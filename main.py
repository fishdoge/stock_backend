
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
  print(type(his), data)
  return data

# profit and yield history
@app.route('/yphistory')
def yphistory():
  jsonFilePath = r'./get_tx_history/history/yield_m_22_23.json'
  his = readjson(jsonFilePath)
  print(type(his))
  return his
  
@app.route('/realtime')
def getPrices():
  myRes={}
  url = "https://mis.taifex.com.tw/futures/api/getQuoteList"
  payload = {"MarketType":"0",
            "SymbolType":"F",
            "KindID":"1",
            "CID":"TXF",
            "ExpireMonth":"",
            "RowSize":"全部",
            "PageNo":"",
            "SortColumn":"",
            "AscDesc":"A"}
  res = r.post(url, json = payload)
  data = res.json()
  tx_new = data["RtData"]["QuoteList"][1]
  # myRes["tx_new"] = {"DispEName": tx_new["DispEName"], "Status": tx_new["Status"], "CLastPrice": tx_new["CLastPrice"]}
  myRes["tx_new"] = tx_new
  payload["MarketType"] = "1"
  res = r.post(url, json = payload)
  data = res.json()
  tx_pm = data["RtData"]["QuoteList"][1]
  print(tx_pm)
  # myRes["tx_pm"] = {"DispEName": tx_pm["DispEName"], "Status": tx_pm["Status"], "CLastPrice": tx_pm["CLastPrice"]}
  myRes["tx_pm"] = tx_pm
  url = "https://finance.yahoo.com/quote/YM=F"
  response = r.get(url, headers={"User-Agent":"Mozilla/5.0"})
  if not response.ok:
    print('Status code:', response.status_code)
    raise Exception('Failed to load page {}'.format(url))
  page_content = response.text
  doc = BeautifulSoup(page_content, 'html.parser')
  title_tag = doc.title.string
  print(title_tag)
  tags = doc.find_all(["fin-streamer"], limit=7)
  print(len(tags),tags)
  price = tags[3].string
  amp = tags[4].string
  percent = tags[5].string

  # print(price, amp, percent)
  myRes['edji'] = {'title': title_tag, 'price': price, 'amp': amp, 'percent': percent}
  
  # print(type(myRes), myRes)
  return myRes


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]


# {'SymbolID': 'TXFH3-M', 'SpotID': '', 'DispCName': '臺指期083', 'DispEName': 'TX083', 'Status': '', 'CBidPrice1': '17244.00', 'CBidSize1': '14', 'CAskPrice1': '17246.00', 'CAskSize1': '16', 'CTotalVolume': '10547', 'COpenPrice': '17199.00', 'CHighPrice': '17247.00', 'CLowPrice': '17193.00', 'CLastPrice': '17245.00', 'CRefPrice': '17182.00', 'CCeilPrice': '18900.00', 'CFloorPrice': '15464.00', 'SettlementPrice': '','OpenInterest': '', 'CDate': '20230725', 'CTime': '192844', 'CTestTime': '145955', 'CDiff': '63.00', 'CDiffRate': '0.37', 'CAmpRate': '0.31', 'CBestBidPrice': '17244.00', 'CBestAskPrice': '17246.00', 'CBestBidSize': '14', 'CBestAskSize': '16', 'CTestPrice': '17197.00', 'CTestVolume': '55'}
from flask import Flask
import requests as r
import time
# import pandas as pd
import yfinance as yf
import json 

app = Flask(__name__)

@app.route('/getprices')
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
  myRes["tx_new"] = {"DispEName": tx_new["DispEName"], "Status": tx_new["Status"], "CLastPrice": tx_new["CLastPrice"]}

  payload["MarketType"] = "1"
  res = r.post(url, json = payload)
  data = res.json()
  tx_pm = data["RtData"]["QuoteList"][1]
  myRes["tx_pm"] = {"DispEName": tx_pm["DispEName"], "Status": tx_pm["Status"], "CLastPrice": tx_pm["CLastPrice"]}

  stock = yf.Ticker("YM=F")
  data = stock.info
  myRes["edji"] = {"DispEName": "YM=F", "bid": data["bid"], "ask": data["ask"]}
  
  print(myRes)
  return myRes

@app.route('/')
def index():
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
  
  stock = yf.Ticker("%5EDJI")
  data = stock.info
  print(data)
  return data

@app.route('/get')
def get():
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
  # print("txf",data.RtData.QuoteList[0].CLastPrice)
  # print(data.keys())
  # print(data.keys(),data["RtData"]["QuoteList"][0]["DispCName"],data["RtData"]["QuoteList"][0]["DispEName"])
  # for y in data["RtData"]["QuoteList"]:
  #   myRes[y["DispEName"]] = {"DispEName": y["DispEName"], "CLastPrice": y["CLastPrice"], "Status": y["Status"]}

  y = data[0]
  myRes[y["DispEName"]] = {"DispEName": y["DispEName"], "CLastPrice": y["CLastPrice"], "Status": y["Status"]}

  payload = {"MarketType":"1",
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

  return myRes

# profit and yield history
def readjson(jsonFilePath):
    jdict = {}
    with open(jsonFilePath, encoding='utf-8') as j:
        jdict = json.load(j)
    return jdict

@app.route('/yphistory')
def yphistory():
  jsonFilePath = r'./get_tx_history/history/yield_m_22_23.json'
  his = readjson(jsonFilePath)
  print(type(his))
  return his
  

app.run(host='0.0.0.0', port=81)

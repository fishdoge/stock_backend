from flask import Flask
import requests as r
# import pandas as pd

app = Flask(__name__)


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
  print("f",data)
  return data


app.run(host='0.0.0.0', port=81)

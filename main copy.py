from flask import Flask
import yfinance as yf
import json 
import requests as r

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
  # k = stock.info
  # myRes["edji"] = {"DispEName": "YM=F", "bid": data["bid"], "ask": data["ask"]}

# requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: https://query2.finance.yahoo.com/v10/finance/quoteSummary/YM=F?modules=summaryProfile%2CfinancialData%2CquoteType%2CdefaultKeyStatistics%2CassetProfile%2CsummaryDetail&ssl=true
  url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/YM=F?modules=summaryProfile%2CfinancialData%2CquoteType%2CdefaultKeyStatistics%2CassetProfile%2CsummaryDetail&ssl=true'
  res = r.get(url)
  # k = res.json()
  print(type(myRes), type(res))
  return myRes

@app.route('/sc')
def sc():
  api_url = 'https://www.page2api.com/api/v1/scrape'
  payload = {
    "api_key": "0990b538cafcbfcd4f23dada11d5e41e31d7673f",
    "url": "https://finance.yahoo.com/quote/YM=F?p=YM=F&.tsrc=fin-srch",
    "parse": {
      "name": "#quote-header-info h1 >> text",
      "price": "#quote-header-info [data-field=regularMarketPrice] >> text",
      "change": "#quote-header-info [data-field=regularMarketChange] >> text",
      "change_percent": "#quote-header-info [data-field=regularMarketChangePercent] >> text"
    }
  }

  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  response = r.post(api_url, data=json.dumps(payload), headers=headers)
  result = json.loads(response.text)
  print(result['result'])
  return result['result']


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]

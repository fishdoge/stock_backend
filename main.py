
from flask import Flask
import yfinance as yf
import json 
import requests as r
from bs4 import BeautifulSoup
from flask import request  # Import the request object from flask


app = Flask(__name__)

# Define a Data Model for Trade Records
class TradeRecord:
    def __init__(self, stop_30, stop_50, action, buy_price, dow_percent, high, is_summer, low, percentage_gap, profit, sell_price, time, tx_percent):
        self.data = {
            '30_stop': stop_30,
            '50_stop': stop_50,
            'action': action,
            'buy_price': buy_price,
            'dow_percent': dow_percent,
            'high': high,
            'is_summer': is_summer,
            'low': low,
            'percentage_gap': percentage_gap,
            'profit': profit,
            'sell_price': sell_price,
            'time': time,
            'tx_percent': tx_percent
        }

    def to_dict(self):
        return self.data

# Read JSON file 
def readjson(jsonFilePath):
    jdict = {}
    with open(jsonFilePath, encoding='utf-8') as j:
        jdict = json.load(j)
    return jdict



@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    return "test   !  "

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
  myRes={"tx": tx, "ym": ym, "tx_ym_gap": ym["percent"]-tx["percent"], "time": time}
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
  price = float((tags[2].string).replace(",", ""))
  change = float(tags[3].string)
  percent = float(tags[4].string[1:-2])
  open = float(price+change)
  # print(tags)
  return {"open": open,"price": price, "change": change, "percent": percent}

@app.route('/tradehistory/add_record', methods=['POST'])
def add_trade_record():
    try:
        request_data = request.get_json()
        required_fields = [
            '30_stop', '50_stop', 'action', 'buy_price', 'dow_percent', 'high', 
            'is_summer', 'low', 'percentage_gap', 'profit', 'sell_price', 'time', 'tx_percent'
        ]
        if not all(field in request_data for field in required_fields):
            return "Missing required fields in the request data", 400

        # Rename the fields from request_data
        request_data['stop_30'] = request_data.pop('30_stop')
        request_data['stop_50'] = request_data.pop('50_stop')

        new_record = TradeRecord(**request_data)
        jsonFilePath = r'./get_tx_history/history/yield_tx_dow_22_23.json'
        existing_data = readjson(jsonFilePath)
        existing_data.append(new_record.to_dict())
        with open(jsonFilePath, 'w', encoding='utf-8') as j:
            json.dump(existing_data, j, ensure_ascii=False, indent=4)

        return "Trade record added successfully"
    except Exception as e:
        return str(e), 500


# Update (Modify Trade Record in JSON File)
@app.route('/tradehistory/update_record/<int:id>', methods=['PUT'])
def update_trade_record(id):
    try:
        updated_data = request.get_json()
        jsonFilePath = r'./get_tx_history/history/yield_tx_dow_22_23.json'
        existing_data = readjson(jsonFilePath)

        required_fields = [
            '30_stop', '50_stop', 'action', 'buy_price', 'dow_percent', 'high',
            'is_summer', 'low', 'percentage_gap', 'profit', 'sell_price', 'time', 'tx_percent'
        ]
        if not all(field in updated_data for field in required_fields):
            return "Missing required fields in the request data", 400

        if 0 <= id < len(existing_data):
            # Rename the field in existing_data
            if '30_stop' in updated_data:
                existing_data[id]['30_stop'] = updated_data.pop('30_stop')
            if '50_stop' in updated_data:
                existing_data[id]['50_stop'] = updated_data.pop('50_stop')

            existing_data[id].update(updated_data)

            with open(jsonFilePath, 'w', encoding='utf-8') as j:
                json.dump(existing_data, j, ensure_ascii=False, indent=4)

            return "Trade record updated successfully"
        else:
            return "Trade record not found", 404
    except Exception as e:
        return str(e), 500

# Read (Retrieve) Trade History from JSON File
@app.route('/tradehistory', methods=['GET'])
def get_trade_history():
    jsonFilePath = r'./get_tx_history/history/yield_tx_dow_22_23.json'
    his = readjson(jsonFilePath)
    data = {"data": his}
    return data

# Delete (Remove Trade Record from JSON File)
@app.route('/tradehistory/delete_record/<int:id>', methods=['DELETE'])
def delete_trade_record(id):
    try:
        jsonFilePath = r'./get_tx_history/history/yield_tx_dow_22_23.json'
        existing_data = readjson(jsonFilePath)

        if 0 <= id < len(existing_data):
            existing_data.pop(id)

            with open(jsonFilePath, 'w', encoding='utf-8') as j:
                json.dump(existing_data, j, ensure_ascii=False, indent=4)

            return "Trade record deleted successfully"
        else:
            return "Trade record not found", 404
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]


# {'SymbolID': 'TXFH3-M', 'SpotID': '', 'DispCName': '臺指期 083', 'DispEName': 'TX083', 'Status': '', 'CBidPrice1': '17244.00', 'CBidSize1': '14', 'CAskPrice1': '17246.00', 'CAskSize1': '16', 'CTotalVolume': '10547', 'COpenPrice': '17199.00', 'CHighPrice': '17247.00', 'CLowPrice': '17193.00', 'CLastPrice': '17245.00', 'CRefPrice': '17182.00', 'CCeilPrice': '18900.00', 'CFloorPrice': '15464.00', 'SettlementPrice': '','OpenInterest': '', 'CDate': '20230725', 'CTime': '192844', 'CTestTime': '145955', 'CDiff': '63.00', 'CDiffRate': '0.37', 'CAmpRate': '0.31', 'CBestBidPrice': '17244.00', 'CBestAskPrice': '17246.00', 'CBestBidSize': '14', 'CBestAskSize': '16', 'CTestPrice': '17197.00', 'CTestVolume': '55'}
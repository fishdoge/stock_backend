from flask import Flask
import requests as r
import time
# import pandas as pd
import yfinance as yf
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

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
  print(tx_new)
  myRes["tx_new"] = {"DispEName": tx_new["DispEName"], "Status": tx_new["Status"], "COpenPrice": tx_new["COpenPrice"], "CLastPrice": tx_new["CLastPrice"]}

  payload["MarketType"] = "1"
  res = r.post(url, json = payload)
  data = res.json()
  tx_pm = data["RtData"]["QuoteList"][1]
  myRes["tx_pm"] = {"DispEName": tx_pm["DispEName"], "Status": tx_pm["Status"], "COpenPrice": tx_pm["COpenPrice"], "CLastPrice": tx_pm["CLastPrice"]}

  stock = yf.Ticker("YM=F")
  data = stock.info
  myRes["edji"] = {"DispEName": "YM=F", "bid": data["bid"], "ask": data["ask"]}
  
  print(myRes)
  return myRes

@app.route('/')
def index():
  i = 0
  while(True):
    time.sleep(4)
    print("LOOP", i)
    i = i+1
    subject = "Email Subject"
    body = "This is the body of the text message"
    sender = "wesley@hongwangtec.com"
    password = "tpgvzwefzlctvjas"
    receiver = ["wesliutw@gmail.com"]
    if(i%1200==0):
      send_email(subject, body, sender, receiver, password)
  return 0

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

@app.route('/trigger')
def trigger():
  return "200"
  
# def testLoop():
  # while(True):
  #   time.sleep(4)
  #   print("LOOP")
    
app.run(host='0.0.0.0', port=81)
# testLoop()



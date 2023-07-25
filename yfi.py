# https://www.page2api.com/blog/how-to-scrape-yahoo-finance/
import requests
import json

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
response = requests.post(api_url, data=json.dumps(payload), headers=headers)
result = json.loads(response.text)

print(result)

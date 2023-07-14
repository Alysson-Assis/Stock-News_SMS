import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "WT0YDQ52U3D14WDC."
NEWS_API_KEY = "b8df6f80f37045ddb9851bbcb38e85ff"




stock_url = "https://www.alphavantage.co/query"


stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(stock_url, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
# print(stock_data)
days_data = stock_data["Time Series (Daily)"]
data_list = [value for (key, value) in days_data.items()]
close_yesterday = float(data_list[0]["4. close"])
open_day = float(data_list[1]["4. close"])
# print(close_yesterday)
# print(open_day)

difference = abs(close_yesterday - open_day)
percent = round((difference/close_yesterday) * 100)
# print(percent)

up_down = None
if percent > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

news_url = "https://newsapi.org/v2/everything"
news_params = {
    'qInTitle': COMPANY_NAME,
    'apiKey': NEWS_API_KEY
}

news_response = requests.get(news_url, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
articles = news_data["articles"]
three_articles = articles[:3]
# print(three_articles)


text_message = [f'{COMPANY_NAME}: {up_down}{percent}% \nHeadline: {article["title"]}. \nBrief: {article["description"]}' for article in three_articles]
# print(text_message)

account_sid = "AC1c59bf4f835869a1af5a94705a2255a5"
auth_token = "56ab886252ac607cc4885f04aebad5d6"
client = Client(account_sid, auth_token)

for article in text_message:
    message = client.messages.create(
        body=article,
        from_='+12345162408',
        to='+5511941109001'
    )
    
    print(message.status)



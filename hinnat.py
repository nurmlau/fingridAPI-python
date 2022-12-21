import requests
import xml.etree.ElementTree as ET
import xmltodict
import json
from datetime import date
import datetime
import secrets

today = date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

yesterdaystamp = yesterday.strftime("%Y%m%d")
tomorrowstamp = tomorrow.strftime("%Y%m%d")
mw = 999.59785523

url = f"https://web-api.tp.entsoe.eu/api?securityToken={secrets.entsoeKey}&documentType=A44&in_Domain=10YFI-1--------U&out_Domain=10YFI-1--------U&periodStart={yesterdaystamp}2300&periodEnd={tomorrowstamp}2300"


result = requests.get(url, headers = {})

data = xmltodict.parse(result.content)



hours = ["00-01", "01-02", "02-03", "03-04", "04-05", "05-06", "06-07", "07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-24",]

temp = []
for item in data["Publication_MarketDocument"]["TimeSeries"]:

    for i in item["Period"]["Point"]:
        price = float(i["price.amount"]) / mw * 100
        temp.append(price)

priceData = []
for i in range(47):
    if i >= 23:
        priceData.append(temp[i])

for i in range(24):
    print(tomorrow, hours[i], "{:.2f}".format(priceData[i]))

    


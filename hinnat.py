import requests
import xmltodict
from datetime import date
import datetime
import secrets

today = date.today()
dayafter = today - datetime.timedelta(days=2)
tomorrow = today + datetime.timedelta(days=1)

dayafterstamp = dayafter.strftime("%Y%m%d")
tomorrowstamp = tomorrow.strftime("%Y%m%d")
mw = 999.59785523

url = f"https://web-api.tp.entsoe.eu/api?securityToken={secrets.entsoeKey}&documentType=A44&in_Domain=10YFI-1--------U&out_Domain=10YFI-1--------U&periodStart={dayafterstamp}2300&periodEnd={tomorrowstamp}2300"


result = requests.get(url, headers = {})

data = xmltodict.parse(result.content)

hours = ["00-01", "01-02", "02-03", "03-04", "04-05", "05-06", "06-07", "07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-24",]

try:

    temp = []
    for item in data["Publication_MarketDocument"]["TimeSeries"]:

        for i in item["Period"]["Point"]:
            price = float(i["price.amount"]) / mw * 100
            temp.append(price)

    

    todayPrices = temp[23:47]

    if len(temp) > 48:
        tomorrowPrices = temp[47:]


    print("Today prices:              Tomorrow prices:")
    for i in range(24):

        if len(tomorrowPrices) > 0:
            tomorrowPrint = str(tomorrow) + " " + hours[i] + " " + "{:.2f}".format(tomorrowPrices[i])
        
        else:
            tomorrowPrint = ""

        print(today, hours[i], "{:.2f}".format(todayPrices[i]), "---", tomorrowPrint)

except NameError:
    pass
    

    


import requests
import secrets
from rich.tree import Tree
from rich import print
from rich.console import Console
from rich.table import Table
import xmltodict
from datetime import date
import datetime as d
from datetime import datetime

def getGridData():

    try:

        url = "https://api.fingrid.fi/v1/variable/event/json/336%2C177%2C201%2C188%2C191%2C202%2C181%2C209%2C192%2C193"

        result = requests.get(url, headers = {"x-api-key": secrets.key})

        data = result.json()

        windpower = production = consumption = status = industrial = water = nuclear = kauko = frequency = shortage = ""

        for item in data:
            if item["variable_id"] == 181: windpower = item["value"]
            if item["variable_id"] == 192: production = item["value"]
            if item["variable_id"] == 193: consumption = item["value"]
            if item["variable_id"] == 209: status = item["value"]
            if item["variable_id"] == 202: industrial = item["value"]
            if item["variable_id"] == 191: water = item["value"]
            if item["variable_id"] == 188: nuclear = item["value"]
            if item["variable_id"] == 201: kauko = item["value"]
            if item["variable_id"] == 177: frequency = item["value"]
            if item["variable_id"] == 336: shortage = item["value"]

        match status:
            case 1:
                status = "[green]Vihreä: [default]Sähköjärjestelmän käyttötilanne on normaali"
            case 2:
                status = "[yellow]Keltainen: [default]Sähköjärjestelmän käyttötilanne on heikentynyt. Sähkön riittävyys Suomessa on uhattuna (sähköpulan riski on suuri) tai voimajärjestelmä ei täytä käyttövarmuuskriteerejä"
            case 3:
                status = "[red]Punainen: [default]Sähköjärjestelmän käyttövarmuus on vaarassa. Sähkönkulutusta on kytketty irti voimajärjestelmän"
            case 4:
                status = "[black]Musta: [default]Vakava laajaa osaa tai koko Suomea kattava häiriö"
            case 5:
                status = "[blue]Sininen: [default]Vakavan häiriön käytönpalautus on menossa."

        match shortage:
            case 0:
                shortage = "[green]Normaali"
            case 1:
                shortage = "[orange3]Sähköpula mahdollinen"
            case 2:
                shortage = "[darkred]Sähköpulan riski suuri"
            case 3:
                shortage = "[red3]Sähköpula"

        output = Tree("Suomen sähköverkko")

        table = Table(show_header=False)

        table.add_column(justify="left", style="medium_violet_red", no_wrap=True)
        table.add_column(justify="right", style="cyan")
        table.add_column(justify="right", style="red")

        table.add_row("Ydinvoima", str(nuclear), str(round(nuclear / production * 100, 1)) + "%")
        table.add_row("Tuulivoima", str(windpower), str(round(windpower / production * 100, 1)) + "%")
        table.add_row("Teollisuus", str(industrial), str(round(industrial / production * 100, 1)) + "%")
        table.add_row("Vesivoima", str(water), str(round(water / production * 100, 1)) + "%")
        table.add_row("Kaukolämpö", str(kauko), str(round(kauko / production * 100, 1)) + "%")
        table.add_row("Muu", str(round(production - (windpower + industrial + water + nuclear + kauko), 1)), str(round((production - (windpower + industrial + water + nuclear + kauko)) / production * 100, 1)) + "%")

        output.add("Tuotanto Suomessa: " + "[bright_cyan]" + str(production) + " [default]MW").add(table)

        consumptionBranch = output.add("Kulutus Suomessa: " + "[bright_cyan]" + str(consumption) + " [default]MW")

        suffiency = round(production - consumption, 2)
        
        if suffiency < 0:
            suffiency = "[red]" + str(suffiency)
        else:
            suffiency = "[green]" + str(suffiency)
        consumptionBranch.add("Omavaraisuus: " + suffiency + " [default]MW")

        statusBranch = output.add("Sähköverkon tila")
        statusBranch.add(status)
        statusBranch.add("Sähköverkon taajuus: " + "[bright_cyan]" + str(frequency) + " [default]Hz")
        statusBranch.add("Sähköpula: " + shortage)
        output.add("Hintatiedot: c/kWh (alv 10%)")
        console = Console()
        console.print(output)
    
    except Exception as e:
        print(e)

def getPriceData():

    today = date.today()
    time = datetime.now()
    hour = int(time.strftime("%H"))
    
    dayafter = today - d.timedelta(days=2)
    tomorrow = today + d.timedelta(days=1)

    dayafterstamp = dayafter.strftime("%Y%m%d")
    tomorrowstamp = tomorrow.strftime("%Y%m%d")

    url = f"https://web-api.tp.entsoe.eu/api?securityToken={secrets.entsoeKey}&documentType=A44&in_Domain=10YFI-1--------U&out_Domain=10YFI-1--------U&periodStart={dayafterstamp}2300&periodEnd={tomorrowstamp}2300"

    result = requests.get(url, headers = {})

    data = xmltodict.parse(result.content)

    hours = ["00-01", "01-02", "02-03", "03-04", "04-05", "05-06", "06-07", "07-08", "08-09", "09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23", "23-24",]

    try:

        temp = []
        for item in data["Publication_MarketDocument"]["TimeSeries"]:

            for i in item["Period"]["Point"]:
                price = float(i["price.amount"]) / 10 * 1.1
                temp.append(price)
   
        todayPrices = temp[23:47]
        tomorrowPrices = ""
        topic = "Hinnat tänään              Ei vielä huomisen hintatietoja"
        if len(temp) > 48:
            tomorrowPrices = temp[47:]
            topic = "Hinnat tänään              Hinnat huomenna"

        print(topic)

        for i in range(24):
            
            todayColor = "[green]"
            tomorrowColor = "[green]"

            if todayPrices[i] > 20: todayColor = "[orange1]"
            if todayPrices[i] > 40: todayColor = "[red]"
            
            if len(tomorrowPrices) > 0:
                if tomorrowPrices[i] > 20: tomorrowColor = "[orange1]"
                if tomorrowPrices[i] > 40: tomorrowColor = "[red]"
                tomorrowPrint = str(tomorrow) + " [medium_violet_red]" + hours[i] + " " + tomorrowColor + "{:.2f}".format(tomorrowPrices[i])
            
            else:
                tomorrowPrint = ""

            indicator = "---"

            if (hour) == i:
                indicator = "[bold][red]<<<"

            print(today, "[medium_violet_red]" + hours[i], todayColor + "{:.2f}".format(todayPrices[i]), indicator, tomorrowPrint)

    except Exception as e:
        print(e)

def main():
    
    getGridData()
    getPriceData()

if __name__ == "__main__":
    main()



import requests
import secrets
from rich.tree import Tree
from rich import print
from rich.console import Console
from rich.table import Table

url = "https://api.fingrid.fi/v1/variable/event/json/336%2C177%2C201%2C188%2C191%2C202%2C181%2C209%2C192%2C193"

result = requests.get(url, headers = {"x-api-key": secrets.key})

data = result.json()

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

suffiency = production - consumption
if suffiency < 0:
    suffiency = "[red]" + str(suffiency)
else:
    suffiency = "[green]" + str(suffiency)
consumptionBranch.add("Omavaraisuus: " + suffiency + " [default]MW")

statusBranch = output.add("Sähköverkon tila")
statusBranch.add(status)
statusBranch.add("Sähköverkon taajuus: " + "[bright_cyan]" + str(frequency) + " [default]Hz")
statusBranch.add("Sähköpula: " + shortage)
console = Console()
console.print(output)




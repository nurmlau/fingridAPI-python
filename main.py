import requests
import secrets

url = "https://api.fingrid.fi/v1/variable/event/json/192%2C193"


result = requests.get(url, headers = {"x-api-key": secrets.key})

sahko = result.json()

print("Tuotanto:", sahko[1]["value"])
print("Kulutus:", sahko[0]["value"])


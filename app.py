import requests

funds = [
    "120503",
    "118989",
    "122639"
]

for scheme_code in funds:
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)
    data = response.json()

    print("-" * 50)
    print("Scheme :", data["meta"]["scheme_name"])
    print("NAV    :", data["data"][0]["nav"])
    print("Date   :", data["data"][0]["date"])
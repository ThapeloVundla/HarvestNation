import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.agrimag.co.za/commodities"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_commodities():
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find("tbody").find_all("tr")

    commodities = []

    for row in rows[:5]:  # Only first 5 rows
        cols = row.find_all("td")

        if len(cols) < 5:
            continue  # Skip malformed rows

        agriculture = cols[0].get_text(strip=True)
        unit = cols[1].get_text(strip=True)
        price = "R" + cols[2].get_text(strip=True)
        date = cols[3].get_text(strip=True)

        # Handle "Change" column (nested div + possible icon)
        change = cols[4].get_text(strip=True)

        commodity_data = {
            "agriculture": agriculture,
            "unit": unit,
            "price": price,
            "date": date,
            "change": change
        }

        commodities.append(commodity_data)

    return commodities


def save_to_json(data):
    with open("commodities.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    data = fetch_commodities()

    if data:
        save_to_json(data)
        print("commodities.json created successfully")
    else:
        print("No data to save")    
import csv
import requests
import datetime


def replace_string(str) -> str:
    return str.split(" ")[0]


def get_prayer_time(data):
    month_index = 1
    fieldnames = [
        "Day",
        "Fajr",
        "Sunrise",
        "Dhuhr",
        "Asr",
        "Maghrib",
        "Isha"
    ]

    with open("prayer_time.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        while month_index < 13:
            for day in data[str(month_index)]:
                print(f"Date: {day['date']['gregorian']['date']}")

                writer.writerow({
                    "Day": day["date"]["gregorian"]["date"],
                    "Fajr": replace_string(day["timings"]["Fajr"]),
                    "Sunrise": replace_string(day["timings"]["Sunrise"]),
                    "Dhuhr": replace_string(day["timings"]["Dhuhr"]),
                    "Asr": replace_string(day["timings"]["Asr"]),
                    "Maghrib": replace_string(day["timings"]["Maghrib"]),
                    "Isha": replace_string(day["timings"]["Isha"]),
                })
        
            month_index += 1

    print("File generated prayer_time.csv")


if __name__ == "__main__":
    latitude = "40.837048"
    longitude = "-73.865433"
    year = str(datetime.date.today().year)
    whole_year = "true"
    query_params = {
        "latitude": latitude,
        "longitude": longitude,
        "year": year,
        "annual": whole_year
    }
    url = "http://api.aladhan.com/v1/calendar"

    print(f"Getting prayer times of {year}\n")

    req = requests.get(url, params=query_params)
    data = req.json()

    if data["code"] == 200 and data["status"] == "OK":
        get_prayer_time(data=data["data"])
    else:
        print("Could not get prayer timing")

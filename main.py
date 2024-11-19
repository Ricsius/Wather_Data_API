from flask import Flask, render_template
import pandas as pd

STATION_ID_COLUMN = "STAID"
STATION_NAME_COLUMN = "STANAME                                 "
NEW_STATION_ID_COLUMN = "Station id"
NEW_STATION_NAME_COLUMN = "Station name"

DATE_COLUMN = "    DATE"
TEMPERATURE_COLUMN = "   TG"
DATA_PATH = "data"

app = Flask(__name__)

stations = pd.read_csv(f"{DATA_PATH}/stations.txt", skiprows=17)
stations[NEW_STATION_ID_COLUMN] = stations[STATION_ID_COLUMN]
stations[NEW_STATION_NAME_COLUMN] = stations[STATION_NAME_COLUMN]
stations = stations[[NEW_STATION_ID_COLUMN, NEW_STATION_NAME_COLUMN]]

def read_station(id):
    path = f"{DATA_PATH}\TG_STAID" + str(id).zfill(6) + ".txt"
    df = pd.read_csv(path, skiprows=20, parse_dates=[DATE_COLUMN])

    return df

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def get(station, date):
    df = read_station(station)
    temperature = df.loc[df[DATE_COLUMN] == date][TEMPERATURE_COLUMN].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<station>")
def all_data(station):
    df = read_station(station)
    result = df.to_dict(orient="records")

    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    year = str(year)
    df = read_station(station)
    df[DATE_COLUMN] = df[DATE_COLUMN].astype(str)
    result = df[df[DATE_COLUMN].str.startswith(year)].to_dict(orient="records")

    return result

if __name__ == "__main__":
    app.run(debug=True)
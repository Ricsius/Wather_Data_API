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

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def get(station, date):
    path = f"{DATA_PATH}\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(path, skiprows=20, parse_dates=[DATE_COLUMN])

    temperature = df.loc[df[DATE_COLUMN] == date][TEMPERATURE_COLUMN].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True)
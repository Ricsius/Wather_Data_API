from flask import Flask, render_template
import pandas as pd

DATE_COLUMN = "    DATE"
TEMPERATURE_COLUMN = "   TG"
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def get(station, date):
    path = "data\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(path, skiprows=20, parse_dates=[DATE_COLUMN])

    temperature = df.loc[df[DATE_COLUMN] == date][TEMPERATURE_COLUMN].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True)
import requests
import os
import io
import pandas as pd

from datetime import date
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("NETZTRANSPARENZ_ID")
CLIENT_SECRET = os.getenv("NETZTRANSPARENZ_SECRET")
TOKEN_URL = "https://identity.netztransparenz.de/users/connect/token"
BASE_URL = "https://ds.netztransparenz.de/api/v1/data"


def _get_token() -> str:
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_monatsmarktwerte(year=None):
    token = _get_token()
    year = year or date.today().year
    url = f"{BASE_URL}/marktpraemie/1/{year}/12/{year}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()

    df = pd.read_csv(
        io.StringIO(resp.text), sep=";", decimal=",", na_values=["N.A.", ""]
    )

    months = ["Januar", "Februar", "März",
              "April", "Mai", "Juni",
              "Juli", "August", "September",
              "Oktober", "November", "Dezember"]

    return {k: v for k, v in zip(months, df["MW Wind Onshore in ct/kWh"].to_list())}


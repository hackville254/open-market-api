import IP2Location
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALISATION = BASE_DIR / "localisation/IP2LOCATION-LITE-DB5.BIN"


def get_geo_data(ip):
    database = IP2Location.IP2Location(LOCALISATION)
    record = database.get_all(ip)
    geo_data = {
        "country": record.country_long,
        "region": record.region,
        "city": record.city,
    }
    return geo_data

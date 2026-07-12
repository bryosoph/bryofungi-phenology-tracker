import requests
import json
from datetime import datetime

# The primary search term used across biodiversity platforms
QUERY_TERM = "bryophilous"

def clean_date(date_str):
    """Normalizes variation in API timestamps to standard YYYY-MM-DD."""
    if not date_str:
        return None
    try:
        return date_str[:10]
    except Exception:
        return None

def fetch_inat():
    features = []
    url = f"https://api.inaturalist.org/v1/observations?q={QUERY_TERM}&per_page=200&geo=true"
    try:
        res = requests.get(url, timeout=15).json()
        for obs in res.get('results', []):
            coords = obs.get('geojson', {}).get('coordinates')
            date = clean_date(obs.get('observed_on'))
            if coords and date:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": coords},
                    "properties": {
                        "s": obs.get('taxon', {}).get('name', 'Unknown Fungi'),
                        "d": date,
                        "p": "iNat"
                    }
                })
    except Exception as e:
        print(f"Error fetching iNaturalist: {e}")
    return features

def fetch_gbif():
    features = []
    url = f"https://api.gbif.org/v1/occurrence/search?q={QUERY_TERM}&hasCoordinate=true&limit=300"
    try:
        res = requests.get(url, timeout=15).json()
        for occ in res.get('results', []):
            lng = occ.get('decimalLongitude')
            lat = occ.get('decimalLatitude')
            date = clean_date(occ.get('eventDate'))
            if lng and lat and date:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [float(lng), float(lat)]},
                    "properties": {
                        "s": occ.get('scientificName', 'Unknown Fungi').split(" ")[0:2],
                        "d": date,
                        "p": "GBIF"
                    }
                })
        # Format the split genus/species list back into a string
        for f in features:
            if isinstance(f["properties"]["s"], list):
                f["properties"]["s"] = " ".join(f["properties"]["s"])
    except Exception as e:
        print(f"Error fetching GBIF: {e}")
    return features

def fetch_mushroom_observer():
    features = []
    url = f"https://mushroomobserver.org/api2/observations?pattern={QUERY_TERM}&format=json"
    try:
        res = requests.get(url, timeout=15).json()
        for obs in res.get('results', []):
            lat = obs.get('latitude')
            lng = obs.get('longitude')
            date = clean_date(obs.get('date'))
            if lat and lng and date:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [float(lng), float(lat)]},
                    "properties": {
                        "s": obs.get('consensus_name', 'Unknown Fungi'),
                        "d": date,
                        "p": "MushObs"
                    }
                })
    except Exception as e:
        print(f"Error fetching Mushroom Observer: {e}")
    return features

def main():
    all_features = fetch_inat() + fetch_gbif() + fetch_mushroom_observer()
    
    geojson_out = {
        "type": "FeatureCollection",
        "features": all_features
    }
    
    # Save with absolute minimal whitespace to protect GitHub file limits
    with open("data.geojson", "w") as f:
        json.dump(geojson_out, f, separators=(',', ':'))
    print(f"Successfully processed {len(all_features)} unique phenology records.")

if __name__ == "__main__":
    main()

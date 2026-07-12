import os
import requests
import json
from datetime import datetime

# ==========================================
# TARGET BRYOPHILOUS TAXA FILTER CONFIGURATION
# ==========================================

TARGET_SPECIES = {
    "arrhenia retiruga", "bryobroma microcarpum", "bryobroma microcarpum var. racomitrii",
    "bryobroma velenovskyi", "bryocentria brongniartii", "bryocentria hypothallina",
    "bryocentria metzgeriae", "bryocentria octosporelloides", "bryochiton macrosporus",
    "bryochiton microscopicus", "bryochiton monascus", "bryoglossum gracile",
    "bryorutstroemia fulva", "bryoscyphus conocephali", "bryoscyphus dicrani",
    "bryoscyphus turbinatus", "bryosphaeria bryophila", "bryostroma trichostomi",
    "chromocyphella muscicola", "cistella polytrichi", "dactylospora scapanaria",
    "durella polytrichina", "eocronartium muscicola", "epibryon bryophilum",
    "epibryon casaresii", "epibryon diaphanum", "epibryon dicrani",
    "epibryon hepaticicola", "epibryon interlamellare", "epibryon metzgeriae",
    "epibryon muscicola", "epibryon plagiochilae", "epibryon turfosorum",
    "helotium schimperi", "hilberina sphagnorum", "hymenoscyphus vasaensis",
    "hyphodiscus delitescens", "lamprospora hispanica", "lamprospora miniata",
    "lamprospora tortulae-ruralis", "lamprospora wrightii", "lizonia baldinii",
    "luteodiscus hemiamyloideus", "mniaecia gloeocapsae", "mniaecia jungermanniae",
    "mniaecia nivea", "muscinupta laevis", "neottiella ricciae",
    "neottiella rutilans", "octospora affinis", "octospora axillaris",
    "octospora coccinea", "octospora excipulata", "octospora fissidentis",
    "octospora gemmicola", "octospora gyalectoides", "octospora humosa",
    "octospora itzerottii", "octospora leucoloma", "octospora lilacina",
    "octospora musci-muralis", "octospora orthotrichi", "octospora rustica",
    "octosporella perforata", "pezoloma marchantiae", "pithyella chalaudii",
    "pleostigma jungermannicola", "rickenella swartzii", "rimbachia arachnoidea",
    "rimbachia bryophila", "rimbachia neckerae"
}

OPEN_GENERA = {
    "bryobroma", "bryocentria", "bryochiton", "bryonectria", "bryopistillaria", 
    "bryoscyphus", "bryosphaeria", "chromocyphella", "eocronartium", "epibryon", 
    "gloeopeziza", "helotium", "lamprospora", "lizonia", "loreleia", "luteodiscus", 
    "octosporella", "pithyella", "potridiscus", "rimbachia"
}

EXCLUDED_CONIOCHAETA = {
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina"
}

def matches_target_taxa(scientific_name):
    if not scientific_name:
        return False
    name_clean = scientific_name.lower().strip()
    words = name_clean.split()
    if not words:
        return False
    genus = words[0]
    
    if name_clean in TARGET_SPECIES:
        return True
    if len(words) >= 2:
        binomial = f"{words[0]} {words[1]}"
        if binomial in TARGET_SPECIES:
            return True
        if genus == "coniochaeta":
            return binomial not in EXCLUDED_CONIOCHAETA
    if genus in OPEN_GENERA:
        return True
    return False

# ==========================================
# MULTI-PLATFORM DATA RETRIEVAL PIPELINE
# ==========================================

SEARCH_TERMS = sorted(OPEN_GENERA.union({
    "arrhenia", "bryoglossum", "bryorutstroemia", "cistella", "dactylospora", 
    "durella", "hilberina", "hymenoscyphus", "hyphodiscus", "mniaecia", 
    "muscinupta", "neottiella", "octospora", "pezoloma", "pleostigma", 
    "rickenella", "coniochaeta"
}))

def fetch_inaturalist():
    features = []
    url = "https://api.inaturalist.org/v1/observations"
    for term in SEARCH_TERMS:
        params = {"q": term, "iconic_taxa": "Fungi", "place_id": 97394, "per_page": 100}
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                for obs in res.json().get("results", []):
                    taxon_name = obs.get("taxon", {}).get("name") if obs.get("taxon") else None
                    if taxon_name and matches_target_taxa(taxon_name):
                        geom = obs.get("geojson")
                        date = obs.get("observed_on_details", {}).get("date")
                        if geom and date:
                            features.append({
                                "type": "Feature", "geometry": geom,
                                "properties": {
                                    "s": taxon_name, "d": date, "p": "iNaturalist",
                                    "u": f"https://www.inaturalist.org/observations/{obs.get('id')}"
                                }
                            })
        except Exception:
            continue
    return features

def fetch_gbif():
    features = []
    url = "https://api.gbif.org/v1/occurrence/search"
    # North America broad bounding box query logic
    for term in SEARCH_TERMS:
        params = {"q": term, "kingdomKey": 5, "decimalLatitude": "15,80", "decimalLongitude": "-170,-50", "limit": 100}
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                for record in res.json().get("results", []):
                    taxon_name = record.get("scientificName")
                    if taxon_name and matches_target_taxa(taxon_name):
                        lat = record.get("decimalLatitude")
                        lon = record.get("decimalLongitude")
                        date_str = record.get("eventDate")
                        if lat and lon:
                            date = date_str.split("T")[0] if date_str else "Unknown Date"
                            gbif_id = record.get("key")
                            features.append({
                                "type": "Feature",
                                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                                "properties": {
                                    "s": taxon_name.split(" ")[0] + " " + taxon_name.split(" ")[1] if len(taxon_name.split(" ")) >= 2 else taxon_name,
                                    "d": date, "p": "GBIF/Herbarium",
                                    "u": f"https://www.gbif.org/occurrence/{gbif_id}"
                                }
                            })
        except Exception:
            continue
    return features

def fetch_mushroom_observer():
    features = []
    url = "https://mushroomobserver.org/api2/observations"
    for term in SEARCH_TERMS:
        params = {"name": term, "format": "json", "detail": "high"}
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                for obs in res.json().get("results", []):
                    taxon_name = obs.get("consensus_name")
                    if taxon_name and matches_target_taxa(taxon_name):
                        # Filter North American coordinates broadly
                        lat = obs.get("latitude")
                        lon = obs.get("longitude")
                        date = obs.get("date")
                        if lat and lon and (15 <= lat <= 80) and (-170 <= lon <= -50):
                            features.append({
                                "type": "Feature",
                                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                                "properties": {
                                    "s": taxon_name, "d": date, "p": "Mushroom Observer",
                                    "u": f"https://mushroomobserver.org/{obs.get('id')}"
                                }
                            })
        except Exception:
            continue
    return features

def main():
    print("Initiating multi-platform API parsing across North America...")
    all_features = fetch_inaturalist() + fetch_gbif() + fetch_mushroom_observer()
    
    # Deduplicate matching entries across all metadata sources
    seen_ids = set()
    unique_features = []
    for f in all_features:
        coord_key = tuple(f["geometry"]["coordinates"])
        spec_key = (f["properties"]["s"].lower(), f["properties"]["d"], coord_key)
        if spec_key not in seen_ids:
            seen_ids.add(spec_key)
            unique_features.append(f)
            
    output_geojson = {
        "type": "FeatureCollection",
        "features": unique_features
    }
    
    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(output_geojson, f, ensure_ascii=False, indent=2)
        
    print(f"Pipeline finished! Saved multi-platform data.geojson with {len(unique_features)} total records.")

if __name__ == "__main__":
    main()

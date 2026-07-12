import os
import requests
import json
from datetime import datetime

# ==========================================
# TARGET BRYOPHILOUS TAXA FILTER CONFIGURATION
# ==========================================

# 1. Exact list of full species names / varieties to include
TARGET_SPECIES = {
    "arrhenia retiruga",
    "bryobroma microcarpum",
    "bryobroma microcarpum var. racomitrii",
    "bryobroma velenovskyi",
    "bryocentria brongniartii",
    "bryocentria hypothallina",
    "bryocentria metzgeriae",
    "bryocentria octosporelloides",
    "bryochiton macrosporus",
    "bryochiton microscopicus",
    "bryochiton monascus",
    "bryoglossum gracile",
    "bryorutstroemia fulva",
    "bryoscyphus conocephali",
    "bryoscyphus dicrani",
    "bryoscyphus turbinatus",
    "bryosphaeria bryophila",
    "bryostroma trichostomi",
    "chromocyphella muscicola",
    "cistella polytrichi",
    "dactylospora scapanaria",
    "durella polytrichina",
    "eocronartium muscicola",
    "epibryon bryophilum",
    "epibryon casaresii",
    "epibryon diaphanum",
    "epibryon dicrani",
    "epibryon hepaticicola",
    "epibryon interlamellare",
    "epibryon metzgeriae",
    "epibryon muscicola",
    "epibryon plagiochilae",
    "epibryon turfosorum",
    "helotium schimperi",
    "hilberina sphagnorum",
    "hymenoscyphus vasaensis",
    "hyphodiscus delitescens",
    "lamprospora hispanica",
    "lamprospora miniata",
    "lamprospora tortulae-ruralis",
    "lamprospora wrightii",
    "lizonia baldinii",
    "luteodiscus hemiamyloideus",
    "mniaecia gloeocapsae",
    "mniaecia jungermanniae",
    "mniaecia nivea",
    "muscinupta laevis",
    "neottiella ricciae",
    "neottiella rutilans",
    "octospora affinis",
    "octospora axillaris",
    "octospora coccinea",
    "octospora excipulata",
    "octospora fissidentis",
    "octospora gemmicola",
    "octospora gyalectoides",
    "octospora humosa",
    "octospora itzerottii",
    "octospora leucoloma",
    "octospora lilacina",
    "octospora musci-muralis",
    "octospora orthotrichi",
    "octospora rustica",
    "octosporella perforata",
    "pezoloma marchantiae",
    "pithyella chalaudii",
    "pleostigma jungermannicola",
    "rickenella swartzii",
    "rimbachia arachnoidea",
    "rimbachia bryophila",
    "rimbachia neckerae"
}

# 2. Genera where ALL species are included (except for the explicitly blacklisted ones)
OPEN_GENERA = {
    "bryobroma", "bryocentria", "bryochiton", "bryonectria", "bryopistillaria", 
    "bryoscyphus", "bryosphaeria", "chromocyphella", "eocronartium", "epibryon", 
    "gloeopeziza", "helotium", "lamprospora", "lizonia", "loreleia", "luteodiscus", 
    "octosporella", "pithyella", "potridiscus", "rimbachia"
}

# 3. Explicit species of Coniochaeta to filter out entirely
EXCLUDED_CONIOCHAETA = {
    "coniochaeta ambigua", 
    "coniochaeta leucoplaca", 
    "coniochaeta ligniaria", 
    "coniochaeta pulveracea", 
    "coniochaeta vagans", 
    "coniochaeta velutina"
}

def matches_target_taxa(scientific_name):
    """
    Strictly evaluates if an observation matches the exact criteria list.
    """
    if not scientific_name:
        return False
    
    name_clean = scientific_name.lower().strip()
    words = name_clean.split()
    if not words:
        return False
    
    genus = words[0]
    
    # Check 1: Is it an exact specific species name or variety from the list?
    if name_clean in TARGET_SPECIES:
        return True
    
    # Handle basic binomial string check if it contains common sub-taxa notations
    if len(words) >= 2:
        binomial = f"{words[0]} {words[1]}"
        if binomial in TARGET_SPECIES:
            return True
            
        # Check 2: Handle Coniochaeta logic (Include genus, but skip the explicit 6 exclusions)
        if genus == "coniochaeta":
            return binomial not in EXCLUDED_CONIOCHAETA

    # Check 3: Is it part of a genus where you want to track everything?
    if genus in OPEN_GENERA:
        return True
        
    return False

# ==========================================
# DATA RETRIEVAL PIPELINE
# ==========================================

def fetch_inaturalist_records():
    """
    Queries iNaturalist for target records across North America.
    """
    features = []
    url = "https://api.inaturalist.org/v1/observations"
    
    # Create a unique search list out of all specific target genera
    search_queries = OPEN_GENERA.union({"arrhenia", "bryoglossum", "bryorutstroemia", "cistella", "dactylospora", "durella", "hilberina", "hymenoscyphus", "hyphodiscus", "mniaecia", "muscinupta", "neottiella", "octospora", "pezoloma", "pleostigma", "rickenella", "coniochaeta"})
    
    for term in sorted(search_queries):
        params = {
            "q": term,
            "iconic_taxa": "Fungi",
            "place_id": 97394, # North America ID
            "per_page": 200,
            "only_id": "false"
        }
        try:
            res = requests.get(url, params=params, timeout=30)
            if res.status_code == 200:
                data = res.json()
                for obs in data.get("results", []):
                    taxon_name = obs.get("taxon", {}).get("name") if obs.get("taxon") else None
                    
                    if taxon_name and matches_target_taxa(taxon_name):
                        geojson_loc = obs.get("geojson")
                        obs_date = obs.get("observed_on_details", {}).get("date")
                        
                        if geojson_loc and obs_date:
                            features.append({
                                "type": "Feature",
                                "geometry": geojson_loc,
                                "properties": {
                                    "s": taxon_name,
                                    "d": obs_date,
                                    "p": "iNaturalist"
                                }
                            })
        except Exception as e:
            print(f"Error gathering data for query term '{term}': {e}")
            
    return features

def main():
    print("Initiating strict botanical API parsing across North America...")
    all_features = fetch_inaturalist_records()
    
    # Deduplicate entries that might overlap queries
    seen_ids = set()
    unique_features = []
    for f in all_features:
        coord_key = tuple(f["geometry"]["coordinates"])
        spec_key = (f["properties"]["s"], f["properties"]["d"], coord_key)
        if spec_key not in seen_ids:
            seen_ids.add(spec_key)
            unique_features.append(f)
            
    output_geojson = {
        "type": "FeatureCollection",
        "features": unique_features
    }
    
    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(output_geojson, f, ensure_ascii=False, indent=2)
        
    print(f"Pipeline finished! Created data.geojson with {len(unique_features)} precise target records.")

if __name__ == "__main__":
    main()

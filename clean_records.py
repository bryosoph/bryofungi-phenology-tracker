import os
import requests
import json
from datetime import datetime

# ==========================================
# TARGET TAXA & GENERA CONFIGURATION
# ==========================================

TARGET_SPECIES = {
    "arrhenia retiruga", "belonium coroniforme", "belonioscyphella hypnorum", 
    "bryobroma microcarpum", "bryobroma microcarpum var. racomitrii", "bryobroma velenovskyi", 
    "bryocentria brongniartii", "bryocentria hypothallina", "bryocentria metzgeriae", 
    "bryocentria octosporelloides", "bryocentria biannulata", "bryocentria pentamera", 
    "bryocentria chrysothrix", "bryocentria pachydesma", "bryocentria lusor", 
    "bryocentria navicula", "bryochiton macrosporus", "bryochiton microscopicus", 
    "bryochiton monascus", "bryoglossum gracile", "bryorutstroemia fulva", 
    "bryoscyphus conocephali", "bryoscyphus dicrani", "bryoscyphus hyalotectus", 
    "bryoscyphus turbinatus", "bryosphaeria bryophila", "bryostroma trichostomi", 
    "bryotria lagodes", "bryotria adelpha", "bryotria urophora", "bryonectria aphanes", 
    "bryonectria phyllogena", "bryonectria cuneifera", "bryonectria hylocomii", 
    "bryonectria anisopoda", "bryonectria callicarpa", 
    "chromocyphella muscicola", "cistella polytrichi", "dactylospora scapanaria", 
    "dawsomyces subinvisibilis", "durella polytrichina", "eocronartium muscicola", 
    "epibryon arachnoideum", "epibryon bryophilum", "epibryon bubakii", 
    "epibryon casaresii", "epibryon diaphanum", "epibryon dicrani", 
    "epibryon endocarpum", "epibryon harrisii", "epibryon hepaticicola", 
    "epibryon hypophyllum", "epibryon intercellulare", "epibryon interlamellare", 
    "epibryon metzgeriae", "epibryon muscicola", "epibryon pedinophylli", 
    "epibryon plagiochilae", "epibryon pogonati-urnigeri", "epibryon turfosorum", 
    "epibryon ventrale", "filicupula cyanopoda", "filicupula sororia", 
    "gloeopeziza interlamellaris", "helotium schimperi", "hilberina sphagnorum", 
    "hymenoscyphus vasaensis", "hyphodiscus delitescens", "laniatria myxostoma", 
    "lamprospora annulata", "lamprospora benkertii", "lamprospora campylopodis", 
    "lamprospora carbonicola", "lamprospora dicranellae", "lamprospora dictydiola", 
    "lamprospora feurichiana", "lamprospora hispanica", "lamprospora lubicensis", 
    "lamprospora lutziana", "lamprospora miniata", "lamprospora miniata var. miniata", 
    "lamprospora miniata var. parvispora", "lamprospora miniata var. ratisbonensis", 
    "lamprospora minuta", "lamprospora pseudoarvensis", "lamprospora seaveri", 
    "lamprospora tortulae-ruralis", "lamprospora tuberculata", "lamprospora tuberculatella", 
    "lizonia baldinii", "lizonia emperigonia", "lizonia sexangularis", 
    "luteodiscus hemiamyloideus", "mniaecia gloeocapsae", "mniaecia jungermanniae", 
    "mniaecia nivea", "muscinupta laevis", "neottiella ricciae", "neottiella rutilans", 
    "octospora affinis", "octospora axillaris", "octospora axillaris var. axillaris", 
    "octospora axillaris var. tetraspora", "octospora bridei", "octospora coccinea", 
    "octospora coccinea var. coccinea", "octospora coccinea var. tetraspora", 
    "octospora crosslandii", "octospora excipulata", "octospora fissidentis", 
    "octospora gemmicola", "octospora grimmiae", "octospora gyalectoides", 
    "octospora hetieri", "octospora humosa", "octospora ithacaensis", 
    "octospora itzerottii", "octospora leucoloma", "octospora leucoloma agg.", 
    "octospora leucoloma var. leucoloma", "octospora leucoloma var. tetraspora", 
    "octospora lilacina", "octospora meslinii", "octospora mnii", 
    "octospora musci-muralis", "octospora orthotrichi", "octospora phagospora", 
    "octospora rubens", "octospora rustica", "octospora similis", "octospora wrightii", 
    "octosporella brevibarbata", "octosporella caudifera", "octosporella imitatrix", 
    "octosporella jungermanniarum", "octosporella ornithocephala", "octosporella perforata", 
    "periantria bellacaptiva", "periantria frullaniae", "pezoloma marchantiae", 
    "pithyella chalaudii", "pithyella trigona", "pleostigma jungermannicola", 
    "potriphila navicularis", "protothelenella polytrichi", "rickenella swartzii", 
    "rimbachia arachnoidea", "rimbachia bryophila", "rimbachia neckerae", 
    "roseodiscus subcarneus", "stenocybe nitida", "trichosphaerella goniospora", 
    "trizodia acrobia"
}

OPEN_GENERA = {
    "bryobroma", "bryocentria", "bryotria", "bryochiton", "bryonectria", "bryopistillaria", 
    "bryoscyphus", "bryosphaeria", "eocronartium", "epibryon", 
    "filicupula", "gloeopeziza", "lamprospora", "lizonia", "loreleia", 
    "luteodiscus", "octospora", "octosporella", "periantria", "pithyella", 
    "potridiscus", "potriphila", "rimbachia", "roseodiscus"
}

# Automatically include any genera derived from target species
derived_target_genera = {s.split()[0] for s in TARGET_SPECIES}
OPEN_GENERA = OPEN_GENERA.union(derived_target_genera)

EXCLUDED_TAXA = {
    "helotium citrinum", "helotium aeruginosum", "helotium scutula",
    "helotium cyathoideum", "helotium destructor", "helotium epiphyllum",
    "helotium erraticum", "helotium fraternum", "helotium herbarum",
    "helotium midlandense", "helotium populinum", "helotium schimperi",
    "helotium sloaneae", "helotium urticae", "helotium virgultorum",
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina", "pithyella hispida"
}

# ==========================================
# FETCHING & PROCESSING LOGIC
# ==========================================

def fetch_inaturalist_observations():
    url = "https://api.inaturalist.org/v1/observations"
    features = []
    seen_ids = set()

    # Query per genus to ensure robust coverage including Roseodiscus
    queries_to_run = sorted(list(OPEN_GENERA))

    for taxon_query in queries_to_run:
        page = 1
        while page <= 5:  # Safe pagination ceiling per genus
            params = {
                "taxon_name": taxon_query,
                "quality_grade": "research",
                "geoprivacy": "open",
                "per_page": 200,
                "page": page
            }
            try:
                response = requests.get(url, params=params, timeout=15)
                if response.status_code != 200:
                    break
                data = response.json()
                results = data.get("results", [])
                if not results:
                    break

                for obs in results:
                    obs_id = obs.get("id")
                    if obs_id in seen_ids:
                        continue
                    
                    # Extract geometry
                    geom = obs.get("geometry")
                    loc = obs.get("location")
                    lat, lon = None, None
                    
                    if geom and geom.get("coordinates"):
                        lon, lat = geom["coordinates"]
                    elif loc:
                        lat_lon_str = loc.split(",")
                        lat, lon = float(lat_lon_str[0]), float(lat_lon_str[1])

                    if lat is None or lon is None:
                        continue

                    # Extract taxonomic identification
                    taxa_info = obs.get("taxon", {})
                    scientific_name = taxa_info.get("name", "").strip()

                    # Apply cleaning rules
                    if scientific_name == "Lizonia (Cesati":
                        scientific_name = "Lizonia"
                    elif "(" in scientific_name:
                        scientific_name = scientific_name.split("(")[0].strip()
                    elif scientific_name.endswith(","):
                        scientific_name = scientific_name.rstrip(",").strip()

                    name_lower = scientific_name.lower()

                    # Filtering checks
                    if name_lower in EXCLUDED_TAXA:
                        continue

                    name_parts = name_lower.split()
                    is_open_genus = len(name_parts) == 1 and name_lower in OPEN_GENERA
                    is_target_species = name_lower in TARGET_SPECIES

                    if is_open_genus or is_target_species:
                        seen_ids.add(obs_id)
                        obs_date = obs.get("observed_on") or (obs.get("created_at", "")[:10])
                        obs_url = f"https://www.inaturalist.org/observations/{obs_id}"

                        feature = {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [lon, lat]
                            },
                            "properties": {
                                "s": scientific_name,
                                "d": obs_date,
                                "p": "iNaturalist",
                                "u": obs_url
                            }
                        }
                        features.append(feature)

                if len(results) < 200:
                    break
                page += 1
            except Exception as e:
                print(f"Error querying {taxon_query}: {e}")
                break

    return features

if __name__ == "__main__":
    print("Fetching and cleaning records from iNaturalist...")
    all_features = fetch_inaturalist_observations()
    
    geojson_collection = {
        "type": "FeatureCollection",
        "features": all_features
    }

    output_filename = "records.geojson"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(geojson_collection, f, indent=2)

    print(f"Successfully generated {output_filename} with {len(all_features)} records (including Roseodiscus).")

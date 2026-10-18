import json
import sys

# Define taxa you want to explicitly include/target
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
    "octosporella perforata", "pezoloma marchantiae", "pithyella chalaudii", "pithyella trigona", 
    "pleostigma jungermannicola", "rickenella swartzii", "rimbachia arachnoidea",
    "rimbachia bryophila", "rimbachia neckerae", "trichosphaerella goniospora", 
}

OPEN_GENERA = {
    "bryobroma", "bryocentria", "bryochiton", "bryonectria", "bryopistillaria", 
    "bryoscyphus", "bryosphaeria", "chromocyphella", "eocronartium", "epibryon", 
    "gloeopeziza", "lamprospora", "lizonia", "loreleia", "luteodiscus", 
    "octosporella", "pithyella", "potridiscus", "rimbachia"
}

# Non-bryophilous species to explicitly drop
EXCLUDED_TAXA = {
    "helotium citrinum", "helotium aeruginosum", "helotium scutula",
    "helotium cyathoideum", "helotium destructor", "helotium epiphyllum",
    "helotium erraticum", "helotium fraternum", "helotium herbarum",
    "helotium midlandense", "helotium populinum", "helotium schimperi",
    "helotium sloaneae", "helotium urticae", "helotium virgultorum",
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina", "pithyella hispida"
}

def clean_records(input_path, output_path):
    # 1. Open and load the raw GeoJSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_features = []

    # 2. Loop through features and apply your cleaning logic
    for feature in data.get('features', []):
        geometry = feature.get('geometry')
        properties = feature.get('properties', {})
        
        taxon_name = properties.get('s', '').strip()
        
        # Clean up author names/trailing punctuation (e.g., "Lizonia (Cesati" -> "Lizonia", "Epibryon Döbbeler," -> "Epibryon")
        if taxon_name == "Lizonia (Cesati":
            taxon_name = "Lizonia"
        elif "(" in taxon_name:
            taxon_name = taxon_name.split("(")[0].strip()
        elif taxon_name.endswith(","):
            taxon_name = taxon_name.rstrip(",").strip()
            
        properties['s'] = taxon_name
        feature['properties'] = properties
        
        # 3. Validation & Strict Inclusion Filtering
        if geometry and geometry.get('coordinates'):
            name_lower = taxon_name.lower()
            
            # Check if it matches an open genus (single word) or specific target species
            name_parts = name_lower.split()
            is_open_genus = len(name_parts) == 1 and name_lower in OPEN_GENERA
            is_target_species = name_lower in TARGET_SPECIES
            
            if is_open_genus or is_target_species:
                cleaned_features.append(feature)
            
    # 4. Update the GeoJSON structure with the cleaned features
    data['features'] = cleaned_features
    
    # 5. Write out the cleaned records to the target path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully cleaned {len(cleaned_features)} records and saved to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python clean_records.py <input_geojson> <output_geojson>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    clean_records(input_file, output_file)

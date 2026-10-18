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

EXCLUDED_CONIOCHAETA = {
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina", "pithyella hispida", 
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
        
        # Clean up or standardize taxon names
        taxon_name = properties.get('s', '')
        
        # Example fixes or regex cleanups:
        if taxon_name == "Lizonia (Cesati":
            properties['s'] = "Lizonia"
        elif taxon_name.endswith("("):
            properties['s'] = taxon_name.rstrip("(").strip()
            
        # Make sure properties are saved back to the feature
        feature['properties'] = properties
        
        # 3. Filtering checks before keeping the feature
        if geometry and geometry.get('coordinates'):
            name_lower = properties.get('s', '').strip().lower()
            
            # Skip if explicitly excluded
            if name_lower in EXCLUDED_CONIOCHAETA:
                continue
                
            # Optional: Add your inclusion criteria here (e.g., must match target species or open genera)
            # For now, it keeps valid coordinates while filtering out exclusions.
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

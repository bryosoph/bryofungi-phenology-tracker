import json
import sys

# Define taxa you want to explicitly include/target
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
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_features = []

    for feature in data.get('features', []):
        geometry = feature.get('geometry')
        properties = feature.get('properties', {})
        
        taxon_name = properties.get('s', '').strip()
        
        if taxon_name == "Lizonia (Cesati":
            taxon_name = "Lizonia"
        elif "(" in taxon_name:
            taxon_name = taxon_name.split("(")[0].strip()
        elif taxon_name.endswith(","):
            taxon_name = taxon_name.rstrip(",").strip()
            
        properties['s'] = taxon_name
        feature['properties'] = properties
        
        if geometry and geometry.get('coordinates'):
            name_lower = taxon_name.lower()
            name_parts = name_lower.split()
            is_open_genus = len(name_parts) == 1 and name_lower in OPEN_GENERA
            is_target_species = name_lower in TARGET_SPECIES
            
            if is_open_genus or is_target_species:
                cleaned_features.append(feature)
            
    data['features'] = cleaned_features
    
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

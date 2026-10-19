import os
import requests
import json
from datetime import datetime

# ==========================================
# TARGET BRYOPHILOUS TAXA FILTER CONFIGURATION
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
    "bryonectria anisopoda", "bryonectria callicarpa", "chlorociboria lamellicola", 
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
    "bryoscyphus", "bryosphaeria", "chromocyphella", "eocronartium", "epibryon", 
    "filicupula", "gloeopeziza", "lamprospora", "lizonia", "loreleia", 
    "luteodiscus", "octospora", "octosporella", "periantria", "pithyella", 
    "potridiscus", "potriphila", "rimbachia"
}

EXCLUDED_CONIOCHAETA = {
    "coniochaeta ambigua", "coniochaeta leucoplaca", "coniochaeta ligniaria", 
    "coniochaeta pulveracea", "coniochaeta vagans", "coniochaeta velutina", "pithyella hispida", 
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
